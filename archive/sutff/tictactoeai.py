

# Tic-Tac-Toe AI with Animated UI (Tkinter)
# Features:
# - Easy / Hard difficulty (random vs. minimax)
# - Smooth "grow" animation when marks appear
# - Hover highlight, status bar, and Reset button
# - Clean single-file script

import tkinter as tk
import random
import math
from typing import List, Optional, Tuple

# ----------------------------
# Game Logic
# ----------------------------
Board = List[Optional[str]]  # 9 items of 'X', 'O', or None

LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diagonals
]

def winner(board: Board) -> Optional[str]:
    for a,b,c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board: Board) -> bool:
    return all(board[i] is not None for i in range(9))

# --- Minimax for Hard ---

def minimax(board: Board, is_max: bool, me: str, opp: str) -> int:
    w = winner(board)
    if w == me:  # AI wins
        return 1
    if w == opp: # human wins
        return -1
    if is_full(board):
        return 0

    best = -math.inf if is_max else math.inf
    for i in range(9):
        if board[i] is None:
            board[i] = me if is_max else opp
            val = minimax(board, not is_max, me, opp)
            board[i] = None
            if is_max:
                best = max(best, val)
            else:
                best = min(best, val)
    return int(best)

def best_move_minimax(board: Board, me: str) -> int:
    opp = 'O' if me == 'X' else 'X'
    best_score = -10
    best_idx = -1
    # small ordering helps pruning a bit on average
    for i in [4,0,2,6,8,1,3,5,7]:
        if board[i] is None:
            board[i] = me
            score = minimax(board, False, me, opp)
            board[i] = None
            if score > best_score:
                best_score = score
                best_idx = i
    return best_idx

# --- Easy AI ---

def best_move_easy(board: Board, me: str) -> int:
    """Easy = random legal, with a tiny bit of defense (block if obvious)."""
    opp = 'O' if me == 'X' else 'X'
    # 1) try to win in 1
    for i in range(9):
        if board[i] is None:
            board[i] = me
            if winner(board) == me:
                board[i] = None
                return i
            board[i] = None
    # 2) try to block opponent's immediate win
    for i in range(9):
        if board[i] is None:
            board[i] = opp
            if winner(board) == opp:
                board[i] = None
                return i
            board[i] = None
    # 3) otherwise random
    choices = [i for i in range(9) if board[i] is None]
    return random.choice(choices) if choices else -1

# ----------------------------
# UI / Animation
# ----------------------------
CELL = 120
PADDING = 20
W = H = CELL * 3
LINE_COLOR = "#222"
MARK_X = "#0B84FF"
MARK_O = "#FF5D5D"
HOVER_COLOR = "#e9f3ff"
WIN_HIGHLIGHT = "#3bd16f"

class TicTacToeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Easy/Hard) — Animated")
        self.board: Board = [None]*9
        self.human = 'X'
        self.ai = 'O'
        self.game_over = False

        top = tk.Frame(root)
        top.pack(fill="x", padx=12, pady=8)

        tk.Label(top, text="Difficulty:").pack(side="left")
        self.difficulty = tk.StringVar(value="Easy")
        tk.OptionMenu(top, self.difficulty, "Easy", "Hard").pack(side="left", padx=6)

        tk.Button(top, text="Reset", command=self.reset).pack(side="left", padx=6)
        self.status = tk.Label(top, text="Your turn (X)")
        self.status.pack(side="right")

        self.canvas = tk.Canvas(root, width=W, height=H, bg="white", highlightthickness=0)
        self.canvas.pack(padx=12, pady=12)

        # draw grid
        for i in range(1,3):
            x = i*CELL
            self.canvas.create_line(x, 0, x, H, width=3, fill=LINE_COLOR)
            self.canvas.create_line(0, i*CELL, W, i*CELL, width=3, fill=LINE_COLOR)

        # hover highlight rectangle
        self.hover_rect = self.canvas.create_rectangle(0,0,0,0, outline="", fill="")

        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", lambda e: self.canvas.itemconfigure(self.hover_rect, fill=""))
        self.canvas.bind("<Button-1>", self.on_click)

    # --- Helpers ---
    def idx_from_xy(self, x: int, y: int) -> int:
        col = x // CELL
        row = y // CELL
        idx = int(row*3 + col)
        return idx if 0 <= idx < 9 else -1

    def cell_bounds(self, idx: int) -> Tuple[int,int,int,int]:
        r, c = divmod(idx, 3)
        x1, y1 = c*CELL, r*CELL
        return (x1, y1, x1+CELL, y1+CELL)

    def cell_center(self, idx: int) -> Tuple[int,int]:
        x1, y1, x2, y2 = self.cell_bounds(idx)
        return ((x1+x2)//2, (y1+y2)//2)

    # --- Events ---
    def on_motion(self, e):
        if self.game_over:
            self.canvas.itemconfigure(self.hover_rect, fill="")
            return
        idx = self.idx_from_xy(e.x, e.y)
        if idx == -1 or self.board[idx] is not None:
            self.canvas.itemconfigure(self.hover_rect, fill="")
            return
        x1,y1,x2,y2 = self.cell_bounds(idx)
        pad = 6
        self.canvas.coords(self.hover_rect, x1+pad, y1+pad, x2-pad, y2-pad)
        self.canvas.itemconfigure(self.hover_rect, fill=HOVER_COLOR)

    def on_click(self, e):
        if self.game_over:
            return
        idx = self.idx_from_xy(e.x, e.y)
        if idx == -1 or self.board[idx] is not None:
            return
        self.play_mark(idx, self.human)

        if self.check_game_end():
            return
        self.root.after(200, self.ai_turn)  # small delay for UX

    # --- Gameplay ---
    def ai_turn(self):
        if self.game_over:
            return
        diff = self.difficulty.get()
        if diff == "Hard":
            idx = best_move_minimax(self.board[:], self.ai)
        else:
            idx = best_move_easy(self.board[:], self.ai)
        if idx != -1 and self.board[idx] is None:
            self.play_mark(idx, self.ai)
            self.check_game_end()

    def play_mark(self, idx: int, mark: str):
        self.board[idx] = mark
        self.animate_mark(idx, mark)
        self.status.configure(text=("AI thinking..." if mark == self.human else "Your turn (X)"))

    def check_game_end(self) -> bool:
        w = winner(self.board)
        if w:
            self.game_over = True
            self.status.configure(text=f"{w} wins! Click Reset to play again.")
            self.highlight_winline(w)
            return True
        if is_full(self.board):
            self.game_over = True
            self.status.configure(text="Draw! Click Reset to play again.")
            return True
        return False

    def highlight_winline(self, wmark: str):
        for a,b,c in LINES:
            if self.board[a] == self.board[b] == self.board[c] == wmark:
                for idx in (a,b,c):
                    x1,y1,x2,y2 = self.cell_bounds(idx)
                    pad = 18
                    self.canvas.create_rectangle(x1+pad, y1+pad, x2-pad, y2-pad,
                                                 outline=WIN_HIGHLIGHT, width=4)
                break

    def reset(self):
        self.board = [None]*9
        self.game_over = False
        self.canvas.delete("mark")
        self.canvas.delete("winline")
        self.status.configure(text="Your turn (X)")

    # --- Animation ---
    def animate_mark(self, idx: int, mark: str):
        # Animated draw: grow from small to full size in steps
        cx, cy = self.cell_center(idx)
        size_full = CELL//2 - PADDING
        steps = 8
        duration = 120  # ms total
        step_ms = max(10, duration // steps)

        if mark == 'O':
            # start very small circle, expand radius
            start_r = 2
            end_r = size_full
            ring = self.canvas.create_oval(cx-start_r, cy-start_r, cx+start_r, cy+start_r,
                                           outline=MARK_O, width=6, tags=("mark",))
            def grow(step=0):
                t = (step+1)/steps
                r = int(start_r + (end_r-start_r)*t)
                self.canvas.coords(ring, cx-r, cy-r, cx+r, cy+r)
                if step+1 < steps:
                    self.root.after(step_ms, grow, step+1)
            grow(0)
        else:  # 'X'
            # draw two lines, length grows
            arm = self.canvas.create_line(cx, cy, cx, cy, fill=MARK_X, width=6, capstyle="round", tags=("mark",))
            arm2 = self.canvas.create_line(cx, cy, cx, cy, fill=MARK_X, width=6, capstyle="round", tags=("mark",))
            half = size_full
            def grow(step=0):
                t = (step+1)/steps
                dx = int(half*t)
                dy = int(half*t)
                # line1: top-left to bottom-right
                self.canvas.coords(arm, cx-dx, cy-dy, cx+dx, cy+dy)
                # line2: bottom-left to top-right
                self.canvas.coords(arm2, cx-dx, cy+dy, cx+dx, cy-dy)
                if step+1 < steps:
                    self.root.after(step_ms, grow, step+1)
            grow(0)

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()