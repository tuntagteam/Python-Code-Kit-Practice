import pygame
import random

# ตั้งค่าพื้นฐานของเกม
WIDTH, HEIGHT = 600, 700  # กำหนดความกว้างและความสูงของหน้าจอเกม
FPS = 60  # กำหนดจำนวนเฟรมต่อวินาที เพื่อควบคุมความเร็วของเกมให้คงที่

# เริ่มต้นใช้งาน pygame
pygame.init()  # เริ่มต้นโมดูล pygame เพื่อเตรียมใช้งาน
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # สร้างหน้าต่างเกมขนาด WIDTH x HEIGHT
pygame.display.set_caption("🎮 Catch the Magic Ball")  # ตั้งชื่อหน้าต่างเกม
clock = pygame.time.Clock()  # สร้างตัวจับเวลาเพื่อควบคุม FPS ของเกม

# ฟอนต์ที่ใช้สำหรับแสดงคะแนนและข้อความ
font = pygame.font.SysFont("Arial", 28)  # สร้างฟอนต์ขนาด 28 สำหรับข้อความทั่วไป
big_font = pygame.font.SysFont("Arial", 48, bold=True)  # สร้างฟอนต์ขนาดใหญ่ 48 ตัวหนาสำหรับข้อความสำคัญ

# กำหนดขนาดและตำแหน่งของผู้เล่น
PLAYER_WIDTH = 80  # กำหนดความกว้างของผู้เล่น
PLAYER_HEIGHT = 20  # กำหนดความสูงของผู้เล่น
player_x = WIDTH // 2 - PLAYER_WIDTH // 2  # กำหนดตำแหน่ง x เริ่มต้นของผู้เล่นให้อยู่ตรงกลางหน้าจอ
player_y = HEIGHT - 60  # กำหนดตำแหน่ง y ของผู้เล่นให้อยู่ด้านล่างของหน้าจอ
player_speed = 8  # กำหนดความเร็วในการเคลื่อนที่ของผู้เล่น

# ตัวแปรสำหรับลูกบอลทั้งหมดในเกม
balls = []  # สร้างลิสต์เก็บลูกบอลที่กำลังตกลงมาในเกม
misses = 0  # ตัวแปรเก็บจำนวนครั้งที่ผู้เล่นพลาดไม่รับลูกบอล
max_miss = 3  # กำหนดจำนวนครั้งที่พลาดได้ก่อนเกมจะจบ
score = 0  # ตัวแปรเก็บคะแนนของผู้เล่น

# ฟังก์ชันสำหรับสร้างลูกบอลใหม่
def spawn_ball():
    # สร้างลูกบอลใหม่โดยกำหนดตำแหน่ง x แบบสุ่มภายในหน้าจอ
    # เริ่มต้นตำแหน่ง y อยู่ด้านบนของหน้าจอ (-20 เพื่อให้เริ่มนอกหน้าจอ)
    # กำหนดรัศมีลูกบอล ขนาดและสีสุ่มระหว่างสีฟ้าหรือสีทอง (item)
    # กำหนดความเร็วลูกบอลแบบสุ่มเพื่อเพิ่มความท้าทาย
    return {
        "x": random.randint(20, WIDTH - 20),  # ตำแหน่งแนวนอนแบบสุ่ม ไม่ให้ติดขอบ
        "y": -20,  # เริ่มต้นที่ด้านบนหน้าจอ (ข้างนอกหน้าจอ)
        "radius": 20,  # ขนาดรัศมีลูกบอล
        "color": random.choice([(173, 216, 230), (255, 215, 0)]),  # สีฟ้าหรือสีทอง
        "speed": random.randint(4, 7)  # ความเร็วในการตกของลูกบอล
    }

# เพิ่มลูกบอลเริ่มต้นเข้ามาหนึ่งลูก เพื่อให้เกมเริ่มมีลูกบอลตก
balls.append(spawn_ball())
game_over = False  # ตัวแปรสถานะเกมว่าเกมยังไม่จบ

# เพิ่มตัวแปรสถานะสำหรับหน้าเริ่มเกม
show_start_screen = True

# สร้างปุ่ม Start
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 80)

# ลูปหลักของเกม
running = True  # ตัวแปรควบคุมลูปเกมให้ทำงานต่อเนื่อง
while running:
    clock.tick(FPS)  # จำกัดความเร็วลูปให้อยู่ที่ FPS ที่กำหนด เพื่อความสมูทของเกม
    screen.fill((25, 10, 40))  # ล้างหน้าจอด้วยสีพื้นหลังโทนเข้ม (สีม่วงเข้ม)

    # ตรวจสอบเหตุการณ์จากผู้ใช้ เช่น การกดปิดหน้าจอ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ถ้าผู้ใช้กดปิดหน้าต่าง
            running = False  # ออกจากลูปเกมเพื่อปิดเกม

        # เช็คคลิกบนปุ่ม start
        if show_start_screen and event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                show_start_screen = False  # เริ่มเกมเมื่อกดปุ่ม

    if show_start_screen:
        # วาดปุ่ม Start
        pygame.draw.rect(screen, (0, 200, 0), start_button)
        start_text = big_font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 24))
    elif not game_over:
        # ตรวจสอบการกดปุ่มลูกศรซ้าย/ขวา เพื่อควบคุมตัวละคร
        keys = pygame.key.get_pressed()  # รับสถานะการกดปุ่มทั้งหมดในขณะนี้
        if keys[pygame.K_LEFT] and player_x > 0:  # ถ้ากดปุ่มซ้ายและผู้เล่นยังไม่ชนขอบซ้าย
            player_x -= player_speed  # เลื่อนผู้เล่นไปทางซ้ายตามความเร็วที่กำหนด
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:  # ถ้ากดปุ่มขวาและผู้เล่นยังไม่ชนขอบขวา
            player_x += player_speed  # เลื่อนผู้เล่นไปทางขวาตามความเร็วที่กำหนด

        # สุ่มเพิ่มลูกบอลใหม่แบบสุ่ม เมื่อยังไม่เกินจำนวนสูงสุด 5 ลูก
        if random.randint(0, 100) < 2 and len(balls) < 5:
            balls.append(spawn_ball())  # สร้างลูกบอลใหม่และเพิ่มเข้าไปในลิสต์ลูกบอล

        # วาดผู้เล่นเป็นสี่เหลี่ยมที่ตำแหน่ง player_x, player_y
        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)  # สร้างกรอบสี่เหลี่ยมผู้เล่น
        pygame.draw.rect(screen, (255, 255, 255), player_rect)  # วาดสี่เหลี่ยมสีขาวบนหน้าจอ

        # อัปเดตตำแหน่งลูกบอลและตรวจจับการชนกับผู้เล่น
        for ball in balls[:]:  # ใช้ [:] เพื่อทำสำเนาลิสต์ป้องกันปัญหาเวลาลบลูกบอลขณะวนลูป
            ball["y"] += ball["speed"]  # เลื่อนลูกบอลลงตามความเร็วที่กำหนด
            pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball["radius"])  # วาดลูกบอลบนหน้าจอ

            # สร้างกรอบสี่เหลี่ยมรอบลูกบอลเพื่อใช้ตรวจสอบการชน
            ball_rect = pygame.Rect(ball["x"] - ball["radius"], ball["y"] - ball["radius"],
                                    ball["radius"] * 2, ball["radius"] * 2)

            # ถ้าเกิดการชนระหว่างลูกบอลกับผู้เล่น
            if player_rect.colliderect(ball_rect):
                if ball["color"] == (255, 215, 0):  # ถ้าลูกบอลเป็นสีทอง (item พิเศษ)
                    score += 3  # เพิ่มคะแนน 3 แต้ม
                else:
                    score += 1  # ลูกบอลธรรมดาเพิ่มคะแนน 1 แต้ม
                balls.remove(ball)  # เอาบอลออกจากลิสต์หลังชนเพื่อไม่ให้ตรวจซ้ำ

            # ถ้าบอลตกเลยขอบล่างของหน้าจอ ถือว่าเป็นการพลาด
            elif ball["y"] > HEIGHT:
                balls.remove(ball)  # เอาบอลออกจากลิสต์เพราะหลุดหน้าจอ
                misses += 1  # เพิ่มจำนวนครั้งที่พลาด
                if misses >= max_miss:  # ถ้าพลาดเกินจำนวนที่กำหนด
                    game_over = True  # เปลี่ยนสถานะเกมเป็นจบเกม

        # แสดงคะแนนปัจจุบันและจำนวนครั้งที่พลาดบนหน้าจอ
        score_text = font.render(f"Scores: {score}", True, (255, 255, 0))  # สร้างข้อความคะแนนสีเหลือง
        miss_text = font.render(f"Missed: {misses}/{max_miss}", True, (255, 100, 100))  # ข้อความจำนวนครั้งพลาดสีแดงอมชมพู
        screen.blit(score_text, (20, 20))  # วางข้อความคะแนนที่มุมซ้ายบน
        screen.blit(miss_text, (20, 60))  # วางข้อความจำนวนพลาดด้านล่างคะแนนเล็กน้อย

    else:  # ถ้าเกมจบแล้ว
        # แสดงข้อความ GAME OVER พร้อมคะแนนสุดท้ายตรงกลางหน้าจอ
        over_text = big_font.render("🛑 GAME OVER", True, (255, 0, 0))  # ข้อความใหญ่สีแดงแจ้งจบเกม
        final_score = font.render(f"Scores: {score}", True, (255, 255, 255))  # คะแนนสุดท้ายสีขาว
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))  # วางข้อความ GAME OVER ตรงกลางแนวนอนและเลื่อนขึ้นเล็กน้อย
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 10))  # วางคะแนนตรงกลางหน้าจอด้านล่างข้อความ GAME OVER

    pygame.display.flip()  # อัปเดตหน้าจอทั้งหมดเพื่อแสดงผลการวาดในแต่ละเฟรม

# จบ pygame และปิดหน้าต่างเกม
pygame.quit()  # ปิด pygame และคืนทรัพยากรทั้งหมดที่ใช้งานไป