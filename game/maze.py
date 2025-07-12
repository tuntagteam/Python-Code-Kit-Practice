import tkinter as tk  # เรียกใช้งานไลบรารี tkinter เพื่อสร้าง GUI (Graphical User Interface)
import random         # นำเข้าโมดูล random สำหรับสุ่มค่าที่ใช้สร้างกำแพงหรือทางเดิน
import time           # นำเข้าโมดูล time เพื่อจับเวลาเริ่มและคำนวณเวลาที่ผ่านไป
from tkinter import messagebox  # นำเข้า widget สำหรับแสดงกล่องข้อความแจ้งเตือน (modal)

# === CONFIGURATION ===
WIDTH, HEIGHT = 400, 400       # กำหนดขนาดหน้าต่างเกม: ความกว้างและความสูงเป็นพิกเซล
# Q: ทำไมเราต้องแยก CONFIGURATION ออกมา? เพื่ออะไร?
# A: เพื่อความยืดหยุ่นในการปรับค่าต่างๆ เช่น ขนาด สี หรืออัตราการสุ่ม ได้ง่าย ไม่ต้องแก้โค้ดหลายจุด

ROWS, COLS = 10, 10            # กำหนดจำนวนแถวและคอลัมน์ของตารางเขาวงกต
CELL_SIZE = WIDTH // COLS      # คำนวณขนาดของแต่ละเซลล์โดยหารความกว้างด้วยจำนวนคอลัมน์

WALL_COLOR   = "#FF0000"  # สีแดงสำหรับกำแพง (ไม่สามารถเดินผ่านได้)
PATH_COLOR   = "#222222"  # สีเข้มสำหรับทางเดิน (สามารถเดินผ่านได้)
GRID_COLOR   = "#00FFFF"  # สีฟ้าอมเขียวสำหรับขอบกริด เพื่อให้เกิดเอฟเฟกต์ Neon
PLAYER_COLOR = "#FF0055"  # สีชมพูสดสำหรับผู้เล่น
GOAL_COLOR   = "#00FF66"  # สีเขียวสดสำหรับจุดหมายปลายทาง
TRACE_COLOR  = "#FFFF00"  # สีเหลืองสดสำหรับร่องรอยการเดิน (trail)

# Q: ทำไมเราต้องกำหนดสีและขนาดต่างๆ ใน CONFIGURATION?
# A: เพื่อให้ปรับแต่งค่าพารามิเตอร์ได้ง่ายโดยไม่ต้องแก้หลายจุด ช่วยให้โค้ดอ่านง่ายและลดข้อผิดพลาดเมื่อเปลี่ยนแปลงค่า

# === CLASS DEFINITION ===
class NeonMaze:
    def __init__(self, root):  # เมธอดเริ่มต้น รับออบเจกต์หน้าต่างหลักจาก tkinter
        self.root = root  # เก็บ reference ของหน้าต่างหลัก
        self.root.title("⚡ Neon Maze Explorer ⚡")  # ตั้งชื่อหน้าต่างโปรแกรม
        self.root.configure(bg="black")  # ตั้งพื้นหลังให้เป็นสีดำ เพื่อเน้น UI แบบ Neon

        # --- TOOLBAR ---
        bar = tk.Frame(root, bg="black", pady=5)  # สร้างเฟรมแนวนอนสำหรับวางปุ่มและป้ายข้อมูล
        bar.pack(fill="x")  # ขยายเฟรมเต็มความกว้างหน้าต่าง

        btn_style = {  # กำหนดสไตล์ปุ่มใช้ซ้ำได้
            "bg": "#111",  # สีพื้นปุ่ม
            "fg": GRID_COLOR,  # สีข้อความบนปุ่ม
            "activebackground": "#222",  # สีพื้นเมื่อปุ่มถูกกด
            "activeforeground": "white",  # สีข้อความเมื่อปุ่มถูกกด
            "relief": "flat",  # ไม่มีขอบนูน
            "font": ("Consolas", 11, "bold"),  # ฟอนต์และขนาด
            "padx": 10, "pady": 5  # ระยะขอบภายในปุ่ม
        }
        tk.Button(bar, text="🔄 New Maze", command=self.reset_maze, **btn_style).pack(side="left", padx=10)
        # Q: ปุ่ม New Maze มีไว้ทำอะไร และ command ทำงานยังไง?
        # A: ใช้สร้างเขาวงกตใหม่โดยเรียกเมธอด reset_maze เมื่อคลิก, command=self.reset_maze คือการส่ง reference ของฟังก์ชันไปให้ Tkinter เรียกเมื่อเกิด event คลิก

        self.moves_label = tk.Label(bar, text="Moves: 0", fg="white", bg="black", font=("Consolas",11))
        self.moves_label.pack(side="left", padx=20)  # ป้ายแสดงจำนวนครั้งที่ผู้เล่นเคลื่อนที่

        self.timer_label = tk.Label(bar, text="Time: 00:00", fg="white", bg="black", font=("Consolas",11))
        self.timer_label.pack(side="left", padx=20)  # ป้ายแสดงเวลาที่ผ่านไป

        # --- CANVAS ---
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)  # พื้นที่สำหรับวาดเขาวงกต ผู้เล่น และจุดหมาย

        # --- INITIAL STATE ---
        self.player_pos = [0, 0]  # ตำแหน่งผู้เล่นเริ่มต้นที่มุมบนซ้าย ([row, col])
        self.moves = 0  # ตัวนับการเคลื่อนที่ตั้งค่าเริ่มต้นเป็น 0
        self.start_time = None  # เก็บเวลาที่เริ่มเกม จะกำหนดใน _generate_maze
        self.trace = []  # รายการเก็บร่องรอยการเคลื่อนที่ก่อนหน้า

        self._generate_maze()  # สร้างเขาวงกตใหม่และตั้งค่า state เริ่มต้น
        self._draw()  # วาดสถานะเริ่มต้นบน canvas

        root.bind("<Key>", self._on_key)  # ผูก event กดคีย์บอร์ดกับเมธอด _on_key
        # Q: ถ้าไม่ bind คีย์ จะขยับผู้เล่นยังไง?
        # A: จะไม่สามารถจับ event key press ได้ ผู้เล่นกดปุ่มแล้วจะไม่เกิดการเคลื่อนที่

    def _generate_maze(self):  # สร้างเขาวงกตและรีเซ็ต state
        self.maze = [
            [0 if random.random() > 0.2 else 1 for _ in range(COLS)]  # สุ่มกำแพง (1) หรือทางเดิน (0) ด้วยโอกาส 20% เป็นกำแพง
            for _ in range(ROWS)
        ]
        self.maze[0][0] = 0  # บังคับ cell แรกเป็นทางเดิน
        self.maze[ROWS-1][COLS-1] = 0  # บังคับ cell สุดท้ายเป็นทางเดิน

        self.player_pos = [0, 0]  # รีเซ็ตตำแหน่งผู้เล่น
        self.moves = 0  # รีเซ็ตตัวนับ moves
        self.trace = []  # เคลียร์ร่องรอยเดิม
        self.start_time = time.time()  # จับเวลาเริ่มเกมใหม่
        # Q: ถ้าไม่ตั้ง start_time ใหม่ จะจับเวลาอย่างไร?
        # A: start_time จะคงค่าจากเกมก่อนหน้า ทำให้ timer แสดงค่าผิดพลาด เป็นเวลาสะสมไม่ใช่เวลาเกมนี้

    def reset_maze(self):  # เมธอดเรียกเมื่อกดปุ่ม New Maze
        self._generate_maze()  # สร้างและตั้งค่าใหม่
        self._draw()  # วาดสถานะใหม่

    def _draw(self):  # วาดภาพทั้งหมดบน canvas
        self.canvas.delete("all")  # ลบวัตถุก่อนหน้า

        # วาด grid ของเขาวงกต
        for i in range(ROWS):
            for j in range(COLS):
                x1 = j * CELL_SIZE; y1 = i * CELL_SIZE  # พิกัดซ้ายบนของ cell
                x2 = x1 + CELL_SIZE; y2 = y1 + CELL_SIZE  # พิกัดขวาล่าง
                fill_color = PATH_COLOR if self.maze[i][j] == 0 else WALL_COLOR  # เลือกสีตามค่า maze
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=GRID_COLOR)
                # Q: outline กับ fill ต่างกันอย่างไร?
                # A: fill คือสีภายใน shape, outline คือสีเส้นขอบ ช่วยให้เห็นขอบเซลล์ชัดเจน

        # วาดร่องรอยการเดิน (trail)
        for (r, c) in self.trace:
            cx = c * CELL_SIZE + CELL_SIZE // 2; cy = r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill=TRACE_COLOR, outline="")

        # วาดจุดหมายปลายทาง
        gx1 = (COLS-1)*CELL_SIZE+5; gy1 = (ROWS-1)*CELL_SIZE+5
        gx2 = COLS*CELL_SIZE-5; gy2 = ROWS*CELL_SIZE-5
        self.canvas.create_rectangle(gx1, gy1, gx2, gy2, fill=GOAL_COLOR, outline=GOAL_COLOR, width=3)

        # วาดผู้เล่น (glow + core)
        r, c = self.player_pos
        px1 = c*CELL_SIZE+8; py1 = r*CELL_SIZE+8
        px2 = (c+1)*CELL_SIZE-8; py2 = (r+1)*CELL_SIZE-8
        self.canvas.create_oval(px1-3, py1-3, px2+3, py2+3, outline=PLAYER_COLOR, width=3)
        self.canvas.create_oval(px1, py1, px2, py2, fill=PLAYER_COLOR, outline="")

        # อัปเดตป้าย moves และ timer
        self.moves_label.config(text=f"Moves: {self.moves}")  # แสดง count moves ล่าสุด
        elapsed = int(time.time() - self.start_time)  # คำนวณเวลาที่ผ่านไป
        mins, secs = divmod(elapsed, 60)
        self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")  # แสดง timer

        # ตรวจ victory condition
        if self.player_pos == [ROWS-1, COLS-1]:  # ถ้าถึง goal
            self._win()  # เรียกเมธอดเมื่อชนะ

    def _win(self):  # เมื่อผู้เล่นชนะ
        elapsed = int(time.time() - self.start_time)  # เวลา elapsed
        mins, secs = divmod(elapsed, 60)
        messagebox.showinfo("🎉 You Win! 🎉",
            f"Congratulations, you escaped the neon maze in {self.moves} moves\nand {mins:02d}:{secs:02d}!")
        # Q: ถ้าไม่ reset maze ใหม่หลัง win จะเกิดอะไรขึ้น?
        # A: ผู้เล่นจะติดอยู่ที่ goal หรือเกมค้าง ไม่สามารถเล่นต่อได้อัตโนมัติ
        self.reset_maze()  # สร้าง maze ใหม่ทันที

    def _on_key(self, e):  # จัดการ event กดปุ่มคีย์บอร์ด
        dir_map = {"Up":(-1,0),"Down":(1,0),"Left":(0,-1),"Right":(0,1),
                   "w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1)}  # แผนที่ key->vector
        if e.keysym in dir_map:
            dx, dy = dir_map[e.keysym]
            nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
            # ตรวจขอบเขตและกำแพง
            if 0 <= nx < ROWS and 0 <= ny < COLS and self.maze[nx][ny] == 0:
                self.trace.append(tuple(self.player_pos))  # เก็บตำแหน่งเดิม
                self.player_pos = [nx, ny]
                self.moves += 1  # เพิ่ม count moves
            self._draw()  # วาดสถานะใหม่
            # Q: ถ้าไม่ตรวจเงื่อนไขขอบเขต จะเกิดอะไร? อธิบายข้อผิดพลาดที่อาจเกิดขึ้น
            # A: อาจเกิด IndexError หรือโปรแกรมหยุดทำงานเพราะเข้าถึงตำแหน่งนอกตาราง

if __name__ == "__main__":
    root = tk.Tk()  # สร้างหน้าต่างหลักของ tkinter
    game = NeonMaze(root)  # สร้างอินสแตนซ์เกม
    root.mainloop()  # เริ่ม main loop รอและแจกจ่าย event
    # Q: mainloop() ทำอะไร มีความสำคัญอย่างไร?
    # A: คอยรับและจัดการ event (เช่น key press, button click) ให้ GUI ตอบสนอง หากไม่รัน loop จะไม่เกิดการอัปเดตหรือรับ input
