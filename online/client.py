import socket, sys, json

def send(conn, msg):
    conn.sendall((json.dumps(msg) + "\n").encode("utf-8"))

def recv_line(conn):
    buf = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        buf += chunk
        if buf.endswith(b"\n"):
            return buf.decode("utf-8").strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_ip> [port]")
        return
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {host}:{port} ...")
        s.connect((host, port))
        print("Connected! Waiting…")
        while True:
            line = recv_line(s)
            if line is None:
                print("Disconnected.")
                break
            msg = json.loads(line)
            t = msg.get("type")
            if t == "info":
                print("[INFO]", msg.get("msg",""))
            elif t == "prompt":
                print(msg.get("msg",""))
            elif t == "ask_choice":
                choice = input("Your move (rock/paper/scissors or quit): ").strip().lower()
                send(s, {"type":"choice","value":choice})
            elif t == "result":
                print(f"Result: P1={msg['p1']}  P2={msg['p2']}  Winner={msg['winner']}")
            elif t == "error":
                print("Error:", msg.get("msg",""))
            else:
                print("Message:", msg)

if __name__ == "__main__":
    main()