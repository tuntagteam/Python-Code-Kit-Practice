import socket
import sys
import threading
import queue
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Configuration ----------------
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1234

ACCENT = "#7c5cff"      # accent color (buttons, highlights)
BG_DARK = "#111318"     # app background
BG_PANEL = "#171a21"    # panels
BG_INPUT = "#0f1116"
FG_TEXT = "#e5e7eb"     # primary text
FG_SUBTLE = "#9aa2b1"   # secondary text
FG_SYSTEM = "#60a5fa"   # system message color
FG_ME = "#a7f3d0"       # my message color
FG_PEER = "#f9d28c"     # other message color

# ---------------- Networking Thread ----------------
class ChatClient(threading.Thread):
    def __init__(self, host, port, name, incoming_queue, on_disconnect):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.name = name
        self.incoming_queue = incoming_queue
        self.on_disconnect = on_disconnect
        self.sock = None
        self._stop = threading.Event()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass
        s.connect((self.host, self.port))
        s.sendall((f"NAME:{self.name}\n").encode("utf-8"))
        self.sock = s

    def run(self):
        try:
            self.connect()
        except Exception as e:
            self.incoming_queue.put(("system", f"Failed to connect: {e}"))
            self.on_disconnect()
            return
        self.incoming_queue.put(("system", f"Connected to {self.host}:{self.port} as {self.name}"))
        buf = b""
        try:
            while not self._stop.is_set():
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        msg = line.decode("utf-8").rstrip("\r")
                    except UnicodeDecodeError:
                        msg = "(unreadable message)"
                    self.incoming_queue.put(("msg", msg))
        except OSError:
            pass
        finally:
            try:
                if self.sock:
                    self.sock.close()
            except Exception:
                pass
            self.on_disconnect()
            self.incoming_queue.put(("system", "Disconnected"))

    def send(self, text):
        if not self.sock:
            return
        try:
            if not text.endswith("\n"):
                text += "\n"
            self.sock.sendall(text.encode("utf-8"))
        except OSError:
            pass

    def stop(self):
        self._stop.set()
        try:
            self.send("/quit")
        except Exception:
            pass
        try:
            if self.sock:
                self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass

# ---------------- Theme ----------------
def apply_dark_theme(root: tk.Tk):
    style = ttk.Style(root)
    # base theme
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    # Global styling
    style.configure(".", background=BG_DARK, foreground=FG_TEXT, fieldbackground=BG_INPUT, borderwidth=0, focuscolor=ACCENT)
    style.configure("TFrame", background=BG_DARK)
    style.configure("Card.TFrame", background=BG_PANEL)
    style.configure("Header.TFrame", background=BG_PANEL)
    style.configure("TLabel", background=BG_DARK, foreground=FG_TEXT)
    style.configure("Header.TLabel", background=BG_PANEL, foreground=FG_TEXT, font=("Inter", 12, "bold"))
    style.configure("Subtle.TLabel", background=BG_PANEL, foreground=FG_SUBTLE)
    style.configure("TButton", background=ACCENT, foreground="white", padding=(12,6))
    style.map("TButton", background=[("active", "#6d49ff")])
    style.configure("Accent.TButton", background=ACCENT, foreground="white", padding=(10,6))
    style.configure("TEntry", fieldbackground=BG_INPUT, foreground=FG_TEXT, padding=8)
    style.configure("TMenubutton", background=BG_PANEL, foreground=FG_TEXT)
    style.configure("Vertical.TScrollbar", background=BG_PANEL, troughcolor=BG_DARK)
    # Listbox needs manual styling via tk config (handled later)

# ---------------- GUI ----------------
class ConnectDialog(tk.Toplevel):
    def __init__(self, master, on_connect):
        super().__init__(master)
        self.title("Connect to Chat")
        self.on_connect = on_connect
        self.resizable(False, False)
        self.configure(bg=BG_PANEL)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

        frm = ttk.Frame(self, style="Card.TFrame", padding=16)
        frm.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frm, text="Server Host:", style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.host_var = tk.StringVar(value=DEFAULT_HOST)
        ttk.Entry(frm, textvariable=self.host_var, width=28).grid(row=0, column=1, sticky="ew", pady=(0,6))

        ttk.Label(frm, text="Port:", style="Header.TLabel").grid(row=1, column=0, sticky="w", pady=(0,6))
        self.port_var = tk.StringVar(value=str(DEFAULT_PORT))
        ttk.Entry(frm, textvariable=self.port_var, width=10).grid(row=1, column=1, sticky="w", pady=(0,6))

        ttk.Label(frm, text="Your Name:", style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=(0,6))
        self.name_var = tk.StringVar(value="guest")
        ttk.Entry(frm, textvariable=self.name_var, width=28).grid(row=2, column=1, sticky="ew", pady=(0,6))

        btns = ttk.Frame(frm, style="Card.TFrame")
        btns.grid(row=3, column=0, columnspan=2, pady=(10,0), sticky="e")
        ttk.Button(btns, text="Connect", style="Accent.TButton", command=self._ok).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=self._cancel).grid(row=0, column=1)

        for i in range(3):
            frm.grid_rowconfigure(i, pad=4)
        frm.grid_columnconfigure(1, weight=1)

        self.bind("<Return>", lambda e: self._ok())

    def _ok(self):
        host = self.host_var.get().strip() or DEFAULT_HOST
        port_text = self.port_var.get().strip() or str(DEFAULT_PORT)
        name = self.name_var.get().strip() or "guest"
        try:
            port = int(port_text)
        except ValueError:
            messagebox.showerror("Invalid Port", "Port must be a number.")
            return
        self.on_connect(host, port, name)
        self.destroy()

    def _cancel(self):
        self.destroy()

class ChatUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python LAN Chat — Modern")
        self.geometry("980x620")
        self.configure(bg=BG_DARK)
        apply_dark_theme(self)

        # State
        self.client = None
        self.incoming = queue.Queue()
        self.me_name = ""

        # Header bar
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x", side="top")
        self.title_lbl = ttk.Label(header, text="Python LAN Chat", style="Header.TLabel")
        self.title_lbl.pack(side="left", padx=14, pady=10)
        self.status_lbl = ttk.Label(header, text="Disconnected", style="Subtle.TLabel")
        self.status_lbl.pack(side="right", padx=14, pady=10)

        # Main content
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, weight=0)

        # Chat area (bubbles)
        chat_card = ttk.Frame(main, style="Card.TFrame", padding=10)
        chat_card.grid(row=0, column=0, sticky="nsew", padx=(12,6), pady=(12,6))

        self.chat_text = tk.Text(chat_card, wrap="word", bd=0, highlightthickness=0, bg=BG_PANEL, fg=FG_TEXT)
        self.chat_text.config(state="disabled", padx=10, pady=10, insertbackground=FG_TEXT)
        yscroll = ttk.Scrollbar(chat_card, orient="vertical", command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=yscroll.set)
        self.chat_text.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        # Message tags (simulate bubbles)
        self.chat_text.tag_configure("time", foreground=FG_SUBTLE, spacing3=4, font=("Inter", 9))
        self.chat_text.tag_configure("system", foreground=FG_SYSTEM, spacing3=8, font=("Inter", 10, "italic"))
        self.chat_text.tag_configure("me", foreground=FG_ME, spacing3=6, font=("Inter", 11, "bold"))
        self.chat_text.tag_configure("peer", foreground=FG_PEER, spacing3=6, font=("Inter", 11))

        # Right panel: users
        side = ttk.Frame(main, style="Card.TFrame", padding=10)
        side.grid(row=0, column=1, sticky="nsew", padx=(6,12), pady=(12,6))
        self.server_lbl = ttk.Label(side, text="Server: —", style="Subtle.TLabel")
        self.server_lbl.pack(anchor="w")
        ttk.Label(side, text="Online Users", style="Header.TLabel").pack(anchor="w", pady=(10,4))
        self.users_list = tk.Listbox(side, height=10, bg=BG_PANEL, fg=FG_TEXT, activestyle="none", highlightthickness=0, bd=0, selectbackground=ACCENT)
        self.users_list.pack(fill="both", expand=True)

        # Bottom input area
        bottom = ttk.Frame(main, style="Card.TFrame", padding=10)
        bottom.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(6,12))
        bottom.columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(bottom, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.insert(0, "Type a message…")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<Return>", self._on_enter)
        # Shift+Enter -> newline (insert explicit \n)
        self.entry.bind("<Shift-Return>", lambda e: self._insert_newline())

        send_btn = ttk.Button(bottom, text="Send ↩", style="Accent.TButton", command=self.send_message)
        send_btn.grid(row=0, column=1, padx=(10,0))

        # Menu
        menubar = tk.Menu(self, tearoff=0)
        conn_menu = tk.Menu(menubar, tearoff=0)
        conn_menu.add_command(label="Connect…", command=self.open_connect)
        conn_menu.add_command(label="Disconnect", command=self.disconnect)
        conn_menu.add_separator()
        conn_menu.add_command(label="Clear Chat", command=self.clear_chat)
        conn_menu.add_separator()
        conn_menu.add_command(label="Quit", command=self._on_close)
        menubar.add_cascade(label="Session", menu=conn_menu)
        self.config(menu=menubar)

        # Start with connect dialog
        self.after(150, self.open_connect)
        # Poll incoming queue
        self.after(50, self._drain_incoming)

    # ---------- Connection management ----------
    def open_connect(self):
        if self.client:
            messagebox.showinfo("Connected", "Already connected.")
            return
        ConnectDialog(self, self._start_connection)

    def _start_connection(self, host, port, name):
        if self.client:
            return
        self.me_name = name
        self.status_lbl.config(text="Connecting…")
        self.server_lbl.config(text=f"Server: {host}:{port}")
        self._append_system(f"Connecting to {host}:{port} as {name} …")
        self.client = ChatClient(host, port, name, self.incoming, self._on_disconnect)
        self.client.start()

    def disconnect(self):
        if self.client:
            self.client.stop()
            self.client = None
            self.status_lbl.config(text="Disconnected")

    def _on_disconnect(self):
        # Called from network thread at end
        self.client = None
        self.status_lbl.config(text="Disconnected")

    # ---------- UI helpers ----------
    def _clear_placeholder(self, _e):
        if self.entry_var.get() == "Type a message…":
            self.entry_var.set("")

    def _insert_newline(self):
        # add a literal newline to entry
        current = self.entry_var.get()
        self.entry_var.set(current + "\\n")

    def clear_chat(self):
        self.chat_text.config(state="normal")
        self.chat_text.delete("1.0", "end")
        self.chat_text.config(state="disabled")

    def _append(self, text, tag=None):
        ts = time.strftime("%H:%M:%S")
        self.chat_text.config(state="normal")
        if tag == "system":
            self.chat_text.insert("end", f"[{ts}] {text}\n", ("system",))
        elif tag == "me":
            self.chat_text.insert("end", f"[{ts}] {text}\n", ("me",))
        elif tag == "peer":
            self.chat_text.insert("end", f"[{ts}] {text}\n", ("peer",))
        else:
            self.chat_text.insert("end", f"[{ts}] {text}\n")
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")

    def _append_system(self, text):
        self._append(f"SYSTEM: {text}", tag="system")

    def send_message(self):
        msg = self.entry_var.get().strip()
        if not msg or msg == "Type a message…":
            return
        if self.client:
            # Echo locally as "me" if not a command
            if not msg.startswith("/"):
                self._append(f"[{self.me_name}] {msg}", tag="me")
            self.client.send(msg)
        self.entry_var.set("")

    def _update_users_from_system_line(self, line):
        key = "Users online:"
        if key in line:
            after = line.split(key, 1)[1].strip()
            names = [n.strip() for n in after.split(",") if n.strip()]
            self.users_list.delete(0, "end")
            for n in names:
                self.users_list.insert("end", n)

    def _on_enter(self, _e):
        self.send_message()
        return "break"

    def _drain_incoming(self):
        try:
            while True:
                kind, payload = self.incoming.get_nowait()
                if kind == "msg":
                    # Decide styling by prefix
                    txt = payload
                    if txt.startswith("SYSTEM:"):
                        self._append(txt, tag="system")
                        self._update_users_from_system_line(txt)
                    elif txt.startswith("[") and "]" in txt:
                        # Looks like "[Name] message"
                        name = txt[1:txt.find("]")]
                        tag = "me" if name == self.me_name else "peer"
                        self._append(txt, tag=tag)
                    else:
                        self._append(txt, tag=None)
                elif kind == "system":
                    self._append_system(payload)
        except queue.Empty:
            pass
        self.after(50, self._drain_incoming)

    def _on_close(self):
        try:
            self.disconnect()
        finally:
            self.destroy()

if __name__ == "__main__":
    app = ChatUI()
    app.mainloop()