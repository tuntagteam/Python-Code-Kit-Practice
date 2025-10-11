import socket, sys, json, time

def parse_args(argv):
    if len(argv) < 2:
        print("Usage: python client.py <server_ip> [port]")
        print("       python client.py <server_ip:port>")
        sys.exit(1)
    host = argv[1]
    port = None
    if ":" in host:
        host, port_str = host.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            print("Invalid port in host:port")
            sys.exit(1)
    if port is None:
        port = int(argv[2]) if len(argv) > 2 else 5000
    return host, port

def send(conn, msg):
    try:
        conn.sendall((json.dumps(msg) + "\n").encode("utf-8"))
    except (BrokenPipeError, OSError):
        print("Connection lost while sending.")
        raise

def recv_line(conn, timeout=None):
    """Read a JSON line terminated by \n. Returns str or None if disconnected."""
    conn.settimeout(timeout)
    buf = b""
    try:
        while True:
            chunk = conn.recv(1)
            if not chunk:
                return None
            buf += chunk
            if buf.endswith(b"\n"):
                return buf.decode("utf-8").strip()
    except socket.timeout:
        return "__TIMEOUT__"
    except OSError:
        return None

def prompt_choice():
    while True:
        choice = input("Your move (rock/paper/scissors or quit): ").strip().lower()
        if choice in ("rock", "paper", "scissors", "quit"):
            return choice
        print("Please type rock, paper, scissors, or quit.")

def main():
    host, port = parse_args(sys.argv)
    print(f"Connecting to {host}:{port} ...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # connect timeout
            s.connect((host, port))
            s.settimeout(None)  # back to blocking for game messages
            print("Connected! Waiting for server messages…")
            while True:
                line = recv_line(s, timeout=None)
                if line is None:
                    print("Disconnected from server.")
                    break
                if line == "__TIMEOUT__":
                    print("Timed out waiting for server.")
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    print("Received non-JSON message:", line)
                    continue
                t = msg.get("type")
                if t == "info":
                    print("[INFO]", msg.get("msg",""))
                elif t == "prompt":
                    print(msg.get("msg",""))
                elif t == "ask_choice":
                    choice = prompt_choice()
                    send(s, {"type":"choice","value":choice})
                elif t == "result":
                    print(f"Result: P1={msg.get('p1')}  P2={msg.get('p2')}  Winner={msg.get('winner')}")
                elif t == "error":
                    print("[ERROR]", msg.get("msg",""))
                else:
                    print("[MESSAGE]", msg)
    except (ConnectionRefusedError, TimeoutError):
        print("Cannot connect to server. Is it running and reachable?")
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()