# ======================================================================
#  🎮 หมากฮอสไทย — กฎมาตรฐานไทยเต็มรูปแบบ
#  เขียนด้วย Python + Pygame
#  comment แบบสอนเด็ก ทุกบรรทัด + อุปมาอุปไมย
# ======================================================================
#
#  📖 กฎที่ใช้ (จากกติกาสมาคมหมากฮอสไทย):
#  ──────────────────────────────────────────
#
#  🟫 กระดานและการวาง:
#     • กระดาน 8×8  เล่นบนช่องสีเข้มเท่านั้น
#     • แต่ละฝ่ายมี 8 ตัว  วางแบบซิกแซกใน 2 แถวสุดท้าย
#
#  ♟️ การเดิน:
#     • เดินทแยงไปข้างหน้าทีละ 1 ช่อง
#     • "กิน" = กระโดดข้ามหมากฝ่ายตรงข้ามที่อยู่ติดกัน
#       (ต้องมีช่องว่างอยู่ด้านหลัง)
#     • หลังกินแล้ว → สลับตาทันที  (หมากธรรมดากินได้ครั้งเดียวต่อตา)
#
#  ⚠️ กฎการบังคับกิน (กฎสำคัญของไทย!):
#     • ปกติ: เลือกได้ว่าจะกินหรือเดินปกติ
#     • "บังคับ": ถ้าฝ่าย A ประกาศบังคับ → ฝ่าย B ต้องกินทันที
#     • ในโปรแกรมนี้: กดปุ่ม F เพื่อประกาศ "บังคับกิน" ฝ่ายตรงข้าม
#       (ถ้ากำลังเล่นอยู่และมีหมากที่กินได้)
#
#  👑 ดาม (King):
#     • เดินถึงฝั่งตรงข้าม → กลายเป็นดาม
#     • ดามเดินได้ทุก 4 ทิศ ทแยง ไกลไม่จำกัด
#     • ดามกินได้หลายตัวต่อเนื่องในตาเดียว
#
#  🏆 ชนะ:
#     1. กินหมากฝ่ายตรงข้ามจนหมด
#     2. ทำให้ฝ่ายตรงข้ามเดินไม่ได้
#     3. ฝ่ายตรงข้ามยอมแพ้        (กด S)
#     4. ฝ่ายตรงข้ามฝ่าฝืนกฎ      (กด V — Violation)
#     5. ฝ่ายตรงข้ามหมดเวลา
#
#  🤝 เสมอ:
#     • เดินซ้ำท่าเดิมเกิน 3 ครั้ง
#     • เดินไป-กลับยืดเยื้อ
#     • กรรมการตัดสิน (กด D — Draw)
#
#  ⏱️ เวลา (กฎไทย):
#     • 2 นาที/ตา  หมดเวลา = แพ้
#     • ขอพักได้ 2 ครั้ง × 5 นาที  หรือ  1 ครั้ง × 10 นาที  (กด T)
# ======================================================================

# ── นำเข้าเครื่องมือ ─────────────────────────────────────────────────
# "import X" = หยิบเครื่องมือ X เข้ามาใช้
# เปรียบเหมือน: ก่อนทำอาหาร ต้องหยิบหม้อ กะทะ มีด มาก่อน
import pygame               # ชุดเครื่องมือสร้างเกม 2D
import sys                  # สั่งปิดโปรแกรม
import math                 # คณิตศาสตร์ (sin, cos)
import time                 # นับเวลา
from collections import deque  # คิวเก็บประวัติการเดิน

# ── ค่าคงที่ ──────────────────────────────────────────────────────────
# ค่าคงที่ = ค่าที่ไม่เปลี่ยนตลอดโปรแกรม
# เขียนตัวพิมพ์ใหญ่ = สัญญาณ "ห้ามแก้ไข"
# เปรียบเหมือน: ขนาดสนามฟุตบอล — ตายตัว ทุกคนต้องทำตาม
WINDOW_W  = 840
WINDOW_H  = 1010    # 840 กระดาน + 170 แถบล่าง
BOARD_PX  = 840
ROWS      = 8
COLS      = 8
SQ        = BOARD_PX // COLS   # ขนาดช่อง = 105 pixel
R_PIECE   = SQ // 2 - 9        # รัศมีหมาก = 43 pixel
R_KING    = R_PIECE // 2       # รัศมีดาวดาม

# เวลา (กฎไทย)
TURN_TIME         = 120   # 2 นาที/ตา
TIMEOUT_DUR       = 300   # พัก 5 นาที
MAX_TIMEOUTS      = 2     # ขอพักได้สูงสุด 2 ครั้ง
REPEAT_DRAW_LIMIT = 3     # เดินซ้ำเกินนี้ = เสมอ

# ── สี (R, G, B) ──────────────────────────────────────────────────────
# แต่ละค่า 0-255  เปรียบเหมือน: ผสมสีจากสีแม่ 3 สี
C_LIGHT   = (235, 210, 165)   # ช่องสว่าง
C_DARK    = (155,  95,  45)   # ช่องมืด
C_RED     = (215,  40,  40)   # หมากแดง
C_RED_D   = (120,  10,  10)   # ขอบแดงเข้ม
C_BLK     = ( 45,  45,  45)   # หมากดำ
C_BLK_D   = (  5,   5,   5)   # ขอบดำเข้ม
C_SEL     = (255, 215,   0)   # เหลืองทอง (หมากเลือก)
C_HINT    = ( 70, 200,  70)   # เขียว (เดินได้)
C_JUMP    = (255,  90,  40)   # ส้มแดง (กินได้)
C_FORCE   = (255,  30,  30)   # แดงสด (บังคับกินอยู่!)
C_TIMEOUT = (255,  50,  50)   # แดง (เวลาเกือบหมด)
C_PAUSE   = ( 80, 160, 255)   # ฟ้า (พัก)
C_BG      = ( 22,  16,   8)   # พื้นหลัง
C_PANEL   = ( 14,  10,   4)   # แถบล่าง
C_GOLD    = (255, 205,   0)   # ทอง
C_WHITE   = (255, 255, 255)
C_GRAY    = (145, 145, 155)
C_WARN    = (255, 140,   0)   # ส้ม
C_GREEN   = ( 60, 200,  80)   # เขียวสด
C_YELLOW  = (255, 220,   0)   # เหลือง

# ── รหัสผู้เล่น ──────────────────────────────────────────────────────
# ใช้ตัวเลขแทนผู้เล่น เปรียบเหมือน เบอร์เสื้อนักกีฬา
RED   = 1   # หมากแดง เดินขึ้น (row ลด)
BLACK = 2   # หมากดำ  เดินลง   (row เพิ่ม)
EMPTY = 0   # ช่องว่าง


# ── ฟอนต์ ─────────────────────────────────────────────────────────────
# ใช้ฟอนต์ที่รองรับภาษาไทยจริง แทนการเรียก Arial ตรงๆ
THAI_FONT_NAMES = (
    "leelawadeeui",
    "tahoma",
    "nirmalaui",
    "segoeui",
    "microsoftsansserif",
    "arial",
)
MONO_FONT_NAMES = ("consolas", "couriernew", "courier")


def make_font(size, bold=False, mono=False):
    if not pygame.font.get_init():
        pygame.font.init()

    names = MONO_FONT_NAMES if mono else THAI_FONT_NAMES
    for name in names:
        path = pygame.font.match_font(name, bold=bold)
        if path:
            font = pygame.font.Font(path, size)
            font.set_bold(bold)
            return font

    return pygame.font.SysFont(None, size, bold=bold)


def make_ui_fonts():
    return (
        make_font(36, bold=True),
        make_font(24, bold=True),
        make_font(18),
        make_font(14),
    )


# ======================================================================
#  CLASS Piece — หมากหนึ่งตัว
#
#  Class = แม่พิมพ์สร้าง Object
#  เปรียบเหมือน: แบบหล่อขนม ใช้แบบเดียวกัน ได้หลายชิ้น
# ======================================================================
class Piece:

    def __init__(self, row, col, player):
        # __init__ = วิธีสร้างหมากใหม่ (Constructor)
        # "self" = ตัวหมากนี้เอง เหมือนพูดว่า "ฉัน"
        # ทุกครั้งที่เขียน Piece(r,c,p) Python จะรัน __init__ ทันที
        # เปรียบเหมือน: ตอนเกิด ต้องได้ชื่อ ที่อยู่ สัญชาติ ทันที
        self.row     = row      # อยู่แถวที่เท่าไหร่ (0=บน ... 7=ล่าง)
        self.col     = col      # อยู่คอลัมน์ที่เท่าไหร่ (0=ซ้าย ... 7=ขวา)
        self.player  = player   # เป็นของใคร (RED=1 หรือ BLACK=2)
        self.is_king = False    # เป็นดามหรือยัง (False=ยังไม่ใช่)
        self._upd()             # คำนวณพิกัด pixel

    def _upd(self):
        # คำนวณพิกัด pixel กึ่งกลางหมาก
        # สูตร: pixel = (ดัชนีช่อง x ขนาดช่อง) + ครึ่งช่อง
        # ตัวอย่าง col=3, SQ=105 → x = 3x105 + 52 = 367 pixel
        self.x = self.col * SQ + SQ // 2
        self.y = self.row * SQ + SQ // 2

    def crown(self):
        # เลื่อนหมากเป็นดาม: เปลี่ยน is_king จาก False → True
        self.is_king = True

    def move(self, row, col):
        # ย้ายหมากไปตำแหน่งใหม่ แล้วอัปเดตพิกัด pixel
        # เปรียบเหมือน: ย้ายบ้าน — ที่อยู่ใหม่ต้องอัปเดตด้วย
        self.row = row
        self.col = col
        self._upd()

    def draw(self, surf, selected=False, forced=False):
        # วาดหมากทีละชั้น เหมือนทาสีทับกัน:
        # ชั้น 1: เงา      ชั้น 2: กรอบเลือก/บังคับ
        # ชั้น 3: ขอบ      ชั้น 4: สีพื้น
        # ชั้น 5: แสงสะท้อน  ชั้น 6: ดาวดาม

        # เลือกสีตามผู้เล่น
        # if-else เหมือนแยกทาง: ถ้า... → ไปซ้าย  ไม่งั้น → ไปขวา
        if self.player == RED:
            cf, co = C_RED, C_RED_D
        else:
            cf, co = C_BLK, C_BLK_D

        cx, cy = self.x, self.y

        # ชั้น 1: เงา
        # pygame.SRCALPHA = รองรับความโปร่งแสง (alpha channel)
        sh = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        pygame.draw.circle(sh, (0, 0, 0, 65), (SQ//2+5, SQ//2+5), R_PIECE)
        # blit = "แปะ" ภาพ sh ลงบน surf
        surf.blit(sh, (cx - SQ//2, cy - SQ//2))

        # ชั้น 2: กรอบพิเศษ
        if forced:
            # ถูกบังคับ → กรอบแดงสดกะพริบ
            pygame.draw.circle(surf, C_FORCE, (cx, cy), R_PIECE + 12)
            pygame.draw.circle(surf, C_WHITE,  (cx, cy), R_PIECE + 12, 2)
        elif selected:
            # ถูกเลือก → กรอบทอง
            pygame.draw.circle(surf, C_SEL, (cx, cy), R_PIECE + 10)

        # ชั้น 3: ขอบหมาก
        pygame.draw.circle(surf, co, (cx, cy), R_PIECE + 4)

        # ชั้น 4: สีหมาก
        pygame.draw.circle(surf, cf, (cx, cy), R_PIECE)

        # ชั้น 5: แสงสะท้อน (Gloss effect ทำให้ดูเป็น 3D)
        gl = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        pygame.draw.circle(gl, (255, 255, 255, 50),
                           (SQ//2 - 12, SQ//2 - 12), R_PIECE // 2)
        surf.blit(gl, (cx - SQ//2, cy - SQ//2))

        # ชั้น 6: ดาวทอง ถ้าเป็นดาม
        if self.is_king:
            self._star(surf, cx, cy)

    def _star(self, surf, cx, cy):
        # วาดดาว 5 แฉก บนหมากดาม
        # คณิตศาสตร์: วงกลม = 360 องศา  แบ่งเป็น 10 จุด
        # จุดคู่ (0,2,4,6,8) = ปลายแฉก (รัศมีใหญ่)
        # จุดคี่ (1,3,5,7,9) = ร่อง     (รัศมีเล็ก)
        # cos(มุม) = ระยะแนวนอน   sin(มุม) = ระยะแนวตั้ง
        N   = 5
        ro  = R_KING
        ri  = R_KING // 2
        pts = []
        # range(N*2) = สร้างตัวเลข 0 ถึง 9
        # วนลูป i = 0, 1, 2, ..., 9
        for i in range(N * 2):
            # i%2==0 = คู่ → ปลายแฉก  i%2==1 = คี่ → ร่อง
            r = ro if i % 2 == 0 else ri
            # มุม: หมุนทีละ π/N ลบ π/2 เพื่อชี้ขึ้น
            a = math.pi * i / N - math.pi / 2
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pygame.draw.polygon(surf, C_GOLD,        pts)
        pygame.draw.polygon(surf, (170, 120, 0), pts, 1)


# ======================================================================
#  CLASS Board — กระดานและกฎเกมทั้งหมด
# ======================================================================
class Board:

    def __init__(self):
        # สร้างกระดาน 8x8 ว่างๆ
        # List Comprehension: "[ค่า for _ in range(n)]" = สร้าง list ซ้ำ n ครั้ง
        # "_" = ตัวนับที่เราไม่สนใจค่า
        # ผลลัพธ์: [[0,0,0,0,0,0,0,0], [...], ...] (8 แถว x 8 ช่อง)
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]

        # นับหมากที่เหลือ
        # dict = สมุดโทรศัพท์: "ชื่อ" → "ค่า"
        # cnt[RED] = 8 หมายถึง "หมากแดงเหลือ 8 ตัว"
        self.cnt = {RED: 8, BLACK: 8}

        self._setup()

    def _setup(self):
        # วางหมาก 8 ตัว x 2 ฝ่าย ตามกฎไทย:
        # หมากดำ  → แถว 0, 1  (2 แถวบนสุด)
        # หมากแดง → แถว 6, 7  (2 แถวล่างสุด)
        # วางบนช่องสีเข้มเท่านั้น = (row+col) เป็นเลขคี่
        # แต่ละแถวมีช่องเข้ม 4 ช่อง x 2 แถว = 8 ตัว ✓

        # วนลูปทุกแถว: เปรียบเหมือน เดินตรวจทีละแถวจากบนลงล่าง
        for row in range(ROWS):
            # วนลูปทุกคอลัมน์: เปรียบเหมือน เดินจากซ้ายไปขวาในแถวนั้น
            for col in range(COLS):
                # ตรวจช่องสีเข้ม: (row+col)%2==1 → ผลรวมเป็นคี่ → ช่องเข้ม
                # ตัวอย่าง: row=0, col=1 → 0+1=1 → 1%2=1 ✓ ช่องเข้ม
                if (row + col) % 2 == 1:
                    if row <= 1:
                        # 2 แถวบน → หมากดำ
                        self.grid[row][col] = Piece(row, col, BLACK)
                    elif row >= 6:
                        # 2 แถวล่าง → หมากแดง
                        self.grid[row][col] = Piece(row, col, RED)

    def get(self, r, c):
        # ดูช่อง (r, c) ว่ามีอะไร
        # ถ้านอกกระดาน → คืน None (ไม่มีอะไร)
        # "0 <= r < ROWS" = r ต้องอยู่ใน range 0-7
        if 0 <= r < ROWS and 0 <= c < COLS:
            return self.grid[r][c]
        return None

    def do_move(self, piece, tr, tc, captured):
        # ทำการเดินจริงบนกระดาน
        # Parameters:
        #   piece    = หมากที่จะย้าย
        #   tr, tc   = row/col ปลายทาง
        #   captured = list หมากที่ถูกกิน (อาจว่าง [])

        # ลบหมากที่ถูกกิน
        # "for cp in captured" = วนลูปทุกหมากใน list
        # เปรียบเหมือน: เก็บหมากออกทีละตัวที่ถูกจับ
        for cp in captured:
            self.grid[cp.row][cp.col] = EMPTY   # ช่องนั้น = ว่าง
            self.cnt[cp.player] -= 1             # ลดจำนวนหมาก (–= ลบแล้วเก็บ)

        # ย้ายหมาก
        self.grid[piece.row][piece.col] = EMPTY   # ช่องเดิม = ว่าง
        piece.move(tr, tc)                         # บอกหมากว่าอยู่ที่ไหนใหม่
        self.grid[tr][tc] = piece                  # ช่องใหม่ = หมาก

        # ตรวจเลื่อนเป็นดาม
        if not piece.is_king:
            if piece.player == RED   and tr == 0:        piece.crown()
            if piece.player == BLACK and tr == ROWS - 1: piece.crown()

    def valid_moves(self, piece, must_capture=False, already_captured=None):
        # หาการเดินที่ถูกกฎสำหรับหมากตัวนั้น
        #
        # Parameters:
        #   must_capture     = True → คืนเฉพาะการกิน (บังคับกิน)
        #   already_captured = set หมากที่กินไปแล้ว (ป้องกันกินซ้ำ)
        #
        # คืนค่า dict: { (tr, tc): [Piece ที่กิน], ... }
        #   list ว่าง = เดินปกติ   list มีหมาก = กระโดดกิน

        moves = {}

        # ถ้าไม่ส่ง already_captured มา → ใช้ set ว่าง
        if already_captured is None:
            already_captured = set()

        if piece.is_king:
            # === ดาม: เดินทแยงทุกทิศ ไกลไม่จำกัด ===
            # ทิศทาง 4 แบบ: (delta_row, delta_col)
            # (-1,-1)=บนซ้าย  (-1,+1)=บนขวา  (+1,-1)=ล่างซ้าย  (+1,+1)=ล่างขวา
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                r, c      = piece.row + dr, piece.col + dc
                found_cap = None   # หมากฝ่ายตรงข้ามที่เจอ
                cap_pos   = None

                # วนเดินตามทิศนั้นจนสุด ไม่จำกัดระยะ
                # "while True" = วนไปเรื่อยๆ จนกว่าจะ break
                # เปรียบเหมือน: เดินตรงไปจนกว่าจะเจอกำแพงหรือหมาก
                while True:
                    cell = self.get(r, c)
                    if cell is None:
                        break   # ออกนอกกระดาน → หยุดทิศนี้
                    if cell == EMPTY:
                        if found_cap is not None:
                            # ข้ามหมากข้าศึกมาแล้ว → ลงที่นี่ได้
                            if cap_pos not in already_captured:
                                moves[(r, c)] = [found_cap]
                        elif not must_capture:
                            # ไม่บังคับกิน → เดินปกติได้
                            moves[(r, c)] = []
                    elif cell.player == piece.player:
                        break   # เจอหมากพวกเดียวกัน → หยุด
                    else:
                        # เจอหมากฝ่ายตรงข้าม
                        if found_cap is not None:
                            break   # เจอสองตัวติดกัน → ข้ามไม่ได้
                        if cell in already_captured:
                            break
                        found_cap = cell
                        cap_pos   = (cell.row, cell.col)
                    r += dr
                    c += dc

        else:
            # === หมากธรรมดา: เดินหน้าเท่านั้น ===
            # dr: แดงขึ้น (–1), ดำลง (+1)
            dr = -1 if piece.player == RED else 1

            # วนทิศซ้าย (dc=–1) และขวา (dc=+1)
            # [-1, 1] = list ที่มีสองค่า
            for dc in [-1, 1]:
                r1, c1 = piece.row + dr, piece.col + dc
                t1     = self.get(r1, c1)

                if t1 is None:
                    continue   # "continue" = ข้ามรอบนี้ ไปรอบถัดไป

                if t1 == EMPTY and not must_capture:
                    # ช่องว่าง + ไม่บังคับกิน → เดินปกติ
                    moves[(r1, c1)] = []

                elif t1 != EMPTY and t1.player != piece.player:
                    # มีหมากฝ่ายตรงข้าม → ตรวจกระโดดข้าม
                    r2, c2 = piece.row + dr*2, piece.col + dc*2
                    t2     = self.get(r2, c2)
                    if t2 == EMPTY and t1 not in already_captured:
                        # ช่องลงว่าง → กระโดดได้!
                        moves[(r2, c2)] = [t1]

        return moves

    def all_moves(self, player, force_capture=False):
        # หาการเดินทั้งหมดของฝ่ายนั้น
        #
        # Parameters:
        #   force_capture = True → บังคับกิน (ต้องกินเท่านั้น)
        #                   False → เลือกได้ (กฎปกติไทย)
        #
        # คืนค่า: (dict {Piece: {(r,c):[caps]}},  can_capture: bool)

        result      = {}
        can_capture = False   # มีการกินได้ไหม (ใช้แสดง UI)

        # ตรวจว่ามีการกินได้ไหม
        for row in range(ROWS):
            for col in range(COLS):
                p = self.grid[row][col]
                if p == EMPTY or p.player != player:
                    continue
                m = self.valid_moves(p)
                # "any(...)" = True ถ้ามีค่า True อยู่สักตัว
                if any(v for v in m.values() if v):
                    can_capture = True
                    break
            if can_capture:
                break

        # รวบรวมการเดิน
        for row in range(ROWS):
            for col in range(COLS):
                p = self.grid[row][col]
                if p == EMPTY or p.player != player:
                    continue
                # ถ้า force_capture=True → must_capture=True (บังคับกิน)
                # ถ้า force_capture=False → must_capture=False (เลือกได้)
                m = self.valid_moves(p, must_capture=force_capture)
                if m:
                    result[p] = m

        return result, can_capture

    def winner(self):
        # ตรวจว่ามีผู้ชนะแล้วหรือยัง
        # คืน RED, BLACK, หรือ None (ยังเล่นอยู่)
        if self.cnt[RED]   <= 0: return BLACK
        if self.cnt[BLACK] <= 0: return RED
        if not self.all_moves(RED)[0]:   return BLACK   # แดงเดินไม่ได้
        if not self.all_moves(BLACK)[0]: return RED     # ดำเดินไม่ได้
        return None

    def draw_board(self, surf):
        # วาดกระดานและหมากทุกตัว

        # วาดช่องกระดาน
        for row in range(ROWS):
            for col in range(COLS):
                # (row+col)%2==0 → สว่าง   ==1 → มืด
                color = C_LIGHT if (row+col)%2==0 else C_DARK
                pygame.draw.rect(surf, color,
                    pygame.Rect(col*SQ, row*SQ, SQ, SQ))

        # เส้นตาราง
        # range(ROWS+1) = 0, 1, ..., 8  รวม 9 เส้น
        for i in range(ROWS + 1):
            pygame.draw.line(surf,(0,0,0),(0,i*SQ),(BOARD_PX,i*SQ),1)
        for j in range(COLS + 1):
            pygame.draw.line(surf,(0,0,0),(j*SQ,0),(j*SQ,BOARD_PX),1)

        # วาดหมากทุกตัว
        for row in range(ROWS):
            for col in range(COLS):
                p = self.grid[row][col]
                if p != EMPTY:
                    p.draw(surf)


# ======================================================================
#  CLASS Timer — นาฬิกานับถอยหลัง + ระบบพัก
# ======================================================================
class Timer:

    def __init__(self):
        # เวลาที่เหลือของแต่ละผู้เล่น (วินาที)
        self.time_left    = {RED: TURN_TIME, BLACK: TURN_TIME}
        # จำนวนครั้งพักที่เหลือ
        self.timeout_left = {RED: MAX_TIMEOUTS, BLACK: MAX_TIMEOUTS}
        self.active     = RED
        # time.time() = วินาทีตั้งแต่ 1 ม.ค. 1970 ถึงตอนนี้ (Unix time)
        self.last_tick  = time.time()
        self.paused     = False    # กำลังพักอยู่ไหม
        self.pause_end  = 0        # เวลา Unix ที่พักจะสิ้นสุด
        self.timed_out  = None     # ใครหมดเวลา

    def switch(self, player):
        # เปลี่ยนนาฬิกาไปผู้เล่นใหม่ + รีเซ็ตเวลาตา
        self.active              = player
        self.time_left[player]   = TURN_TIME
        self.last_tick           = time.time()

    def request_timeout(self, player):
        # ขอพัก: คืน True ถ้าอนุมัติ
        if self.paused: return False
        if self.timeout_left[player] <= 0: return False
        self.paused               = True
        self.pause_end            = time.time() + TIMEOUT_DUR
        self.timeout_left[player] -= 1
        return True

    def update(self):
        # อัปเดตนาฬิกาทุกเฟรม (60 ครั้ง/วินาที)
        now = time.time()
        if self.paused:
            # กำลังพัก → ตรวจว่าหมดเวลาพักหรือยัง
            if now >= self.pause_end:
                self.paused    = False
                self.last_tick = now
        else:
            # กำลังเล่น → ลดเวลา
            # elapsed = เวลาที่ผ่านไปตั้งแต่ tick ล่าสุด
            elapsed = now - self.last_tick
            self.time_left[self.active] -= elapsed
            self.last_tick = now
            if self.time_left[self.active] <= 0:
                self.time_left[self.active] = 0
                self.timed_out = self.active

    def fmt(self, player):
        # แปลงวินาที → MM:SS  เช่น 90 → "01:30"
        secs = max(0, int(self.time_left[player]))
        # f-string: f"..." = แทรกตัวแปรใน string
        # :02d = แสดง 2 หลัก เติม 0 ถ้าน้อยกว่า 10 เช่น 5 → "05"
        return f"{secs//60:02d}:{secs%60:02d}"

    def color(self, player):
        # สีนาฬิกาตามเวลาที่เหลือ
        t = self.time_left[player]
        if t > 30: return C_GREEN    # > 30 วินาที → เขียว (ปลอดภัย)
        if t > 10: return C_YELLOW   # > 10 วินาที → เหลือง (ระวัง)
        return C_TIMEOUT             # ≤ 10 วินาที → แดง (อันตราย!)


# ======================================================================
#  CLASS Game — ตัวกลางควบคุมเกมทั้งหมด
# ======================================================================
class Game:

    def __init__(self, screen):
        self.screen  = screen
        self.board   = Board()
        self.timer   = Timer()
        self.turn    = RED          # แดงเริ่มก่อน

        # ── state การเลือกหมาก ──
        self.sel      = None   # หมากที่เลือกอยู่ (None=ยังไม่เลือก)
        self.hints    = {}     # ช่องที่เดินได้ {(r,c):[caps]}
        self.movable  = set()  # set หมากที่เดินได้

        # ── state กฎบังคับกิน ──
        # can_capture  = มีการกินได้ในตานี้หรือเปล่า (แสดง UI เตือน)
        # force_active = true ถ้าฝ่ายตรงข้ามประกาศบังคับกิน
        # force_by     = ใครเป็นคนประกาศบังคับ
        self.can_capture  = False
        self.force_active = False
        self.force_by     = None

        # ── state อื่นๆ ──
        self.move_count   = 0
        self.game_over    = False
        self.winner       = None   # None = ยังไม่มีหรือเสมอ
        self.win_reason   = ""

        # ── ประวัติการเดิน (ตรวจเสมอ) ──
        # deque(maxlen=20) = คิวเก็บ 20 รายการล่าสุด อัตโนมัติ
        self.move_history = deque(maxlen=20)

        # ── ฟอนต์ ──
        pygame.font.init()
        self.f_lg, self.f_md, self.f_sm, self.f_xs = make_ui_fonts()
        self.f_tm = make_font(30, bold=True, mono=True)

        self._refresh()

    def _refresh(self):
        # อัปเดตหมากที่เดินได้สำหรับตาปัจจุบัน
        # ถ้า force_active=True → บังคับกิน (must_capture=True)
        # ถ้า force_active=False → เลือกได้ (must_capture=False)
        all_m, self.can_capture = self.board.all_moves(
            self.turn, force_capture=self.force_active
        )
        # "set(...)" แปลง dict_keys → set (ค้นหาเร็วกว่า list)
        self.movable = set(all_m.keys())

    def _opponent(self, player):
        # คืนผู้เล่นฝ่ายตรงข้าม
        # ternary: A if condition else B
        return BLACK if player == RED else RED

    def declare_force(self):
        # ประกาศ "บังคับกิน" ฝ่ายตรงข้าม
        # เงื่อนไข:
        #   1. เกมยังไม่จบ
        #   2. ยังไม่มีการบังคับกินอยู่แล้ว
        #   3. ฝ่ายตรงข้ามมีการกินได้จริง
        if self.game_over: return
        if self.force_active: return

        opp = self._opponent(self.turn)
        _, opp_can = self.board.all_moves(opp, force_capture=False)

        if opp_can:
            # ฝ่ายตรงข้ามกินได้จริง → ประกาศบังคับได้
            self.force_active = True
            self.force_by     = self.turn   # ผู้ที่ประกาศ
            # รีเซ็ตการเลือก
            self.sel   = None
            self.hints = {}
            # สลับตาทันที เพื่อให้ฝ่ายตรงข้ามเดิน
            self.turn = opp
            self.timer.switch(self.turn)
            self._refresh()

    def violation(self, player):
        # ผู้เล่น player ฝ่าฝืนกฎ → ฝ่ายตรงข้ามชนะ
        self.game_over  = True
        self.winner     = self._opponent(player)
        self.win_reason = f"{'แดง' if player==RED else 'ดำ'} ฝ่าฝืนกฎ"

    def click(self, mx, my):
        # จัดการเมื่อคลิกเมาส์
        if self.game_over:    return
        if self.timer.paused: return
        if my >= BOARD_PX:    return   # คลิกนอกกระดาน

        # แปลง pixel → row/col
        # ตัวอย่าง: mx=320, SQ=105 → col = 320//105 = 3
        col     = mx // SQ
        row     = my // SQ
        clicked = self.board.get(row, col)

        if self.sel is None:
            # ยังไม่มีหมากที่เลือก → ลองเลือก
            # ตรวจ 3 เงื่อนไข: มีหมาก, เป็นของตัวเอง, เดินได้
            if (clicked not in (EMPTY, None)
                    and clicked.player == self.turn
                    and clicked in self.movable):
                self.sel   = clicked
                all_m, _   = self.board.all_moves(
                    self.turn, force_capture=self.force_active
                )
                # .get(key, default) = คืนค่าถ้ามี key ไม่งั้นคืน default
                self.hints = all_m.get(clicked, {})

        elif (row, col) in self.hints:
            # คลิกช่องที่เดินได้ → เดิน!
            caps = self.hints[(row, col)]

            # ตรวจเสมอ: เดินซ้ำ
            move_key = (self.sel.row, self.sel.col, row, col)
            self.move_history.append(move_key)
            # .count(x) = นับว่า x ปรากฏกี่ครั้งใน deque
            if self.move_history.count(move_key) > REPEAT_DRAW_LIMIT:
                self.game_over  = True
                self.winner     = None
                self.win_reason = "เดินซ้ำเกิน 3 ครั้ง → เสมอ"
                return

            # ตรวจ: ถ้าถูกบังคับกิน แต่เลือกเดินปกติ → ฝ่าฝืนกฎ!
            if self.force_active and not caps:
                self.violation(self.turn)
                return

            # ทำการเดินจริง
            self.board.do_move(self.sel, row, col, caps)
            self.move_count += 1

            # ตรวจกินต่อเนื่อง (เฉพาะดาม)
            if caps and self.sel.is_king:
                already     = set(caps)
                follow      = self.board.valid_moves(
                    self.sel, must_capture=True, already_captured=already
                )
                # dict comprehension: สร้าง dict ใหม่จากคู่ที่กรองแล้ว
                jump_follow = {k: v for k, v in follow.items() if v}
                if jump_follow:
                    # ดามยังกินต่อได้ → ไม่สลับตา
                    self.hints   = jump_follow
                    self.movable = {self.sel}
                    return

            # ตรวจผู้ชนะ
            w = self.board.winner()
            if w:
                self.game_over  = True
                self.winner     = w
                self.win_reason = "กินหมดทุกตัว หรือ เดินไม่ได้"
                return

            # ยกเลิกการบังคับกิน (ถ้ากินเสร็จแล้ว)
            if caps and self.force_active:
                self.force_active = False
                self.force_by     = None

            # สลับตา
            self.sel   = None
            self.hints = {}
            self.turn  = self._opponent(self.turn)
            self.timer.switch(self.turn)
            self._refresh()

        elif (clicked not in (EMPTY, None)
              and clicked.player == self.turn
              and clicked in self.movable):
            # คลิกหมากตัวอื่นของตัวเอง → เปลี่ยนหมากที่เลือก
            self.sel   = clicked
            all_m, _   = self.board.all_moves(
                self.turn, force_capture=self.force_active
            )
            self.hints = all_m.get(clicked, {})
        else:
            # คลิกที่อื่น → ยกเลิก
            self.sel   = None
            self.hints = {}

    def surrender(self, player):
        # ยอมแพ้
        self.game_over  = True
        self.winner     = self._opponent(player)
        self.win_reason = f"{'แดง' if player==RED else 'ดำ'} ยอมแพ้"

    def declare_draw(self):
        # ประกาศเสมอ (กรรมการ)
        self.game_over  = True
        self.winner     = None
        self.win_reason = "กรรมการตัดสินให้เสมอ"

    def update(self):
        # อัปเดตทุกเฟรม
        if self.game_over: return
        self.timer.update()
        if self.timer.timed_out is not None:
            loser           = self.timer.timed_out
            self.game_over  = True
            self.winner     = self._opponent(loser)
            self.win_reason = f"{'แดง' if loser==RED else 'ดำ'} หมดเวลา 2 นาที"

    # ──────────────────────────────────────────────────────────────────
    #  DRAW METHODS
    # ──────────────────────────────────────────────────────────────────
    def draw(self):
        self.screen.fill(C_BG)

        # กระดาน
        self.board.draw_board(self.screen)

        # แสดง "forced" highlight บนหมากที่ถูกบังคับกิน
        if self.force_active:
            all_m, _ = self.board.all_moves(self.turn, force_capture=True)
            for p in all_m:
                # แสดงกรอบแดงบนหมากที่ต้องกิน
                pygame.draw.circle(self.screen, C_FORCE, (p.x, p.y), R_PIECE+10, 4)
            # วาดหมากเหล่านั้นใหม่พร้อม forced=True
            for p in all_m:
                p.draw(self.screen, forced=True)
        else:
            # กรอบหมากที่เดินได้
            col_out = C_JUMP if self.can_capture else C_HINT
            for p in self.movable:
                pygame.draw.circle(self.screen, col_out, (p.x, p.y), R_PIECE+7, 3)

        # หมากที่เลือก
        if self.sel:
            self.sel.draw(self.screen, selected=True)

        # hints (ช่องที่เดินได้)
        for (r, c), caps in self.hints.items():
            hx = c*SQ + SQ//2
            hy = r*SQ + SQ//2
            if caps:
                # การกิน → ส้ม + กากบาท ×
                pygame.draw.circle(self.screen, C_JUMP, (hx,hy), 20)
                pygame.draw.circle(self.screen, C_WARN, (hx,hy), 20, 3)
                d = 8
                pygame.draw.line(self.screen,C_WHITE,(hx-d,hy-d),(hx+d,hy+d),3)
                pygame.draw.line(self.screen,C_WHITE,(hx+d,hy-d),(hx-d,hy+d),3)
            else:
                # เดินปกติ → จุดเขียว
                pygame.draw.circle(self.screen, C_HINT,      (hx,hy), 16)
                pygame.draw.circle(self.screen, (40,140,40), (hx,hy), 16, 2)

        self._draw_panel()
        if self.game_over:
            self._draw_end()

    def _draw_panel(self):
        # แถบข้อมูลด้านล่าง
        pygame.draw.rect(
            self.screen, C_PANEL,
            pygame.Rect(0, BOARD_PX, WINDOW_W, WINDOW_H-BOARD_PX)
        )
        pygame.draw.line(self.screen, C_GOLD, (0,BOARD_PX),(WINDOW_W,BOARD_PX), 2)

        # แบ่ง 3 ส่วน: ซ้าย (แดง) | กลาง | ขวา (ดำ)
        w3 = WINDOW_W // 3
        self._pblock(0,    w3, RED,   "ผู้เล่น 1", C_RED, C_RED_D)
        self._cblock(w3,   w3)
        self._pblock(w3*2, w3, BLACK, "ผู้เล่น 2", C_BLK, C_BLK_D)

        # แสดงข้อความพักถ้าพักอยู่
        if self.timer.paused:
            remain = max(0, self.timer.pause_end - time.time())
            ps = self.f_md.render(
                f"พักอยู่  {int(remain//60):02d}:{int(remain%60):02d}  เหลือ",
                True, C_PAUSE
            )
            self.screen.blit(ps, ps.get_rect(center=(WINDOW_W//2, BOARD_PX+148)))

    def _pblock(self, x, w, player, name, pc, po):
        # วาดข้อมูลผู้เล่น 1 คน
        px = x + w//2
        is_active = (self.turn == player and not self.game_over)

        if is_active:
            # ไฮไลท์พื้นหลัง
            pygame.draw.rect(
                self.screen, (35,28,15),
                pygame.Rect(x, BOARD_PX+1, w, WINDOW_H-BOARD_PX-1)
            )

        # ชื่อ
        nc = pc if is_active else C_GRAY
        ns = self.f_sm.render(name, True, nc)
        self.screen.blit(ns, ns.get_rect(center=(px, BOARD_PX+22)))

        # วงกลมหมาก + จำนวน
        pygame.draw.circle(self.screen, pc, (px-22, BOARD_PX+60), 18)
        pygame.draw.circle(self.screen, po, (px-22, BOARD_PX+60), 18, 3)
        cs = self.f_md.render(f"x {self.board.cnt[player]}", True, C_WHITE)
        self.screen.blit(cs, cs.get_rect(midleft=(px+2, BOARD_PX+60)))

        # นาฬิกา
        tc = self.timer.color(player)
        ts = self.f_tm.render(self.timer.fmt(player), True, tc)
        self.screen.blit(ts, ts.get_rect(center=(px, BOARD_PX+102)))

        # ครั้งพักเหลือ
        tos = self.f_xs.render(
            f"พัก: {self.timer.timeout_left[player]}x เหลือ", True, C_GRAY
        )
        self.screen.blit(tos, tos.get_rect(center=(px, BOARD_PX+130)))

    def _cblock(self, x, w):
        # ข้อมูลกลาง
        px = x + w//2

        if not self.game_over:
            # ตาของใคร
            who = "ตาของ: แดง" if self.turn==RED else "ตาของ: ดำ"
            wc  = C_RED if self.turn==RED else (200,200,200)
            ws  = self.f_sm.render(who, True, wc)
            self.screen.blit(ws, ws.get_rect(center=(px, BOARD_PX+22)))

            # สถานะบังคับกิน
            if self.force_active:
                # กำลังถูกบังคับ!
                fc = self.f_xs.render("! บังคับกิน! (ต้องกินทันที)", True, C_FORCE)
                self.screen.blit(fc, fc.get_rect(center=(px, BOARD_PX+50)))
                who_forced = "แดง" if self.force_by==RED else "ดำ"
                fb = self.f_xs.render(f"ประกาศโดย: {who_forced}", True, C_WARN)
                self.screen.blit(fb, fb.get_rect(center=(px, BOARD_PX+68)))
            elif self.can_capture:
                # กินได้แต่ไม่บังคับ
                jc = self.f_xs.render("กินได้ (ไม่บังคับ)", True, C_JUMP)
                self.screen.blit(jc, jc.get_rect(center=(px, BOARD_PX+52)))

            ms = self.f_xs.render(f"เดิน: {self.move_count}", True, C_GRAY)
            self.screen.blit(ms, ms.get_rect(center=(px, BOARD_PX+86)))

        # คำแนะนำปุ่ม
        for i, txt in enumerate(["T=พัก  F=บังคับกิน", "S=ยอมแพ้  V=ฝ่าฝืนกฎ", "D=เสมอ  R=เล่นใหม่"]):
            hs = self.f_xs.render(txt, True, (85,80,72))
            self.screen.blit(hs, hs.get_rect(center=(px, BOARD_PX+108+i*17)))

    def _draw_end(self):
        # หน้าจอจบเกม
        ov = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
        ov.fill((10,8,4,212))
        self.screen.blit(ov, (0,0))

        bw, bh = 560, 250
        bx = (WINDOW_W-bw)//2
        by = (WINDOW_H-bh)//2

        if self.winner == RED:
            result, bc = "ผู้เล่น 1 (แดง) ชนะ!", C_RED
        elif self.winner == BLACK:
            result, bc = "ผู้เล่น 2 (ดำ) ชนะ!", (195,195,195)
        else:
            result, bc = "เสมอกัน!", C_GOLD

        pygame.draw.rect(self.screen,(20,15,8),(bx,by,bw,bh),border_radius=18)
        pygame.draw.rect(self.screen,bc,       (bx,by,bw,bh), 3, border_radius=18)

        rs = self.f_lg.render(result, True, bc)
        self.screen.blit(rs, rs.get_rect(center=(WINDOW_W//2, WINDOW_H//2-50)))

        if self.win_reason:
            rr = self.f_sm.render(f"เหตุผล: {self.win_reason}", True, C_GRAY)
            self.screen.blit(rr, rr.get_rect(center=(WINDOW_W//2, WINDOW_H//2+10)))

        bs = self.f_sm.render("R = เล่นใหม่   |   ESC = ออก", True, C_GRAY)
        self.screen.blit(bs, bs.get_rect(center=(WINDOW_W//2, WINDOW_H//2+65)))

    def reset(self):
        # รีเซ็ตเกมทั้งหมด เรียก __init__ ใหม่
        self.__init__(self.screen)


# ======================================================================
#  หน้าจอ Title
# ======================================================================
def draw_title(screen, fonts):
    f_lg, f_md, f_sm, f_xs = fonts

    screen.fill((16,12,6))
    for row in range(ROWS):
        for col in range(COLS):
            if (row+col)%2==1:
                pygame.draw.rect(screen,(26,20,10),
                    pygame.Rect(col*SQ,row*SQ,SQ,SQ))

    ov = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
    ov.fill((8,6,2,194))
    screen.blit(ov,(0,0))

    t1 = f_lg.render("หมากฮอสไทย", True, C_GOLD)
    t2 = f_md.render("กฎมาตรฐานไทย · 8 ตัว · บังคับกิน · ดามไร้ขีดจำกัด", True,(195,180,145))
    screen.blit(t1, t1.get_rect(center=(WINDOW_W//2, 205)))
    screen.blit(t2, t2.get_rect(center=(WINDOW_W//2, 256)))

    # กฎสำคัญ
    # list ของ tuple: (ไอคอน, ข้อความ, สี)
    rules = [
        ("1.", "8 ตัว x 2 ฝ่าย  วางใน 2 แถวสุดท้าย บนช่องสีเข้ม",     C_GRAY),
        ("2.", "ผู้เล่น 1 (แดง) เดินขึ้น",                                 C_RED),
        ("3.", "ผู้เล่น 2 (ดำ)  เดินลง",                                   (190,190,190)),
        ("4.", "กินหรือไม่ก็ได้  แต่ถ้าคู่ต่อสู้บังคับ (F) ต้องกิน!",   C_WARN),
        ("5.", "จุดเขียว=เดินได้  จุดส้ม=กินได้  ขอบแดง=บังคับ!",       C_HINT),
        ("6.", "ถึงฝั่งตรงข้าม = ดาม (เดินทุกทิศ ไกลไม่จำกัด)",         C_GOLD),
        ("7.", "2 นาที/ตา  |  พักได้ 2x5 นาที  (T)",                      C_GRAY),
        ("8.", "S=ยอมแพ้  V=ฝ่าฝืนกฎ  D=เสมอ  F=บังคับกิน",            C_GRAY),
    ]

    # วนลูปแสดงกฎ
    # "enumerate(rules)" คืน (ดัชนี, ค่า) ทีละคู่
    for i, (label, text, color) in enumerate(rules):
        s = f_sm.render(f"{label}  {text}", True, color)
        screen.blit(s, s.get_rect(center=(WINDOW_W//2, 315 + i*44)))

    btn = pygame.Rect(WINDOW_W//2-165, 695, 330, 58)
    pygame.draw.rect(screen, C_GOLD, btn, border_radius=14)
    bs  = f_md.render("กด  SPACE  เพื่อเริ่มเกม", True, (12,8,2))
    screen.blit(bs, bs.get_rect(center=btn.center))

    hint = f_xs.render(
        "T=พัก   S=ยอมแพ้   F=บังคับกิน   V=ฝ่าฝืนกฎ   D=เสมอ   R=เล่นใหม่   ESC=ออก",
        True, (78,72,62)
    )
    screen.blit(hint, hint.get_rect(center=(WINDOW_W//2, 775)))


# ======================================================================
#  FUNCTION main — จุดเริ่มต้นโปรแกรม
# ======================================================================
def main():
    # เริ่มต้น pygame
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("หมากฮอสไทย | Thai Checkers")

    # clock ควบคุม FPS
    clock = pygame.time.Clock()
    FPS   = 60   # 60 เฟรม/วินาที

    # tuple ฟอนต์สำหรับหน้า title
    # tuple = กลุ่มค่าที่เปลี่ยนไม่ได้ เหมือนกล่องที่ล็อคแล้ว
    fonts = make_ui_fonts()

    game  = Game(screen)
    state = "title"

    # ── Game Loop ────────────────────────────────────────────────────
    # วนซ้ำ 60 ครั้ง/วินาที จนกว่า running = False
    # แต่ละรอบ: 1.รับ events  2.อัปเดต  3.วาด
    # เปรียบเหมือน: ภาพยนตร์ที่ฉาย 60 ภาพ/วินาที
    # ────────────────────────────────────────────────────────────────
    running = True

    # "while running" = วนซ้ำตราบเท่าที่ running = True
    while running:

        # ── ส่วนที่ 1: รับ Events ────────────────────────────────
        # pygame.event.get() = "เช็คกล่องจดหมาย" ว่ามีเหตุการณ์อะไรบ้าง
        for event in pygame.event.get():
            # "event" = เหตุการณ์หนึ่งอย่าง เช่น คลิก กดปุ่ม ปิดหน้าต่าง

            if event.type == pygame.QUIT:
                # กด X ปิดหน้าต่าง
                running = False

            elif event.type == pygame.KEYDOWN:
                # กดคีย์บอร์ด
                k = event.key   # รหัสปุ่มที่กด

                if k == pygame.K_ESCAPE:
                    running = False

                elif k == pygame.K_SPACE and state == "title":
                    state = "playing"

                elif k == pygame.K_r:
                    # R = เล่นใหม่
                    game.reset()
                    state = "playing"

                elif k == pygame.K_t and state == "playing":
                    # T = ขอพัก (ผู้เล่นที่ถึงตา)
                    game.timer.request_timeout(game.turn)

                elif k == pygame.K_s and state == "playing":
                    # S = ยอมแพ้
                    if not game.game_over:
                        game.surrender(game.turn)

                elif k == pygame.K_f and state == "playing":
                    # F = ประกาศบังคับกิน (force capture)
                    # ผู้เล่นที่ถึงตาประกาศให้ฝ่ายตรงข้ามต้องกิน
                    if not game.game_over:
                        game.declare_force()

                elif k == pygame.K_v and state == "playing":
                    # V = Violation: ฝ่ายตรงข้ามฝ่าฝืนกฎ
                    # (ผู้เล่นที่ถึงตากด เพื่อรายงานว่าอีกฝ่ายผิดกฎ)
                    if not game.game_over:
                        opp = game._opponent(game.turn)
                        game.violation(opp)

                elif k == pygame.K_d and state == "playing":
                    # D = Draw: กรรมการตัดสินให้เสมอ
                    if not game.game_over:
                        game.declare_draw()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # คลิกเมาส์
                # event.button: 1=ซ้าย, 2=กลาง, 3=ขวา
                if event.button == 1 and state == "playing":
                    mx, my = event.pos
                    game.click(mx, my)

        # ── ส่วนที่ 2: อัปเดต ──────────────────────────────────
        if state == "playing":
            game.update()

        # ── ส่วนที่ 3: วาดหน้าจอ ───────────────────────────────
        if state == "title":
            draw_title(screen, fonts)
        else:
            game.draw()

        # แสดงผลจริง (flip = พลิก double buffer)
        pygame.display.flip()

        # จำกัด FPS: clock.tick(60) = รอจนครบ 1/60 วินาที
        # เปรียบเหมือน: เข็มนาฬิกาที่กระตุกทีละช่อง
        clock.tick(FPS)

    # ปิดโปรแกรม
    pygame.quit()
    sys.exit(0)


# ======================================================================
#  จุดเริ่มต้นจริง
#
#  Python ตรวจ: ไฟล์นี้ถูก "รันโดยตรง" หรือ "ถูก import"?
#  __name__ == "__main__" → รันโดยตรง → เรียก main()
#  ไม่งั้น → ถูก import → ไม่เรียก (ป้องกันรันซ้ำ)
#  เปรียบเหมือน: เปิดร้านเอง → เปิดไฟ / ส่งของมาฝาก → วางแล้วกลับ
# ======================================================================
if __name__ == "__main__":
    main()
