import socket, sys, threading, queue, time

def parse_args(argv):
    if len(argv) < 2:
        print("Usage: python client.py <server_ip> [port] [name]")
        print("   or  python client.py <server_ip:port> [name]")
        sys.exit(1)
    host = argv[1]
    port = None
    name = None
    if ":" in host:
        host, port_str = host.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            print("Invalid port in host:port")
            sys.exit(1)
        name = argv[2] if len(argv) > 2 else None
    else:
        port = int(argv[2]) if len(argv) > 2 else 5000
        name = argv[3] if len(argv) > 3 else None
    if not name:
        name = input("Enter your name: ").strip() or "guest"
    return host, port, name

def recv_loop(sock):
    try:
        buf = b""
        while True:
            ch = sock.recv(1)
            if not ch:
                print("\n[Disconnected by server]")
                break
            buf += ch
            if buf.endswith(b"\n"):
                try:
                    msg = buf.decode("utf-8").rstrip("\r\n")
                except UnicodeDecodeError:
                    msg = "(unreadable message)"
                print("\r" + msg + "\n> ", end="", flush=True)
                buf = b""
    except OSError:
        pass

def main():
    host, port, name = parse_args(sys.argv)
    print(f"Connecting to {host}:{port} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((host, port))
        s.settimeout(None)
        # Handshake: send name
        s.sendall((f"NAME:{name}\n").encode("utf-8"))

        # Start receiver thread
        threading.Thread(target=recv_loop, args=(s,), daemon=True).start()

        print("Connected! Type messages and press Enter. Commands: /who, /quit")
        print("> ", end="", flush=True)
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.rstrip("\r\n")
                if not line:
                    print("> ", end="", flush=True)
                    continue
                s.sendall((line + "\n").encode("utf-8"))
                if line == "/quit":
                    break
                print("> ", end="", flush=True)
        except KeyboardInterrupt:
            try:
                s.sendall(("/quit\n").encode("utf-8"))
            except OSError:
                pass
        finally:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

if __name__ == "__main__":
    main()