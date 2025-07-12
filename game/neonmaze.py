import tkinter as tk
import random
import time
from tkinter import messagebox

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 10,10
CELL_SIZE = WIDTH // COLS

WALL_COLOR = "#FF0000"
PATH_COLOR = "#222222"
GRID_COLOR = "#00FFFF"
PLAYER_COLOR = "#F0592E"
GOAL_COLOR = "#00FF66"
TRACE_COLOR = "#FFFF00"

class NeonMaze:
    def __init__ (self, root):
        self.root = root
        self.root.title("NEON MAZE!")
        self.root.configure(bg="#333")
    
        bar = tk.Frame(root, bg="#555", pady=5)
        bar.pack(fill="x")

        btn_style = {
            "bg" : "#222", #button color
            "fg" : GRID_COLOR, #text color
            "activebackground" : "#333", # color when button clicked
            "activeforeground" : "white", #text color when button clicked
            "relief" : "flat", 
            "font": ("Consolas" , 11, "bold"),
            "padx": 10, "pady": 5
        }

        tk.Button(bar , text="New Games" ,command=self.reset_maze, **btn_style).pack(side="left", padx=10)

        self.moves_label = tk.Label(bar, text="Moves: 0", fg="white", bg="black", font=("Consolas",11))
        self.moves_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(bar, text="Time: 00:00", fg="white", bg="black", font=("Consolas",11))
        self.timer_label.pack(side="left", padx=20)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)

        self.player_pos = [0, 0]
        self.moves = 0
        self.start_time = None
        self.trace = []

        self._generate_maze()
        self._draw()

        root.bind("<Key>", self._on_key)


    def _generate_maze(self):
        self.maze = [
            [0 if random.random() > 0.2 else 1 for _ in range(COLS)]
            for _ in range(ROWS)
        ]
        self.maze[0][0] = 0
        self.maze[ROWS-1][COLS-1] = 0

        self.player_pos = [0, 0]
        self.moves = 0
        self.trace = []
        self.start_time = time.time()

    def reset_maze(self):
        self._generate_maze() 
        self._draw()

    
    def _draw(self):
            self.canvas.delete("all")
            for i in range(ROWS):
                for j in range(COLS):
                    x1 = j * CELL_SIZE; y1 = i * CELL_SIZE
                    x2 = x1 + CELL_SIZE; y2 = y1 + CELL_SIZE
                    fill_color = PATH_COLOR if self.maze[i][j] == 0 else WALL_COLOR
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=GRID_COLOR)

            for (r, c) in self.trace:
                cx = c * CELL_SIZE + CELL_SIZE // 2; cy = r * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill=TRACE_COLOR, outline="")

            gx1 = (COLS-1)*CELL_SIZE+5; gy1 = (ROWS-1)*CELL_SIZE+5
            gx2 = COLS*CELL_SIZE-5; gy2 = ROWS*CELL_SIZE-5
            self.canvas.create_rectangle(gx1, gy1, gx2, gy2, fill=GOAL_COLOR, outline=GOAL_COLOR, width=3)

            r, c = self.player_pos
            px1 = c*CELL_SIZE+8; py1 = r*CELL_SIZE+8
            px2 = (c+1)*CELL_SIZE-8; py2 = (r+1)*CELL_SIZE-8
            self.canvas.create_oval(px1-3, py1-3, px2+3, py2+3, outline=PLAYER_COLOR, width=3)
            self.canvas.create_oval(px1, py1, px2, py2, fill=PLAYER_COLOR, outline="")

            self.moves_label.config(text=f"Moves: {self.moves}")
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")

            if self.player_pos == [ROWS-1, COLS-1]:
                self._win()


    def _win(self):
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        messagebox.showinfo("🎉 You Win! 🎉",
            f"Congratulations, you escaped the neon maze in {self.moves} moves\nand {mins:02d}:{secs:02d}!")
        self.reset_maze()

    def _on_key(self, e):
        dir_map = {"Up":(-1,0),"Down":(1,0),"Left":(0,-1),"Right":(0,1),
                   "w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1)}
        if e.keysym in dir_map:
            dx, dy = dir_map[e.keysym]
            nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and self.maze[nx][ny] == 0:
                self.trace.append(tuple(self.player_pos))
                self.player_pos = [nx, ny]
                self.moves += 1
            self._draw()


if __name__ == "__main__":
    root = tk.Tk()
    game = NeonMaze(root)
    root.mainloop()