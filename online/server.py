import socket, threading, json, sys, urllib.request, urllib.error, time

HOST = "0.0.0.0"
PORT = 1234

clients = []
choices = {}  # {conn: "rock"/"paper"/"scissors"}
clients_lock = threading.Lock()
game_started = False

# ---------- Helpers to show addresses ----------
def get_lan_ip():
    """Best-effort LAN IP discovery (no external traffic actually sent)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def list_local_ips():
    """Collect likely local IPv4 addresses."""
    ips = set()
    try:
        hn = socket.gethostname()
        # hostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        _, _, iplist = socket.gethostbyname_ex(hn)
        ips.update(iplist)
    except Exception:
        pass
    # Add LAN ip detection
    li = get_lan_ip()
    if li:
        ips.add(li)
    # Always include localhost
    ips.add("127.0.0.1")
    return sorted(ips)

def detect_ngrok_tcp(port):
    """
    If ngrok is running locally, query its API for TCP tunnels and return
    (public_host, public_port) for our PORT if found. Otherwise return None.
    """
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=1.0) as r:
            data = json.loads(r.read().decode("utf-8"))
        for t in data.get("tunnels", []):
            pub_url = t.get("public_url", "")
            # We only care about tcp tunnels like "tcp://0.tcp.ap.ngrok.io:12345"
            if pub_url.startswith("tcp://"):
                # If it forwards to localhost:PORT, it's ours.
                cfg = t.get("config", {})
                addr = cfg.get("addr", "")
                # addr might be "http://localhost:5000" or "localhost:5000"
                if str(PORT) in addr:
                    # strip scheme
                    pub = pub_url[len("tcp://"):]
                    # split host:port
                    if ":" in pub:
                        host, p = pub.split(":", 1)
                        return host, int(p)
    except Exception:
        pass
    return None

def print_share_info():
    print("\n=== Connection Info ===")
    print(f"Server listening on 0.0.0.0:{PORT} (all interfaces)")
    lan = get_lan_ip()
    if lan:
        print(f"LAN IP (same Wi-Fi): {lan}:{PORT}")
        print(f"Clients on same network can run:\n  python client.py {lan} {PORT}")
    else:
        print("LAN IP: (couldn’t auto-detect)")

    ips = list_local_ips()
    if ips:
        print("\nAll detected local addresses:")
        for ip in ips:
            print(f"  {ip}:{PORT}")

    # Try to detect ngrok public TCP tunnel automatically
    ng = detect_ngrok_tcp(PORT)
    if ng:
        host, p = ng
        print("\nNgrok public address detected:")
        print(f"  {host}:{p}")
        print(f"Friends on the internet can run:\n  python client.py {host} {p}")
    else:
        print("\nTip: To play over the internet, start ngrok in another terminal:")
        print(f"  ngrok tcp {PORT}")
        print("Then share the tcp host:port that ngrok shows.")

    print("=======================\n")

# ---------- Game logic ----------
def send(conn, msg):
    data = (json.dumps(msg) + "\n").encode("utf-8")
    conn.sendall(data)

def recv_line(conn):
    buf = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        buf += chunk
        if buf.endswith(b"\n"):
            return buf.decode("utf-8").strip()

def safe_send(conn, msg):
    """Send JSON message; return True if success, False if connection is broken."""
    try:
        data = (json.dumps(msg) + "\n").encode("utf-8")
        conn.sendall(data)
        return True
    except OSError:
        return False

def judge(c1, c2):
    if c1 == c2: return "draw"
    wins = {"rock":"scissors", "paper":"rock", "scissors":"paper"}
    return "p1" if wins[c1] == c2 else "p2"

def handle_game():
    """Run a single game session for the first two clients."""
    global game_started
    # Snapshot players safely
    with clients_lock:
        if len(clients) < 2:
            return
        conn1, conn2 = clients[0], clients[1]

    # Notify players
    if not safe_send(conn1, {"type":"info","msg":"Game start! You are Player 1"}):
        cleanup_game(conn1, conn2)
        return
    if not safe_send(conn2, {"type":"info","msg":"Game start! You are Player 2"}):
        cleanup_game(conn1, conn2)
        return

    round_no = 1
    try:
        while True:
            for conn in (conn1, conn2):
                if not safe_send(conn, {"type":"prompt","msg":f"Round {round_no}: rock/paper/scissors (or 'quit')"}):
                    cleanup_game(conn1, conn2); return
            for conn in (conn1, conn2):
                if not safe_send(conn, {"type":"ask_choice"}):
                    cleanup_game(conn1, conn2); return

            round_choices = {}
            for conn in (conn1, conn2):
                line = recv_line(conn)
                if line is None:
                    cleanup_game(conn1, conn2); return
                try:
                    msg = json.loads(line)
                except Exception:
                    safe_send(conn, {"type":"error","msg":"bad json"})
                    cleanup_game(conn1, conn2); return
                if msg.get("type") == "choice":
                    choice = msg.get("value","").lower()
                    if choice == "quit":
                        safe_send(conn1, {"type":"info","msg":"Game ended."})
                        safe_send(conn2, {"type":"info","msg":"Game ended."})
                        cleanup_game(conn1, conn2); return
                    if choice not in ("rock","paper","scissors"):
                        safe_send(conn, {"type":"error","msg":"Invalid choice"})
                        cleanup_game(conn1, conn2); return
                    round_choices[conn] = choice

            c1, c2 = round_choices.get(conn1), round_choices.get(conn2)
            result = judge(c1, c2)
            summary = {"type":"result","p1":c1,"p2":c2,"winner":result}
            if not safe_send(conn1, summary) or not safe_send(conn2, summary):
                cleanup_game(conn1, conn2); return
            round_no += 1
    finally:
        cleanup_game(conn1, conn2)

def cleanup_game(conn1, conn2):
    """Close sockets and reset global game state."""
    global game_started
    for c in (conn1, conn2):
        try:
            c.close()
        except Exception:
            pass
    with clients_lock:
        # Remove the two players if they are still in the list
        for c in (conn1, conn2):
            try:
                if c in clients:
                    clients.remove(c)
            except Exception:
                pass
        game_started = False

def client_thread(conn, addr):
    global game_started
    try:
        safe_send(conn, {"type":"info","msg":"Waiting for another player..."})
        with clients_lock:
            clients.append(conn)
            should_start = (len(clients) >= 2) and (not game_started)
            if should_start:
                game_started = True
        if should_start:
            handle_game()
    finally:
        # Connection will be closed by cleanup_game or here if not in a game
        try:
            if conn.fileno() != -1:
                conn.close()
        except Exception:
            pass

def main():
    print(f"Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        print_share_info()  # <-- print IPs immediately after binding
        while True:
            conn, addr = s.accept()
            print("Connected:", addr)
            threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()