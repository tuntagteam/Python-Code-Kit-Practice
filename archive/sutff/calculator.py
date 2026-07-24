import tkinter as tk

class CalculatorApp:
    def __init__(self, root):
        root.title("Calculator")
        root.resizable(False, False)
        root.configure(bg="#0b0f19")  # deep space background
        root.geometry("480x720")  # bigger canvas

        # Main container (card-like with neon border)
        self.container = tk.Frame(
            root,
            bg="#121826",
            bd=0,
            highlightthickness=2,
            highlightbackground="#8b5cf6",  # purple
            highlightcolor="#8b5cf6",
            relief="flat"
        )
        self.container.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.expression = tk.StringVar(value="")
        self.last_was_equals = False

        # Brand/header strip
        self.brand = tk.Label(
            self.container,
            text="NEON • CALC",
            anchor="w",
            font=("Helvetica", 12, "bold"),
            fg="#a78bfa",  # light purple
            bg="#121826"
        )
        self.brand.grid(row=0, column=0, columnspan=4, sticky="ew", padx=16, pady=(14, 0))

        # Display (mono, glassy)
        self.display = tk.Entry(
            self.container,
            textvariable=self.expression,
            font=("Courier New", 34, "bold"),
            justify="right",
            bd=0,
            bg="#0d1220",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
        )
        self.display.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=16, pady=(10, 14), ipady=24)

        # Button styles
        self.colors = {
            # Dark surfaces
            "num_bg": "#111827",
            "num_fg": "#e5e7eb",
            # Neon operators
            "op_bg":  "#7c3aed",  # purple
            "op_fg":  "#ffffff",
            # Function keys (C, etc.)
            "fn_bg":  "#374151",
            "fn_fg":  "#e5e7eb",
            # Equals (special cyan)
            "eq_bg":  "#06b6d4",
            "eq_hover": "#22d3ee",
            # Hovers
            "hover_light": "#1f2937",
            "hover_orange": "#a78bfa",  # repurposed for operators hover
            "hover_fn": "#4b5563",
        }

        # Grid config (bigger touch targets)
        for i in range(2, 7):  # rows 2..6 after brand+display
            self.container.grid_rowconfigure(i, weight=1, minsize=100)
        for j in range(4):
            self.container.grid_columnconfigure(j, weight=1, minsize=100)

        # Buttons layout (Apple-ish)
        # Row 1: C  /  *  -
        self._make_button("C", 2, 0, self.clear,  style="fn")
        self._make_button("÷", 2, 1, lambda: self.add_op("/"), style="op")
        self._make_button("×", 2, 2, lambda: self.add_op("*"), style="op")
        self._make_button("−", 2, 3, lambda: self.add_op("-"), style="op")

        # Row 2: 7  8  9  +
        self._make_button("7", 3, 0, lambda: self.add_char("7"))
        self._make_button("8", 3, 1, lambda: self.add_char("8"))
        self._make_button("9", 3, 2, lambda: self.add_char("9"))
        self._make_button("+", 3, 3, lambda: self.add_op("+"), style="op")

        # Row 3: 4  5  6  =
        self._make_button("4", 4, 0, lambda: self.add_char("4"))
        self._make_button("5", 4, 1, lambda: self.add_char("5"))
        self._make_button("6", 4, 2, lambda: self.add_char("6"))
        self.eq_btn = self._make_button("=", 4, 3, self.equals, style="eq", rowspan=2)  # tall neon equals

        # Row 4: 1  2  3
        self._make_button("1", 5, 0, lambda: self.add_char("1"))
        self._make_button("2", 5, 1, lambda: self.add_char("2"))
        self._make_button("3", 5, 2, lambda: self.add_char("3"))

        # Row 5: 0 (span 2)
        self._make_button("0", 6, 0, lambda: self.add_char("0"), colspan=2)
        # (We keep it minimal per request—no decimal button.)
        # Fill last two cells with spacing buttons to keep symmetry
        self._make_spacer(6, 2)
        self._make_spacer(6, 3)

        # Key bindings
        for ch in "0123456789":
            root.bind(ch, self._key_digit)
        for ch in "+-*/":
            root.bind(ch, self._key_op)
        root.bind("<Return>", lambda e: self.equals())
        root.bind("<KP_Enter>", lambda e: self.equals())
        root.bind("<Escape>", lambda e: self.clear())
        root.bind("<BackSpace>", lambda e: self.backspace())

        # Start neon animations
        self._animate_border()
        self._pulse_button(self.eq_btn)

    # ---------- UI helpers ----------
    def _make_button(self, text, r, c, cmd, style="num", rowspan=1, colspan=1):
        if style == "eq":
            bg, fg, hover = self.colors["eq_bg"], "#00151a", self.colors["eq_hover"]
        elif style == "op":
            bg, fg, hover = self.colors["op_bg"], self.colors["op_fg"], self.colors["hover_orange"]
        elif style == "fn":
            bg, fg, hover = self.colors["fn_bg"], self.colors["fn_fg"], self.colors["hover_fn"]
        else:
            bg, fg, hover = self.colors["num_bg"], self.colors["num_fg"], self.colors["hover_light"]

        btn = tk.Button(
            self.display.master,
            text=text,
            command=cmd,
            font=("Helvetica", 24, "bold"),
            bd=0,
            relief="flat",
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            padx=0, pady=0,
            highlightthickness=0
        )
        btn.grid(row=r, column=c, rowspan=rowspan, columnspan=colspan, sticky="nsew", padx=12, pady=12, ipady=24)

        # Hover effect
        def on_enter(e): btn.configure(bg=hover)
        def on_leave(e): btn.configure(bg=bg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _make_spacer(self, r, c):
        frame = tk.Frame(self.display.master, bg="#121826", bd=0, highlightthickness=0)
        frame.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

    # ---------- Logic ----------
    def add_char(self, ch: str):
        if self.last_was_equals:
            # Start a new expression after equals if the next input is a number
            self.expression.set("")
            self.last_was_equals = False
        self.expression.set(self.expression.get() + ch)

    def add_op(self, op: str):
        expr = self.expression.get()
        if not expr:
            # Disallow starting with operator
            return
        if expr[-1] in "+-*/":
            # Replace last operator
            expr = expr[:-1] + op
        else:
            expr += op
        self.expression.set(expr)
        self.last_was_equals = False

    def clear(self):
        self.expression.set("")
        self.last_was_equals = False

    def equals(self):
        expr = self.expression.get()
        if not expr:
            return
        # Sanitize: keep only digits and allowed ops
        safe = "".join(ch for ch in expr if ch in "0123456789+-*/ ")
        try:
            # Evaluate safely (limited to the filtered characters)
            result = eval(safe, {"__builtins__": None}, {})
            self.expression.set(str(result))
            self.last_was_equals = True
        except Exception:
            self.expression.set("Error")
            self.last_was_equals = True

    def backspace(self):
        expr = self.expression.get()
        if not expr or expr == "Error":
            self.clear()
            return
        self.expression.set(expr[:-1])
        self.last_was_equals = False

    # ---------- Neon animations ----------
    def _animate_border(self):
        # cycle through purple → blue → cyan for the container highlight
        palette = ["#8b5cf6", "#6366f1", "#3b82f6", "#06b6d4", "#22d3ee"]
        current = getattr(self, "_border_i", 0)
        self.container.configure(highlightbackground=palette[current], highlightcolor=palette[current])
        self._border_i = (current + 1) % len(palette)
        self.container.after(600, self._animate_border)

    def _pulse_button(self, btn):
        if not btn:
            return
        colors = [self.colors["eq_bg"], self.colors["eq_hover"]]
        idx = getattr(self, "_pulse_i", 0)
        btn.configure(bg=colors[idx], activebackground=colors[1-idx])
        self._pulse_i = 1 - idx
        btn.after(700, lambda: self._pulse_button(btn))

    # ---------- Key handlers ----------
    def _key_digit(self, event):
        self.add_char(event.char)

    def _key_op(self, event):
        self.add_op(event.char)

if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()