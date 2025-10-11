import socket, threading, sys, json, urllib.request, time

HOST = "0.0.0.0"
PORT = 1234

# --- Connection registry ---
clients_lock = threading.Lock()
clients = {}  # conn -> {"name": str, "addr": (ip,port)}

# ---------- Helpers to show addresses ----------
def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def list_local_ips():
    ips = set()
    try:
        hn = socket.gethostname()
        _, _, iplist = socket.gethostbyname_ex(hn)
        ips.update(iplist)
    except Exception:
        pass
    li = get_lan_ip()
    if li:
        ips.add(li)
    ips.add("127.0.0.1")
    return sorted(ips)

def detect_ngrok_tcp(port):
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=1.0) as r:
            data = json.loads(r.read().decode("utf-8"))
        for t in data.get("tunnels", []):
            pub_url = t.get("public_url", "")
            if pub_url.startswith("tcp://"):
                addr = t.get("config", {}).get("addr", "")
                if str(port) in addr:
                    pub = pub_url[len("tcp://"):]
                    if ":" in pub:
                        host, p = pub.split(":", 1)
                        return host, int(p)
    except Exception:
        pass
    return None

def print_share_info(actual_port):
    print("\n=== Connection Info ===")
    print(f"Server listening on 0.0.0.0:{actual_port}")
    lan = get_lan_ip()
    if lan:
        print(f"LAN IP (same Wi‑Fi): {lan}:{actual_port}")
        print(f"Clients can run:\n  python client.py {lan} {actual_port} <your_name>")
    else:
        print("LAN IP: (couldn’t auto-detect)")
    print("\nAll detected local addresses:")
    for ip in list_local_ips():
        print(f"  {ip}:{actual_port}")
    ng = detect_ngrok_tcp(actual_port)
    if ng:
        host, p = ng
        print("\nNgrok public address detected:")
        print(f"  {host}:{p}")
        print(f"Friends on the internet can run:\n  python client.py {host} {p} <your_name>")
    else:
        print("\nTip: To play over the internet, start ngrok in another terminal:")
        print(f"  ngrok tcp {actual_port}")
    print("=======================\n")

# ---------- Chat logic ----------
def send_line(conn, text):
    try:
        conn.sendall((text + "\n").encode("utf-8"))
        return True
    except OSError:
        return False

def broadcast(text, exclude=None):
    dead = []
    with clients_lock:
        for c in list(clients.keys()):
            if exclude is not None and c is exclude:
                continue
            if not send_line(c, text):
                dead.append(c)
        for d in dead:
            clients.pop(d, None)

def list_names():
    with clients_lock:
        return [info["name"] for info in clients.values()]

def recv_line(conn):
    buf = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        buf += chunk
        if buf.endswith(b"\n"):
            try:
                return buf.decode("utf-8").rstrip("\r\n")
            except UnicodeDecodeError:
                return None

def handle_client(conn, addr):
    # 1) Handshake: expect first line as "NAME:yourname"
    send_line(conn, "SYSTEM: Welcome! Please send your name as: NAME:your_name")
    first = recv_line(conn)
    if first is None or not first.startswith("NAME:"):
        send_line(conn, "SYSTEM: Invalid handshake. Closing.")
        try: conn.close()
        except: pass
        return
    name = first.split(":", 1)[1].strip()
    if not name:
        name = f"user_{addr[1]}"
    with clients_lock:
        clients[conn] = {"name": name, "addr": addr}
    # Inform everyone
    broadcast(f"SYSTEM: {name} joined. Users online: {', '.join(list_names())}")
    send_line(conn, "SYSTEM: Type /quit to leave. Type /who to list users.")

    # 2) Main loop
    while True:
        line = recv_line(conn)
        if line is None:
            break
        line = line.strip()
        if not line:
            continue
        if line == "/quit":
            break
        if line == "/who":
            send_line(conn, "SYSTEM: " + ", ".join(list_names()))
            continue
        # broadcast message
        broadcast(f"[{name}] {line}", exclude=None)

    # 3) Cleanup on exit
    with clients_lock:
        clients.pop(conn, None)
    broadcast(f"SYSTEM: {name} left. Users online: {', '.join(list_names())}")
    try: conn.close()
    except: pass

def choose_port(preferred):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, preferred))
    except OSError:
        s.bind((HOST, 0))  # auto free port
    s.listen(20)
    return s, s.getsockname()[1]

def main():
    global PORT
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            pass
    print("Starting chat server...")
    server_sock, actual_port = choose_port(PORT)
    print_share_info(actual_port)
    while True:
        conn, addr = server_sock.accept()
        print("Connected:", addr)
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()