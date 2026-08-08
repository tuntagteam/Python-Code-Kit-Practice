import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
FPS = 60

# Timer: level 1 = 15s, floors at 1s by level 50+
START_TIME = 15.0
MIN_TIME = 1.0
TIME_FLOOR_LEVEL = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stroop Sprint")
clock = pygame.time.Clock()

# ----------------------------
# Windows XP / Luna palette
# ----------------------------

DESKTOP_TOP = (90, 150, 220)
DESKTOP_BOTTOM = (58, 110, 180)

WINDOW_FACE = (236, 233, 216)
WINDOW_FACE_LIGHT = (252, 252, 245)
WINDOW_EDGE_LIGHT = (255, 255, 255)
WINDOW_EDGE_DARK = (113, 111, 100)
WINDOW_EDGE_SHADOW = (64, 64, 64)

TITLE_BLUE_LEFT = (0, 84, 227)
TITLE_BLUE_RIGHT = (61, 149, 255)
TITLE_BLUE_INACTIVE = (122, 150, 223)

BUTTON_FACE = (236, 233, 216)
BUTTON_HOVER = (245, 244, 232)
BUTTON_PRESS = (214, 211, 192)

STATUS_BAR = (236, 233, 216)

TEXT_DARK = (0, 0, 0)
TEXT_MUTED = (80, 80, 80)
TEXT_WHITE = (255, 255, 255)

SUCCESS = (16, 140, 48)
DANGER = (180, 20, 20)
WARNING = (200, 140, 0)
TIMER_OK = (34, 139, 34)
TIMER_WARN = (210, 160, 0)
TIMER_LOW = (200, 30, 30)

# ----------------------------
# Game Colors
# ----------------------------

COLORS = {
    "RED": (200, 30, 30),
    "GREEN": (16, 140, 48),
    "BLUE": (30, 80, 200),
    "YELLOW": (210, 180, 0),
    "PURPLE": (128, 40, 180),
    "ORANGE": (220, 110, 20),
}

# ----------------------------
# Fonts (classic OS feel)
# ----------------------------

font_small = pygame.font.SysFont("tahoma", 16)
font_medium = pygame.font.SysFont("tahoma", 22, bold=True)
font_button = pygame.font.SysFont("tahoma", 24, bold=True)
font_word = pygame.font.SysFont("tahoma", 86, bold=True)
font_title = pygame.font.SysFont("tahoma", 18, bold=True)
font_overlay = pygame.font.SysFont("tahoma", 42, bold=True)
font_caption = pygame.font.SysFont("tahoma", 14, bold=True)


def make_gradient(width, height, top_color, bottom_color, horizontal=False):
    surface = pygame.Surface((width, height))

    if horizontal:
        for x in range(width):
            ratio = x / max(1, width - 1)
            color = tuple(
                int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (x, 0), (x, height))
    else:
        for y in range(height):
            ratio = y / max(1, height - 1)
            color = tuple(
                int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (0, y), (width, y))

    return surface


BACKGROUND = make_gradient(WIDTH, HEIGHT, DESKTOP_TOP, DESKTOP_BOTTOM)


def draw_centered_text(surface, text, font, color, center):
    image = font.render(text, True, color)
    rect = image.get_rect(center=center)
    surface.blit(image, rect)
    return rect


def draw_bevel(surface, rect, raised=True, thick=2):
    """Classic Windows raised / sunken 3D border."""

    if raised:
        light = WINDOW_EDGE_LIGHT
        dark = WINDOW_EDGE_DARK
        shadow = WINDOW_EDGE_SHADOW
    else:
        light = WINDOW_EDGE_SHADOW
        dark = WINDOW_EDGE_LIGHT
        shadow = WINDOW_EDGE_LIGHT

    # Outer light / dark
    pygame.draw.line(
        surface, light, rect.topleft, (rect.right - 1, rect.top)
    )
    pygame.draw.line(
        surface, light, rect.topleft, (rect.left, rect.bottom - 1)
    )
    pygame.draw.line(
        surface, shadow, (rect.right - 1, rect.top),
        (rect.right - 1, rect.bottom - 1)
    )
    pygame.draw.line(
        surface, shadow, (rect.left, rect.bottom - 1),
        (rect.right - 1, rect.bottom - 1)
    )

    if thick >= 2:
        inner = rect.inflate(-2, -2)
        pygame.draw.line(
            surface, light if raised else dark,
            inner.topleft, (inner.right - 1, inner.top)
        )
        pygame.draw.line(
            surface, light if raised else dark,
            inner.topleft, (inner.left, inner.bottom - 1)
        )
        pygame.draw.line(
            surface, dark if raised else light,
            (inner.right - 1, inner.top),
            (inner.right - 1, inner.bottom - 1)
        )
        pygame.draw.line(
            surface, dark if raised else light,
            (inner.left, inner.bottom - 1),
            (inner.right - 1, inner.bottom - 1)
        )


def draw_xp_window(surface, rect, title, active=True):
    """Draw a Windows XP Luna-style window chrome."""

    # Window face
    pygame.draw.rect(surface, WINDOW_FACE, rect)
    draw_bevel(surface, rect, raised=True, thick=2)

    # Title bar
    title_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, 28)
    left = TITLE_BLUE_LEFT if active else TITLE_BLUE_INACTIVE
    right = TITLE_BLUE_RIGHT if active else (166, 202, 240)

    title_bar = make_gradient(
        title_rect.width,
        title_rect.height,
        left,
        right,
        horizontal=True
    )
    surface.blit(title_bar, title_rect.topleft)

    # Caption
    caption = font_caption.render(title, True, TEXT_WHITE)
    surface.blit(caption, (title_rect.x + 10, title_rect.y + 6))

    # Fake close button
    close_rect = pygame.Rect(
        title_rect.right - 24,
        title_rect.y + 4,
        20,
        20
    )
    pygame.draw.rect(surface, (225, 60, 40), close_rect)
    draw_bevel(surface, close_rect, raised=True, thick=1)
    draw_centered_text(
        surface, "X", font_small, TEXT_WHITE, close_rect.center
    )

    return pygame.Rect(
        rect.x + 8,
        rect.y + 36,
        rect.width - 16,
        rect.height - 44
    )


def draw_xp_button(surface, rect, label, hovered=False, pressed=False, highlight=None):
    """Skeuomorphic XP push-button."""

    if pressed:
        fill = BUTTON_PRESS
    elif hovered:
        fill = BUTTON_HOVER
    else:
        fill = BUTTON_FACE

    pygame.draw.rect(surface, fill, rect)
    draw_bevel(surface, rect, raised=not pressed, thick=2)

    if highlight:
        # Colored inset ring for correct-answer feedback
        inset = rect.inflate(-6, -6)
        pygame.draw.rect(surface, highlight, inset, width=3)

    text_offset = (1, 1) if pressed else (0, 0)
    draw_centered_text(
        surface,
        label,
        font_button,
        TEXT_DARK,
        (
            rect.centerx + text_offset[0],
            rect.centery + text_offset[1]
        )
    )


def draw_inset_panel(surface, rect, fill=WINDOW_FACE_LIGHT):
    pygame.draw.rect(surface, fill, rect)
    draw_bevel(surface, rect, raised=False, thick=2)


def draw_progress_bar(surface, rect, ratio, color):
    """Classic XP chunky progress bar."""

    pygame.draw.rect(surface, (255, 255, 255), rect)
    draw_bevel(surface, rect, raised=False, thick=2)

    inner = rect.inflate(-4, -4)
    fill_w = int(inner.width * max(0.0, min(1.0, ratio)))

    if fill_w > 0:
        chunk = 10
        x = inner.x
        while x < inner.x + fill_w:
            w = min(chunk - 2, inner.x + fill_w - x)
            if w > 0:
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(x, inner.y, w, inner.height)
                )
            x += chunk


class StroopGame:

    def __init__(self):

        self.choice_rects = [
            pygame.Rect(145, 455, 335, 82),
            pygame.Rect(520, 455, 335, 82),
            pygame.Rect(145, 557, 335, 82),
            pygame.Rect(520, 557, 335, 82),
        ]

        self.restart()

    @staticmethod
    def time_for_level(level):
        """
        Level 1  = 15 seconds
        Level 50+= 1 second (floor)
        Infinite levels — never wins, only loses.
        """

        span = START_TIME - MIN_TIME
        steps = TIME_FLOOR_LEVEL - 1

        return max(
            MIN_TIME,
            START_TIME - (level - 1) * (span / steps)
        )

    def restart(self):

        self.level = 1
        self.score = 0

        self.state = "playing"
        self.end_message = ""

        self.feedback_text = ""
        self.feedback_until = 0

        self.selected_answer = None

        self.new_round()

    def new_round(self):

        names = list(COLORS.keys())

        self.word_name = random.choice(names)

        self.ink_name = random.choice(
            [name for name in names if name != self.word_name]
        )

        distractors = random.sample(
            [name for name in names if name != self.ink_name],
            3
        )

        self.choices = distractors + [self.ink_name]
        random.shuffle(self.choices)

        self.time_limit = self.time_for_level(self.level)
        self.round_started = pygame.time.get_ticks()

        self.feedback_text = ""
        self.selected_answer = None

    def remaining_time(self):

        elapsed = (
            pygame.time.get_ticks() - self.round_started
        ) / 1000

        return max(0.0, self.time_limit - elapsed)

    def submit_answer(self, answer):

        if self.state != "playing":
            return

        if self.feedback_text:
            return

        self.selected_answer = answer

        if answer == self.ink_name:

            remaining = self.remaining_time()
            speed_bonus = int(remaining * 10)

            self.score += 100 + speed_bonus
            self.feedback_text = "CORRECT!"
            self.feedback_until = pygame.time.get_ticks() + 650

        else:

            self.state = "game_over"
            self.end_message = (
                f"Wrong! The text color was {self.ink_name}."
            )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return False

            if self.state == "game_over" and event.key == pygame.K_r:
                self.restart()

            if self.state == "playing" and not self.feedback_text:

                key_to_index = {
                    pygame.K_1: 0,
                    pygame.K_2: 1,
                    pygame.K_3: 2,
                    pygame.K_4: 3,
                }

                if event.key in key_to_index:
                    index = key_to_index[event.key]
                    self.submit_answer(self.choices[index])

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.state == "playing"
            and not self.feedback_text
        ):

            for index, rect in enumerate(self.choice_rects):
                if rect.collidepoint(event.pos):
                    self.submit_answer(self.choices[index])
                    break

        return True

    def update(self):

        if self.state != "playing":
            return

        now = pygame.time.get_ticks()

        if self.feedback_text:

            if now >= self.feedback_until:
                self.level += 1
                self.new_round()

            return

        if self.remaining_time() <= 0:

            self.state = "game_over"
            self.end_message = (
                f"Time's up! The text color was {self.ink_name}."
            )

    def draw_header(self):

        # Outer app window
        window = pygame.Rect(40, 28, 920, 644)
        body = draw_xp_window(screen, window, "Stroop Sprint.exe")

        # Instructions strip
        tip = font_small.render(
            "Choose the COLOR of the text — ignore the word.  "
            "Keys 1-4 or click.  Esc = quit.",
            True,
            TEXT_MUTED
        )
        screen.blit(tip, (body.x + 8, body.y + 4))

        # Level / Score gauges (inset LCD-style panels)
        level_rect = pygame.Rect(670, 78, 125, 62)
        score_rect = pygame.Rect(815, 78, 125, 62)

        draw_inset_panel(screen, level_rect, (20, 28, 20))
        draw_inset_panel(screen, score_rect, (20, 28, 20))

        draw_centered_text(
            screen, "LEVEL", font_small, (90, 200, 90),
            (level_rect.centerx, level_rect.y + 16)
        )
        draw_centered_text(
            screen, str(self.level), font_medium, (120, 255, 120),
            (level_rect.centerx, level_rect.y + 42)
        )

        draw_centered_text(
            screen, "SCORE", font_small, (90, 200, 90),
            (score_rect.centerx, score_rect.y + 16)
        )
        draw_centered_text(
            screen, str(self.score), font_medium, (120, 255, 120),
            (score_rect.centerx, score_rect.y + 42)
        )

        # Title plaque
        plaque = pygame.Rect(60, 78, 580, 62)
        draw_inset_panel(screen, plaque, WINDOW_FACE)
        draw_centered_text(
            screen,
            "STROOP SPRINT",
            font_medium,
            TITLE_BLUE_LEFT,
            (plaque.centerx, plaque.centery - 8)
        )
        draw_centered_text(
            screen,
            "Analog reaction test  ·  Infinite mode",
            font_small,
            TEXT_MUTED,
            (plaque.centerx, plaque.centery + 16)
        )

    def draw_timer(self):

        if self.state == "playing":
            remaining = self.remaining_time()
        else:
            remaining = 0

        ratio = max(
            0.0,
            min(1.0, remaining / self.time_limit)
        )

        if ratio > 0.5:
            bar_color = TIMER_OK
        elif ratio > 0.25:
            bar_color = TIMER_WARN
        else:
            bar_color = TIMER_LOW

        # Label + inset meter
        label = font_small.render("TIME", True, TEXT_MUTED)
        screen.blit(label, (145, 372))

        bar_rect = pygame.Rect(190, 370, 665, 24)
        draw_progress_bar(screen, bar_rect, ratio, bar_color)

        time_text = font_medium.render(
            f"{remaining:04.1f}s",
            True,
            bar_color
        )
        screen.blit(time_text, (870, 368))

    def draw_question(self):

        question_rect = pygame.Rect(145, 155, 710, 200)
        draw_inset_panel(screen, question_rect, (255, 255, 250))

        # Small raised header plate
        header = pygame.Rect(
            question_rect.x + 18,
            question_rect.y + 14,
            question_rect.width - 36,
            28
        )
        pygame.draw.rect(screen, BUTTON_FACE, header)
        draw_bevel(screen, header, raised=True, thick=1)

        draw_centered_text(
            screen,
            "WHAT COLOR IS THIS TEXT?",
            font_small,
            TEXT_MUTED,
            header.center
        )

        draw_centered_text(
            screen,
            self.word_name,
            font_word,
            COLORS[self.ink_name],
            (
                question_rect.centerx,
                question_rect.centery + 28
            )
        )

    def draw_choices(self):

        mouse_position = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        for index, (choice, rect) in enumerate(
            zip(self.choices, self.choice_rects)
        ):

            can_click = (
                self.state == "playing"
                and not self.feedback_text
            )
            hovered = rect.collidepoint(mouse_position) and can_click
            pressed = hovered and mouse_down

            highlight = None
            if self.feedback_text and choice == self.ink_name:
                highlight = SUCCESS

            # Build label with number prefix for analog keypad feel
            label = f"{index + 1}   {choice}"
            draw_xp_button(
                screen,
                rect,
                label,
                hovered=hovered,
                pressed=pressed,
                highlight=highlight
            )

            # Color swatch (inset jewel)
            swatch = pygame.Rect(rect.x + 58, rect.centery - 14, 28, 28)
            if pressed:
                swatch = swatch.move(1, 1)

            pygame.draw.rect(screen, COLORS[choice], swatch)
            draw_bevel(screen, swatch, raised=False, thick=2)

    def draw_feedback(self):

        if not self.feedback_text:
            return

        plate = pygame.Rect(0, 0, 280, 56)
        plate.center = (WIDTH // 2, 365)

        pygame.draw.rect(screen, WINDOW_FACE, plate)
        draw_bevel(screen, plate, raised=True, thick=2)

        draw_centered_text(
            screen,
            self.feedback_text,
            font_overlay,
            SUCCESS,
            plate.center
        )

    def draw_end_overlay(self):

        if self.state != "game_over":
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 40, 60, 140))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(200, 180, 600, 320)
        body = draw_xp_window(
            screen,
            panel_rect,
            "Game Over - Stroop Sprint"
        )

        draw_centered_text(
            screen,
            "GAME OVER",
            font_overlay,
            DANGER,
            (panel_rect.centerx, body.y + 48)
        )

        draw_centered_text(
            screen,
            self.end_message,
            font_small,
            TEXT_DARK,
            (panel_rect.centerx, body.y + 110)
        )

        draw_centered_text(
            screen,
            f"Level reached: {self.level}    Score: {self.score}",
            font_medium,
            TEXT_DARK,
            (panel_rect.centerx, body.y + 160)
        )

        # Fake OK / Restart button
        btn = pygame.Rect(0, 0, 220, 40)
        btn.center = (panel_rect.centerx, body.y + 230)
        draw_xp_button(screen, btn, "Press R to Restart")

    def draw(self):

        screen.blit(BACKGROUND, (0, 0))

        self.draw_header()
        self.draw_question()
        self.draw_timer()
        self.draw_choices()
        self.draw_feedback()
        self.draw_end_overlay()


def main():

    game = StroopGame()
    running = True

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.handle_event(event)

        game.update()
        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
