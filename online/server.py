import socket, threading, json, sys, urllib.request, urllib.error, time

HOST = "0.0.0.0"
PORT = 1234

clients = []
choices = {}  # {conn: "rock"/"paper"/"scissors"}

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

def judge(c1, c2):
    if c1 == c2: return "draw"
    wins = {"rock":"scissors", "paper":"rock", "scissors":"paper"}
    return "p1" if wins[c1] == c2 else "p2"

def handle_game():
    if len(clients) < 2:
        return
    conn1, conn2 = clients[:2]
    send(conn1, {"type":"info","msg":"Game start! You are Player 1"})
    send(conn2, {"type":"info","msg":"Game start! You are Player 2"})

    round_no = 1
    while True:
        for conn in (conn1, conn2):
            send(conn, {"type":"prompt","msg":f"Round {round_no}: rock/paper/scissors (or 'quit')"})
        # collect choices
        for conn in (conn1, conn2):
            send(conn, {"type":"ask_choice"})
        for conn in (conn1, conn2):
            line = recv_line(conn)
            if line is None:
                return
            try:
                msg = json.loads(line)
            except:
                send(conn, {"type":"error","msg":"bad json"}); return
            if msg.get("type") == "choice":
                choice = msg.get("value","").lower()
                if choice == "quit":
                    send(conn1, {"type":"info","msg":"Game ended."})
                    send(conn2, {"type":"info","msg":"Game ended."})
                    return
                if choice not in ("rock","paper","scissors"):
                    send(conn, {"type":"error","msg":"Invalid choice"}); return
                choices[conn] = choice
        c1, c2 = choices.get(conn1), choices.get(conn2)
        result = judge(c1, c2)
        summary = {"type":"result","p1":c1,"p2":c2,"winner":result}
        send(conn1, summary)
        send(conn2, summary)
        round_no += 1

def client_thread(conn, addr):
    try:
        send(conn, {"type":"info","msg":"Waiting for another player..."})
        clients.append(conn)
        if len(clients) == 2:
            handle_game()
    finally:
        try: conn.close()
        except: pass

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