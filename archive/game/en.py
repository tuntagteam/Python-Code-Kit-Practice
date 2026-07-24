import tkinter as tk
import random, time
from tkinter import messagebox

WIDTH, HEIGHT, ROWS, COLS = 450, 450, 7, 7
CELL_SIZE = WIDTH // COLS
COLORS = {
    "wall": "#FF2E63", "path": "#1A1A1D", "grid": "#08D9D6",
    "player": "#F0592E", "goal": "#3EC70B", "trace": "#FCE38A",
    "bg": "#0D0D0D", "panel": "#111", "text1": "#08D9D6", "text2": "#FF2E63"
}

class NeonMaze:
    def __init__(self, root):
        self.root, self.moves, self.trace = root, 0, []
        root.title("⚡ Neon Maze ⚡")
        root.configure(bg=COLORS["bg"])

        bar = tk.Frame(root, bg=COLORS["panel"])
        bar.pack(fill="x", padx=12, pady=8)
        style = {"bg":COLORS["panel"], "fg":COLORS["text1"],
                 "font":("Consolas",12,"bold"), "padx":10, "pady":5}
        tk.Button(bar, text="🌀 New Maze", command=self.reset_maze, **style).pack(side="left", padx=12)
        self.moves_label = tk.Label(bar, text="Moves: 0", **style)
        self.timer_label = tk.Label(bar, text="Time: 00:00", fg=COLORS["text2"], bg=COLORS["panel"], font=("Consolas",12,"bold"))
        self.moves_label.pack(side="left", padx=20); self.timer_label.pack(side="left", padx=20)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=15)

        root.bind("<Key>", self._on_key)
        self.reset_maze()

    def reset_maze(self):
        self.maze = [[0 if random.random()>0.2 else 1 for _ in range(COLS)] for _ in range(ROWS)]
        self.maze[0][0] = self.maze[ROWS-1][COLS-1] = 0
        self.player_pos, self.moves, self.trace, self.start_time = [0,0], 0, [], time.time()
        self._draw()

    def _draw(self):
        c, (pr, pc) = self.canvas, self.player_pos
        c.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                x1, y1, x2, y2 = j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE
                fill = COLORS["path"] if self.maze[i][j]==0 else COLORS["wall"]
                c.create_rectangle(x1,y1,x2,y2, fill=fill, outline=COLORS["grid"])
        for r, cl in self.trace:
            cx, cy = cl*CELL_SIZE+CELL_SIZE//2, r*CELL_SIZE+CELL_SIZE//2
            c.create_oval(cx-4,cy-4,cx+4,cy+4, fill=COLORS["trace"], outline="")
        gx, gy = (COLS-1)*CELL_SIZE, (ROWS-1)*CELL_SIZE
        c.create_rectangle(gx+5,gy+5,gx+CELL_SIZE-5,gy+CELL_SIZE-5, fill=COLORS["goal"], outline=COLORS["goal"], width=3)
        px1, py1, px2, py2 = pc*CELL_SIZE+8, pr*CELL_SIZE+8, (pc+1)*CELL_SIZE-8, (pr+1)*CELL_SIZE-8
        c.create_oval(px1-4,py1-4,px2+4,py2+4, outline=COLORS["wall"], width=4)
        c.create_oval(px1,py1,px2,py2, fill=COLORS["player"], outline="")

        elapsed = int(time.time()-self.start_time)
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.timer_label.config(text=f"Time: {elapsed//60:02d}:{elapsed%60:02d}")
        if self.player_pos == [ROWS-1,COLS-1]: self._win()

    def _win(self):
        e = int(time.time()-self.start_time)
        messagebox.showinfo("🎉 You Win!", f"Escaped in {self.moves} moves\nand {e//60:02d}:{e%60:02d}!")
        self.reset_maze()

    def _on_key(self, e):
        dirs = {"Up":(-1,0),"Down":(1,0),"Left":(0,-1),"Right":(0,1),
                "w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1)}
        if e.keysym in dirs:
            dx, dy = dirs[e.keysym]
            nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
            if 0<=nx<ROWS and 0<=ny<COLS and self.maze[nx][ny]==0:
                self.trace.append(tuple(self.player_pos))
                self.player_pos, self.moves = [nx,ny], self.moves+100
            self._draw()

if __name__=="__main__":
    root = tk.Tk()
    NeonMaze(root)
    root.mainloop()