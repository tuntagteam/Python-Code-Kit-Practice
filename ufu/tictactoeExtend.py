# ==========================================
# TIC TAC TOE GAME - ติก แทก โต้ว
# เกมที่ใช้เล่นระหว่างสองคนบนคีย์บอร์ด
# ==========================================

# ==========================================
# 1. นำเข้าไลบรารี และตั้งค่าเบื้องต้น
# ==========================================
import pygame  # นำเข้าไลบรารี pygame: ใช้สร้างเกมและกราฟิก

pygame.init()  # เริ่มต้นระบบ pygame: เตรียมทุกโมดูลของ pygame พร้อมใช้

# ==========================================
# 2. ตั้งค่าพื้นฐานเกม (Game Constants)
# ==========================================
WIDTH = 600  # ความกว้างหน้าจอ (พิกเซล)
HEIGHT = 700  # ความสูงหน้าจอ (พิกเซล) - เพิ่มจาก 600 เพื่อเผื่อแสดงข้อความ
CELL_SIZE = 200  # ขนาดแต่ละช่องในกระดาน (พิกเซล)

# สร้างหน้าต่างเกม: pygame.display.set_mode() คืนวัตถุ surface ที่ใช้วาดกราฟิก
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - ติก แทก โต้ว")  # ชื่อหน้าต่าง

# ==========================================
# 3. ตัวแปรสถานะเกม (Game State Variables)
# ==========================================
board = [  # สร้างกระดาน 3x3 - ใช้เก็บ "X", "O", หรือ "" (ว่าง)
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

current_player = "X"  # ผู้เล่นปัจจุบัน (เริ่มต้นให้ X เดินก่อน)
winner = None  # เก็บผู้ชนะ (None ถ้ายังไม่มี)
winning_line = None  # เก็บข้อมูลเส้นชนะ: (type, index) เช่น ("row", 0)
game_over = False  # สถานะเกม: True = เสร็จแล้ว, False = ยังเล่นอยู่
running = True  # ควบคุม main loop: True = ยังวิ่ง, False = ออกจากเกม

# ==========================================
# 4. ตั้งค่าฟอนต์ (Font Setup)
# ==========================================
# pygame.font.SysFont(name, size): สร้างฟอนต์จากระบบ None = ฟอนต์ default
mark_font = pygame.font.SysFont(None, 120)  # ฟอนต์ใหญ่สำหรับ X และ O
status_font = pygame.font.SysFont(None, 44)  # ฟอนต์กลางสำหรับข้อความสถานะ
hint_font = pygame.font.SysFont(None, 28)  # ฟอนต์เล็กสำหรับคำแนะนำปุ่ม

# ==========================================
# 5. ฟังก์ชันตรวจสอบผู้ชนะ
# ==========================================
def check_winner():
    """
    ตรวจสอบว่ามีใครชนะเกมแล้วหรือไม่
    คืนค่า: (ผู้ชนะ, ข้อมูลเส้นชนะ) หรือ (None, None) ถ้ายังไม่มีผู้ชนะ
    """
    # ตรวจสอบแถว (horizontal) - ถ้าทั้ง 3 ช่องในแถวเหมือนกัน
    for row in range(3):  # range(3) = [0, 1, 2]
        if board[row][0] != "" and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0], ("row", row)  # คืนผู้ชนะและชนิดเส้น

    # ตรวจสอบคอลัมน์ (vertical) - ถ้าทั้ง 3 ช่องในคอลัมน์เหมือนกัน
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col], ("col", col)

    # ตรวจสอบทแยงมุมลง - จากมุมบนซ้ายไปมุมล่างขวา
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], ("diag", 1)

    # ตรวจสอบทแยงมุมขึ้น - จากมุมล่างซ้ายไปมุมบนขวา
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], ("diag", 2)

    # ไม่มีผู้ชนะ
    return None, None

# ==========================================
# 6. ฟังก์ชันตรวจสอบเสมอ
# ==========================================
def check_draw():
    """
    ตรวจสอบว่ากระดานเต็มแล้วหรือไม่ (เสมอ)
    คืนค่า: True = เสมอ, False = ยังมีช่องว่าง
    """
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":  # ถ้ายังมีช่องว่าง
                return False
    return True  # ไม่มีช่องว่าง = เสมอ

# ==========================================
# 7. ฟังก์ชันรีเซ็ตเกม
# ==========================================
def reset_game():
    """
    เริ่มเกมใหม่: ล้างกระดานและรีเซ็ตตัวแปรทั้งหมด
    """
    global board, current_player, winner, winning_line, game_over
    # global = บอก Python ว่าจะแก้ไขตัวแปรระดับโปรแกรม ไม่ใช่สร้างตัวแปรใหม่

    board = [["", "", ""], ["", "", ""], ["", "", ""]]  # ล้างกระดาน
    current_player = "X"  # X เดินก่อน
    winner = None  # ล้างผู้ชนะ
    winning_line = None  # ล้างเส้นชนะ
    game_over = False  # เกมไม่จบ

# ==========================================
# 8. ฟังก์ชันวาดกระดาน
# ==========================================
def draw_board():
    """
    วาดกระดาน Tic Tac Toe: พื้นหลัง, ช่องสี่เหลี่ยม, เส้นแบ่ง
    """
    # pygame.display.fill(color): เติมพื้นหน้าจอด้วยสี (RGB tuple)
    screen.fill((245, 248, 255))  # พื้นหลัง: ฟ้าอ่อนมาก

    # pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
    # วาดสี่เหลี่ยม: surface = หน้าจอ, color = สี, rect = ตำแหน่ง (x, y, width, height)
    # border_radius = ความโค้งของมุม
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 560, 560), border_radius=25)

    # pygame.draw.line(surface, color, start_pos, end_pos, width)
    # วาดเส้น: start_pos = จุดเริ่ม, end_pos = จุดสิ้นสุด, width = ความหนา
    # เส้นแนวตั้ง (แบ่ง 3 คอลัมน์)
    for x in [200, 400]:  # เส้นที่ x=200 และ x=400
        pygame.draw.line(screen, (40, 40, 40), (x, 30), (x, 570), 6)

    # เส้นแนวนอน (แบ่ง 3 แถว)
    for y in [200, 400]:  # เส้นที่ y=200 และ y=400
        pygame.draw.line(screen, (40, 40, 40), (30, y), (570, y), 6)

# ==========================================
# 9. ฟังก์ชันวาด X และ O
# ==========================================
def draw_marks():
    """
    วาดเครื่องหมาย X (สีน้ำเงิน) และ O (สีส้ม) ลงบนกระดาน
    """
    for row in range(3):
        for col in range(3):
            mark = board[row][col]  # อ่านค่า: "", "X", หรือ "O"

            if mark != "":  # ถ้ามีเครื่องหมาย
                # กำหนดสี: X = น้ำเงิน, O = ส้ม
                color = (40, 100, 255) if mark == "X" else (255, 120, 40)

                # pygame.font.render(text, antialias, color): แปลงตัวอักษรเป็นภาพ
                # antialias = True = เรียบขอบ
                text = mark_font.render(mark, True, color)

                # get_rect(center=(x, y)): หาตำแหน่ง rect และจัดให้กลาง
                # col * CELL_SIZE + 100 = ตำแหน่ง x ของช่องนั้น + ออฟเซต
                text_rect = text.get_rect(center=(col * CELL_SIZE + 100, row * CELL_SIZE + 100))

                # pygame.Surface.blit(source, dest): วาดรูปต้นฉบับลงบนหน้าจอ
                # source = รูปที่วาด, dest = ตำแหน่งที่จะวาด
                screen.blit(text, text_rect)

# ==========================================
# 10. ฟังก์ชันวาดเส้นชนะ
# ==========================================
def draw_winning_line():
    """
    วาดเส้นแดงผ่านเครื่องหมายที่ชนะ (แถว, คอลัมน์, หรือทแยง)
    """
    if winning_line is None:  # ถ้ายังไม่มีเส้นชนะ
        return  # ออกจากฟังก์ชัน

    line_type, index = winning_line  # แยก: ชนิดเส้น (row/col/diag) และตำแหน่ง
    color = (255, 60, 60)  # สีแดง: (R, G, B)
    thickness = 12  # ความหนาเส้น (พิกเซล)

    if line_type == "row":  # ชนะแนวนอน
        y = index * CELL_SIZE + 100  # ตำแหน่ง y ของแถวนั้น
        pygame.draw.line(screen, color, (60, y), (540, y), thickness)

    elif line_type == "col":  # ชนะแนวตั้ง
        x = index * CELL_SIZE + 100  # ตำแหน่ง x ของคอลัมน์นั้น
        pygame.draw.line(screen, color, (x, 60), (x, 540), thickness)

    elif line_type == "diag" and index == 1:  # ชนะทแยงลง (บนซ้าย → ล่างขวา)
        pygame.draw.line(screen, color, (70, 70), (530, 530), thickness)

    elif line_type == "diag" and index == 2:  # ชนะทแยงขึ้น (ล่างซ้าย → บนขวา)
        pygame.draw.line(screen, color, (530, 70), (70, 530), thickness)

# ==========================================
# 11. ฟังก์ชันวาดข้อความสถานะ
# ==========================================
def draw_status():
    """
    วาดข้อความด้านล่าง: ผู้เล่นปัจจุบัน, ผู้ชนะ, หรือเสมอ + คำแนะนำปุ่ม
    """
    # กำหนดข้อความและสีตามสถานะเกม
    if not game_over:
        message = f"Turn: {current_player}"  # ผู้เล่นปัจจุบัน
        color = (30, 30, 30)  # สีเข้ม

    elif winner is not None:
        message = f"{winner} wins! Press R to restart"  # ผู้ชนะ
        color = (255, 60, 60)  # สีแดง

    else:
        message = "Draw! Press R to restart"  # เสมอ
        color = (255, 120, 40)  # สีส้ม

    # แปลงข้อความเป็นรูปภาพ
    text = status_font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, 635))  # จัดกลาง ที่ y=635
    screen.blit(text, text_rect)  # วาดลงบนหน้าจอ

    # คำแนะนำปุ่ม
    hint = hint_font.render("ESC = Quit  |  R = Restart", True, (120, 120, 120))
    hint_rect = hint.get_rect(center=(WIDTH // 2, 675))
    screen.blit(hint, hint_rect)

# ==========================================
# 12. MAIN GAME LOOP - วงจรหลักของเกม
# ==========================================
clock = pygame.time.Clock()  # pygame.time.Clock(): ควบคุมความเร็วเฟรม
FPS = 60  # เฟรมต่อวินาที: ระหว่าง 60 FPS

while running:
    clock.tick(FPS)  # จำกัดความเร็ว: อ่านเพิ่ม 1 ครั้งต่อ 1/60 วินาที

    # pygame.event.get(): อ่านเหตุการณ์ทั้งหมด (คลิก, กดปุ่ม, ปิดหน้าต่าง)
    for event in pygame.event.get():

        # ========== เหตุการณ์: ปิดหน้าต่าง ==========
        if event.type == pygame.QUIT:  # pygame.QUIT: ผู้ใช้กดปิดหน้าต่าง
            running = False

        # ========== เหตุการณ์: กดปุ่มบนคีย์บอร์ด ==========
        if event.type == pygame.KEYDOWN:  # pygame.KEYDOWN: กดปุ่มลง
            if event.key == pygame.K_ESCAPE:  # pygame.K_ESCAPE: ปุ่ม ESC
                running = False

            if event.key == pygame.K_r:  # pygame.K_r: ปุ่ม R
                reset_game()

        # ========== เหตุการณ์: คลิกเมาส์ ==========
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # pygame.MOUSEBUTTONDOWN: คลิกเมาส์ (ระหว่างเล่น)
            x, y = pygame.mouse.get_pos()  # pygame.mouse.get_pos(): อ่านตำแหน่งเมาส์

            if y < 600:  # เช็คคลิกอยู่ในพื้นที่กระดาน (ไม่ใช่ข้อความด้านล่าง)
                col = x // CELL_SIZE  # คำนวณคอลัมน์ (0, 1, หรือ 2)
                row = y // CELL_SIZE  # คำนวณแถว (0, 1, หรือ 2)

                # กำหนด row, col ถ้าเกินขอบเขต ให้อยู่ในช่วง 0-2
                row = min(row, 2)
                col = min(col, 2)

                if board[row][col] == "":  # ถ้าช่องว่าง
                    board[row][col] = current_player  # เดินหมากของผู้เล่นปัจจุบัน

                    winner, winning_line = check_winner()  # ตรวจสอบผู้ชนะ

                    if winner is not None:  # มีผู้ชนะ
                        game_over = True

                    elif check_draw():  # เสมอ
                        game_over = True

                    else:  # เกมยังไม่จบ - สลับผู้เล่น
                        current_player = "O" if current_player == "X" else "X"

    # ========== วาดเกม ==========
    draw_board()  # วาดกระดาน
    draw_marks()  # วาด X และ O
    draw_winning_line()  # วาดเส้นชนะ (ถ้ามี)
    draw_status()  # วาดข้อความสถานะ

    # pygame.display.update(): อัปเดตหน้าจอแสดงผลล่าสุด
    pygame.display.update()

# ==========================================
# 13. ปิดเกม
# ==========================================
pygame.quit()  # pygame.quit(): ปิด pygame ให้เรียบร้อย