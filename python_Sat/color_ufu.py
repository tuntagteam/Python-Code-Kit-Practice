import pygame
import random

pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Colour Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("None", 80)
fontSmall = pygame.font.SysFont("None", 30)
message_font = pygame.font.SysFont("None", 40)

colors = {
    "red": (255, 87, 51),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (40, 180, 99),
    "light blue": (0, 176, 240),
    "blue": (0, 102, 204),
    "purple": (142, 68, 173)
}

color_names = list(colors.keys())

display_word = random.choice(color_names)

font_color_name = random.choice(color_names)
font_color = colors[font_color_name]

user_text = ""
score = 0
running = True
is_incorrect = False
feedback_message = ""
level = 1
timeleft = 10
start_ticks = pygame.time.get_ticks() 

box_rect = pygame.Rect(100, 100, 440, 120)
button_rect = pygame.Rect(250, 500, 140, 50)

def new_color():
    global display_word, font_color_name, font_color
    display_word = random.choice(color_names)
    font_color_name = random.choice(color_names)
    font_color = colors[font_color_name]


def messagebox(message):
    text_surface = message_font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=box_rect.center)
    screen.blit(text_surface, text_rect)


def set_timer(level):
    global timeleft
    if level > 9:
        timeleft = 3
    elif level >= 5:
        timeleft = 4
    elif level > 3:
        timeleft = 6
    else:
        timeleft = 10

def levelUp(score):
    global level
    if score % 5 == 0:
        level += 1
        
    

def draw_feedback():
    if feedback_message:
        text_surface = message_font.render(
            feedback_message,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=(320, 430)
        )

        screen.blit(text_surface, text_rect)


def correct():
    global feedback_message,start_ticks
    feedback_message = "Correct!"
    start_ticks = pygame.time.get_ticks() 
    new_color()


def incorrect():
    global is_incorrect, feedback_message

    feedback_message = "Incorrect!"
    is_incorrect = True


def restart_game():
    global score, is_incorrect, feedback_message, user_text, level, timeleft

    new_color()

    score = 0
    is_incorrect = False
    feedback_message = ""
    user_text = ""
    level = 1
    timeleft = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                if not is_incorrect:
                    if user_text.lower().strip() == font_color_name:
                        score += 1
                        levelUp(score)
                        set_timer(level)
                        correct()
                    else:
                        incorrect()
                    user_text = ""

            elif event.unicode.isprintable():
                if not is_incorrect:
                    user_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_incorrect:
                if restart_button.collidepoint(event.pos):
                    restart_game()

    if not is_incorrect:
        screen.fill("cyan")
    else:
        screen.fill("red")

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    countdown = max(0, timeleft - seconds_passed)

    score_text = fontSmall.render(
        "Score: " + str(score),
        True,
        "white"
    )

    level_text = fontSmall.render(
        "Level: " + str(level),
        True,
        "white"
    )

    score_rect = score_text.get_rect(
        topright=(screen.get_width() - 20, 20)
    )

    level_rect = level_text.get_rect(
        topright=(screen.get_width() - 20, 40)
    )

    screen.blit(score_text, score_rect)
    screen.blit(level_text,level_rect)

    if not is_incorrect:
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            box_rect
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            box_rect,
            3
        )

        messagebox(user_text)


        text_surface = font.render(
            display_word,
            True,
            font_color
        )
        timetext_surface = font.render(f"Time: {int(countdown)}s", True, (255, 255, 255))

        text_rect = text_surface.get_rect(
            center=(320, 320)
        )
        screen.blit(text_surface, text_rect)
        screen.blit(timetext_surface, (50, 50))
        draw_feedback()
    else:

        draw_feedback()

        restart_button = pygame.draw.rect(
            screen,
            (255, 255, 255),
            button_rect
        )

        restart_text = fontSmall.render(
            "RESTART",
            True,
            "black"
        )

        restart_text_rect = restart_text.get_rect(
            center=restart_button.center
        )

        screen.blit(
            restart_text,
            restart_text_rect
        )
    pygame.display.flip()
    clock.tick(60)
pygame.quit()