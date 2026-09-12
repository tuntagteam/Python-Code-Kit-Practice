import pygame
import math
import random
import colorsys

pygame.init()

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Match Wheel")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 52)

# Wheel settings
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 + 20

WHEEL_RADIUS = 250
WHEEL_WIDTH = 40

SELECTOR_RADIUS = 15

# Game settings
ROUND_TIME = 10
score = 0

dragging = False
game_over = False


def hue_to_rgb(hue):
    """
    Convert hue from 0-360 into an RGB color.
    """

    hue_normalized = hue / 360

    red, green, blue = colorsys.hsv_to_rgb(
        hue_normalized,
        1,
        1
    )

    return (
        int(red * 255),
        int(green * 255),
        int(blue * 255)
    )


def random_target():
    """
    Create a random target hue.
    """

    return random.randint(0, 359)


def angle_difference(angle1, angle2):
    """
    Find the smallest difference between two angles.
    """

    difference = abs(angle1 - angle2)

    return min(
        difference,
        360 - difference
    )


def mouse_to_hue(mouse_x, mouse_y):
    """
    Convert the mouse position into a hue angle.
    """

    dx = mouse_x - CENTER_X
    dy = mouse_y - CENTER_Y

    angle = math.degrees(math.atan2(dy, dx))

    # Convert angle so 0 degrees starts at the top
    hue = (angle + 90) % 360

    return hue


def selector_position(hue):
    """
    Get the selector position from the hue angle.
    """

    angle = math.radians(hue - 90)

    x = CENTER_X + math.cos(angle) * WHEEL_RADIUS
    y = CENTER_Y + math.sin(angle) * WHEEL_RADIUS

    return int(x), int(y)


def draw_color_wheel():
    """
    Draw the rainbow wheel using many small lines.
    """

    for hue in range(360):
        angle = math.radians(hue - 90)

        color = hue_to_rgb(hue)

        inner_radius = WHEEL_RADIUS - WHEEL_WIDTH // 2
        outer_radius = WHEEL_RADIUS + WHEEL_WIDTH // 2

        inner_x = CENTER_X + math.cos(angle) * inner_radius
        inner_y = CENTER_Y + math.sin(angle) * inner_radius

        outer_x = CENTER_X + math.cos(angle) * outer_radius
        outer_y = CENTER_Y + math.sin(angle) * outer_radius

        pygame.draw.line(
            screen,
            color,
            (inner_x, inner_y),
            (outer_x, outer_y),
            4
        )


def draw_color_box(x, y, color, title):
    """
    Draw a color preview box.
    """

    pygame.draw.circle(
        screen,
        color,
        (x, y),
        70
    )

    pygame.draw.circle(
        screen,
        (40, 40, 40),
        (x, y),
        70,
        4
    )

    title_surface = font.render(
        title,
        True,
        (30, 30, 30)
    )

    title_rect = title_surface.get_rect(
        center=(x, y + 100)
    )

    screen.blit(title_surface, title_rect)


def reset_round():
    global target_hue
    global selected_hue
    global start_time
    global game_over

    target_hue = random_target()
    selected_hue = random.randint(0, 359)

    start_time = pygame.time.get_ticks()

    game_over = False


reset_round()

running = True

while running:
    clock.tick(60)

    screen.fill((245, 245, 245))

    current_time = pygame.time.get_ticks()

    elapsed_time = (
        current_time - start_time
    ) / 1000

    time_left = max(
        0,
        ROUND_TIME - elapsed_time
    )

    # --------------------
    # Events
    # --------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            selector_x, selector_y = selector_position(
                selected_hue
            )

            distance_to_selector = math.hypot(
                mouse_x - selector_x,
                mouse_y - selector_y
            )

            if distance_to_selector <= 30:
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        if event.type == pygame.MOUSEMOTION:

            if dragging and not game_over:

                mouse_x, mouse_y = event.pos

                selected_hue = mouse_to_hue(
                    mouse_x,
                    mouse_y
                )

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:

                difference = angle_difference(
                    selected_hue,
                    target_hue
                )

                if difference <= 12:
                    score += 1

                game_over = True

            if event.key == pygame.K_RETURN and game_over:
                reset_round()

    # --------------------
    # Timer
    # --------------------

    if time_left <= 0 and not game_over:
        game_over = True

    # --------------------
    # Draw wheel
    # --------------------

    draw_color_wheel()

    selected_color = hue_to_rgb(
        selected_hue
    )

    target_color = hue_to_rgb(
        target_hue
    )

    # Draw selector
    selector_x, selector_y = selector_position(
        selected_hue
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (selector_x, selector_y),
        SELECTOR_RADIUS + 5
    )

    pygame.draw.circle(
        screen,
        (30, 30, 30),
        (selector_x, selector_y),
        SELECTOR_RADIUS + 5,
        3
    )

    pygame.draw.circle(
        screen,
        selected_color,
        (selector_x, selector_y),
        SELECTOR_RADIUS
    )

    # Target and selected colors
    draw_color_box(
        170,
        230,
        target_color,
        "Target Color"
    )

    draw_color_box(
        WIDTH - 170,
        230,
        selected_color,
        "Your Color"
    )

    # --------------------
    # UI
    # --------------------

    title_surface = big_font.render(
        "Color Match Wheel",
        True,
        (30, 30, 30)
    )

    title_rect = title_surface.get_rect(
        center=(WIDTH // 2, 45)
    )

    screen.blit(title_surface, title_rect)

    timer_surface = font.render(
        f"Time: {time_left:.1f}",
        True,
        (220, 50, 50)
    )

    screen.blit(
        timer_surface,
        (30, 30)
    )

    score_surface = font.render(
        f"Score: {score}",
        True,
        (30, 30, 30)
    )

    screen.blit(
        score_surface,
        (WIDTH - 150, 30)
    )

    instruction_surface = font.render(
        "Drag the selector and press SPACE to submit",
        True,
        (60, 60, 60)
    )

    instruction_rect = instruction_surface.get_rect(
        center=(WIDTH // 2, HEIGHT - 45)
    )

    screen.blit(
        instruction_surface,
        instruction_rect
    )

    # --------------------
    # Result
    # --------------------

    if game_over:

        difference = angle_difference(
            selected_hue,
            target_hue
        )

        if difference <= 12:

            result_text = "Correct!"

        else:

            result_text = (
                f"Not quite! Difference: {int(difference)}°"
            )

        result_surface = big_font.render(
            result_text,
            True,
            (20, 20, 20)
        )

        result_rect = result_surface.get_rect(
            center=(WIDTH // 2, CENTER_Y)
        )

        background_rect = result_rect.inflate(
            40,
            30
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            background_rect,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            (30, 30, 30),
            background_rect,
            3,
            border_radius=15
        )

        screen.blit(
            result_surface,
            result_rect
        )

        continue_surface = font.render(
            "Press ENTER for the next round",
            True,
            (30, 30, 30)
        )

        continue_rect = continue_surface.get_rect(
            center=(WIDTH // 2, CENTER_Y + 70)
        )

        screen.blit(
            continue_surface,
            continue_rect
        )

    pygame.display.flip()

pygame.quit()