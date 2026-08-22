import os
import sys
import cv2
import pygame

pygame.init()
pygame.mixer.init()

# bg1.png is 16:9. Keeping the window at the same aspect ratio prevents the
# Minecraft artwork (and its built-in centre panel) from being stretched.
WIDTH = 1200
HEIGHT = 675

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft Launcher")
clock = pygame.time.Clock()

# =========================================================
# FILES
# =========================================================

folder = os.path.dirname(os.path.abspath(__file__))

video_path = os.path.join(folder, "rickrollsecurity.mp4")
music_path = os.path.join(folder, "rickroll.mp3")
bg_path = os.path.join(folder, "bg2.png")
logo_path = os.path.join(folder, "minecraftlogo.svg")

if not os.path.isfile(video_path):
    print("ERROR: rickrollsecurity.mp4 was not found.")
    pygame.quit()
    sys.exit()

if not os.path.isfile(music_path):
    print("ERROR: rickroll.mp3 was not found.")
    pygame.quit()
    sys.exit()

if not os.path.isfile(bg_path):
    print("ERROR: panoramarickroll copy.jpeg was not found.")
    pygame.quit()
    sys.exit()

if not os.path.isfile(logo_path):
    print("ERROR: minecraftlogo.svg was not found.")
    pygame.quit()
    sys.exit()

bg_image = pygame.image.load(bg_path)
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
logo_image = pygame.image.load(logo_path).convert_alpha()
logo_image = pygame.transform.smoothscale(logo_image, (360, 61))
logo_rect = logo_image.get_rect(center=(WIDTH // 2, 155))

# =========================================================
# VIDEO SETUP
# =========================================================

video = cv2.VideoCapture(video_path)
if not video.isOpened():
    print("ERROR: Could not open rickrollsecurity.mp4")
    pygame.quit()
    sys.exit()

fps = video.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30

frame_delay = 1000 / fps
video_timer = 0
video_surface = None

# =========================================================
# COLORS & FONTS
# =========================================================

GREEN_BTN = (84, 172, 62)

INPUT_BG = (10, 10, 10)
INPUT_BORDER = (160, 160, 160)
INPUT_ACTIVE_BORDER = (255, 255, 255)

TEXT_DARK = (35, 35, 35)
TEXT_WHITE = (255, 255, 255)

body_font_path = pygame.font.match_font("helvetica")
heading_font_path = pygame.font.match_font("impact")
button_font_path = pygame.font.match_font("arialblack")
font_body = pygame.font.Font(body_font_path, 19)
font_input = pygame.font.Font(body_font_path, 20)
font_heading = pygame.font.Font(heading_font_path, 30)
font_button = pygame.font.Font(button_font_path, 27)

# A deliberately square bitmap alphabet. Drawing the menu labels from pixels
# gives a much closer Minecraft/Mojangles silhouette than a desktop font.
PIXEL_GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    " ": ("00000",) * 7,
}

# =========================================================
# UI LAYOUT & STATE
# =========================================================

# The sign-in card is centred over the background, like minecraft.net's form.
card_rect = pygame.Rect(370, 215, 460, 320)
card_header = pygame.Rect(card_rect.x, card_rect.y, card_rect.w, 72)
input_box = pygame.Rect(415, 350, 370, 48)
login_button = pygame.Rect(415, 430, 370, 56)

username = ""
input_active = True
rickrolled = False
cursor_timer = 0
show_cursor = True

# =========================================================
# FUNCTIONS
# =========================================================


def get_video_frame():
    global video_surface
    success, frame = video.read()

    if not success:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, frame = video.read()

    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = frame.swapaxes(0, 1)
        video_surface = pygame.surfarray.make_surface(frame)


def trigger_rickroll():
    global rickrolled, video_timer
    rickrolled = True
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    video_timer = 0
    get_video_frame()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)


def draw_pixel_text(text, center, pixel=4, color=TEXT_WHITE, shadow=True):
    """Render crisp block glyphs with Minecraft's hard offset shadow."""
    text = text.upper()
    width = max(0, len(text) * 6 * pixel - pixel)
    height = 7 * pixel
    start_x = center[0] - width // 2
    start_y = center[1] - height // 2

    def paint(offset_x, offset_y, ink):
        for letter_index, letter in enumerate(text):
            glyph = PIXEL_GLYPHS.get(letter, PIXEL_GLYPHS[" "])
            for row, bits in enumerate(glyph):
                for column, bit in enumerate(bits):
                    if bit == "1":
                        pygame.draw.rect(
                            screen,
                            ink,
                            (
                                start_x + letter_index * 6 * pixel + column * pixel + offset_x,
                                start_y + row * pixel + offset_y,
                                pixel,
                                pixel,
                            ),
                        )

    if shadow:
        paint(pixel // 2 + 1, pixel // 2 + 1, (35, 35, 35))
    paint(0, 0, color)


def draw_minecraft_button(rect, text, hovered=False):
    """Draw the green web-style Minecraft action button."""
    border = (28, 38, 24)
    face = (64, 160, 42) if hovered else (47, 139, 35)
    top = (91, 181, 65) if hovered else (75, 164, 52)
    bottom = (31, 92, 24)

    pygame.draw.rect(screen, border, rect, border_radius=3)
    pygame.draw.rect(screen, face, rect.inflate(-6, -6))
    pygame.draw.rect(screen, top, (rect.x + 3, rect.y + 3, rect.w - 6, 5))
    pygame.draw.rect(screen, bottom, (rect.x + 3, rect.bottom - 8, rect.w - 6, 5))
    # Thick, readable white lettering with the game's hard black shadow.
    shadow = font_button.render(text, True, (28, 65, 22))
    label = font_button.render(text, True, TEXT_WHITE)
    screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 3)))
    screen.blit(label, label.get_rect(center=rect.center))


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:
    dt = clock.tick(60)

    cursor_timer += dt
    if cursor_timer >= 500:
        cursor_timer = 0
        show_cursor = not show_cursor

    # -----------------------------------------------------
    # EVENTS
    # -----------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not rickrolled:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                input_active = input_box.collidepoint(event.pos)

                if login_button.collidepoint(event.pos):
                    trigger_rickroll()

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    trigger_rickroll()
                else:
                    if len(username) < 16 and event.unicode.isprintable():
                        username += event.unicode

    # -----------------------------------------------------
    # LOGIN SCREEN
    # -----------------------------------------------------
    if not rickrolled:
        # 1. Draw raw image background
        screen.blit(bg_image, (0, 0))

        # Use the supplied official artwork, with no surrounding navbar.
        screen.blit(logo_image, logo_rect)

        # minecraft.net-inspired sign-in card (the reference navbar is omitted).
        pygame.draw.rect(screen, (252, 252, 252), card_rect)
        pygame.draw.rect(screen, (43, 40, 39), card_rect, 3)
        pygame.draw.rect(screen, (213, 204, 200), card_header)
        pygame.draw.line(
            screen,
            (157, 149, 145),
            card_header.bottomleft,
            card_header.bottomright,
            3,
        )

        helper = font_body.render(
            "Enter your Minecraft username", True, (62, 58, 56)
        )
        screen.blit(helper, helper.get_rect(center=(WIDTH // 2, 322)))

        # Username Input Box
        pygame.draw.rect(screen, INPUT_BG, input_box)
        border_col = INPUT_ACTIVE_BORDER if input_active else INPUT_BORDER
        pygame.draw.rect(screen, border_col, input_box, 2)

        if username:
            txt_surf = font_input.render(username, True, TEXT_WHITE)
        else:
            txt_surf = font_input.render(
                "Minecraft username", True, (185, 185, 185)
            )

        screen.blit(
            txt_surf,
            (input_box.x + 14, input_box.centery - txt_surf.get_height() // 2),
        )

        if input_active and show_cursor:
            cx = (
                input_box.x
                + 14
                + (
                    font_input.render(username, True, TEXT_WHITE).get_width()
                    if username
                    else 0
                )
            )
            pygame.draw.rect(screen, TEXT_WHITE, (cx, input_box.y + 10, 2, 28))

        # PLAY Button
        mouse = pygame.mouse.get_pos()
        draw_minecraft_button(login_button, "PLAY", login_button.collidepoint(mouse))

    # -----------------------------------------------------
    # RICKROLL SCREEN
    # -----------------------------------------------------
    else:
        video_timer += dt
        if video_timer >= frame_delay:
            video_timer -= frame_delay
            get_video_frame()

        if video_surface is not None:
            screen.blit(video_surface, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 70))
        screen.blit(overlay, (0, 0))

        msg_rect = pygame.Rect(390, 25, 420, 50)
        box = msg_rect

        pygame.draw.rect(screen, (0, 0, 0), box)
        pygame.draw.rect(screen, GREEN_BTN, box, 2)
        draw_pixel_text("YOU GOT RICKROLLED", box.center, pixel=3)

    pygame.display.flip()

    # Optional visual-regression capture for development/testing.
    screenshot_path = os.environ.get("RICKROLL_SCREENSHOT")
    if screenshot_path:
        pygame.image.save(screen, screenshot_path)
        running = False

# =========================================================
# CLEANUP
# =========================================================

video.release()
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
