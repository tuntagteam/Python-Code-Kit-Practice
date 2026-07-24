import tkinter as tk
import hashlib
import random
import time
import threading

# ---------------- Terminal Window ----------------
class HackTerminal:
    def __init__(self, root):
        self.root = root
        root.title("HackSim Linux Terminal")

        self.text = tk.Text(root, bg="black", fg="#00ff55",
                            insertbackground="#00ff55",
                            font=("Consolas", 12), wrap="word")
        self.text.pack(fill="both", expand=True)

        self.text.bind("<Return>", self.enter_pressed)

        self.prompt = "tag@hacksim:~$ "
        self.insert_prompt()

        self.command_start = "end-1c linestart"

        # available commands
        self.commands = {
            "help": self.help_cmd,
            "clear": self.clear_cmd,
            "hash crack": self.hash_crack_cmd,
            "sha256 crack": self.sha256_crack_cmd,
            "encrypt": self.encrypt_cmd,
            "decrypt": self.decrypt_cmd,
            "sniff": self.sniff_cmd,
            "handshake": self.handshake_cmd,
            "matrix": self.matrix_cmd
        }

    # insert terminal prompt
    def insert_prompt(self):
        self.text.insert("end", "\n" + self.prompt)
        self.text.see("end")

    def enter_pressed(self, event):
        # Read command
        line = self.text.get(self.command_start, "end").strip()
        if line.startswith(self.prompt):
            cmd = line[len(self.prompt):]
            self.run_command(cmd)

        # stop extra newline
        return "break"

    # ------------------ Commands ------------------
    def run_command(self, cmd):
        # empty
        if not cmd:
            self.insert_prompt()
            return

        # find best matching command
        for keyword in self.commands:
            if cmd.startswith(keyword):
                threading.Thread(target=self.commands[keyword], args=(cmd,)).start()
                return

        self.text.insert("end", f"\nUnknown command: {cmd}")
        self.insert_prompt()

    # HELP
    def help_cmd(self, *_):
        help_text = """
Available commands:
  help              - Show this help
  clear             - Clear terminal
  hash crack <md5>  - Crack MD5 hash using small dictionary
  sha256 crack <hash> - Crack SHA256 hash
  encrypt <text>    - Encrypt using SHA256
  decrypt <sha256>  - (Fake) decrypt: attempts dictionary match
  sniff             - Fake packet sniffing animation
  handshake         - Fake WiFi handshake capture
  matrix            - Enter MATRIX mode
"""
        self.text.insert("end", help_text)
        self.insert_prompt()

    # CLEAR
    def clear_cmd(self, *_):
        self.text.delete("1.0", "end")
        self.insert_prompt()

    # MD5 Crack
    def hash_crack_cmd(self, cmd):
        parts = cmd.split()
        if len(parts) < 3:
            self.text.insert("end", "\nUsage: hash crack <md5_hash>")
            self.insert_prompt()
            return

        target = parts[2]
        self.text.insert("end", f"\nCracking MD5 → {target}\n")

        dictionary = ["admin", "123456", "password", "tag", "qwerty", "letmein"]

        for word in dictionary:
            hashed = hashlib.md5(word.encode()).hexdigest()
            self.text.insert("end", f"Trying: {word} → {hashed}\n")
            self.text.see("end")
            time.sleep(0.3)

            if hashed == target:
                self.text.insert("end", f"\n✔ Match found! Password = {word}\n")
                self.insert_prompt()
                return

        self.text.insert("end", "\n❌ Password not found.\n")
        self.insert_prompt()

    # SHA256 Crack
    def sha256_crack_cmd(self, cmd):
        parts = cmd.split()
        if len(parts) < 3:
            self.text.insert("end", "\nUsage: sha256 crack <hash>")
            self.insert_prompt()
            return

        target = parts[2]
        self.text.insert("end", f"\nCracking SHA256 → {target}\n")

        dictionary = ["tag", "password", "king", "hacker", "dragon", "123456"]

        for word in dictionary:
            hashed = hashlib.sha256(word.encode()).hexdigest()
            self.text.insert("end", f"Trying: {word} → {hashed}\n")
            self.text.see("end")
            time.sleep(0.25)

            if hashed == target:
                self.text.insert("end", f"\n✔ Match found! Word = {word}\n")
                self.insert_prompt()
                return

        self.text.insert("end", "\n❌ Match not found.\n")
        self.insert_prompt()

    # ENCRYPT TEXT (SHA256)
    def encrypt_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            self.text.insert("end", "\nUsage: encrypt <text>")
            self.insert_prompt()
            return

        text = parts[1]
        hashed = hashlib.sha256(text.encode()).hexdigest()

        self.text.insert("end", f"\nSHA256({text}) =\n{hashed}\n")
        self.insert_prompt()

    # FAKE DECRYPT
    def decrypt_cmd(self, cmd):
        parts = cmd.split()
        if len(parts) < 2:
            self.text.insert("end", "\nUsage: decrypt <sha256>")
            self.insert_prompt()
            return

        target = parts[1]
        self.text.insert("end", f"\nAttempting to decrypt SHA256 (impossible)...\n")
        time.sleep(1)
        self.text.insert("end", "\nUsing fallback dictionary matching...\n")

        dictionary = ["tag", "admin", "secret", "password", "dragon"]

        for word in dictionary:
            hashed = hashlib.sha256(word.encode()).hexdigest()
            self.text.insert("end", f"Test: {word}\n")
            self.text.see("end")
            time.sleep(0.22)

            if hashed == target:
                self.text.insert("end", f"\n✔ Match found! Word = {word}\n")
                self.insert_prompt()
                return

        self.text.insert("end", "\n❌ No dictionary match.\n")
        self.insert_prompt()

    # PACKET SNIFFING SIMULATION
    def sniff_cmd(self, *_):
        self.text.insert("end", "\nStarting packet sniffing...\n")
        for _ in range(20):
            packet = f"Packet {_:02d} | src=192.168.1.{random.randint(1,255)} | dst=10.0.0.{random.randint(1,255)} | size={random.randint(40,1500)} bytes"
            self.text.insert("end", packet + "\n")
            self.text.see("end")
            time.sleep(0.1)
        self.text.insert("end", "\n✔ Sniffing complete.\n")
        self.insert_prompt()

    # WIFI HANDSHAKE SIMULATION
    def handshake_cmd(self, *_):
        self.text.insert("end", "\nCapturing WPA2 handshake...\n")
        for i in range(1, 6):
            self.text.insert("end", f"Handshake part {i}/4 captured...\n")
            self.text.see("end")
            time.sleep(0.4)
        self.text.insert("end", "\n✔ WPA2 Handshake saved to handshake.cap\n")
        self.insert_prompt()

    # MATRIX MODE
    def matrix_cmd(self, *_):
        self.text.insert("end", "\nEntering MATRIX mode...\n")
        self.text.see("end")
        for _ in range(200):
            line = "".join(random.choice("01abcdefghijklmnopqrstuvwxyz#$%&") for _ in range(60))
            self.text.insert("end", "\033[32m" + line + "\033[0m\n")
            self.text.see("end")
            time.sleep(0.03)
        self.text.insert("end", "\n✔ Matrix sequence complete.\n")
        self.insert_prompt()


# ---------------- RUN PROGRAM ----------------
root = tk.Tk()
app = HackTerminal(root)
root.mainloop()