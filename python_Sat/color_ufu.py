import pygame
import random

pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Colour Game")

font = pygame.font.SysFont("None", 80)
fontSmall = pygame.font.SysFont("None",30)
message_font = pygame.font.SysFont("None", 40)

color_palette = [
    (255, 87, 51),    # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (40, 180, 99),    # Green
    (0, 176, 240),    # Light Blue
    (0, 102, 204),    # Blue
    (142, 68, 173)    # Purple  
]


text_color = random.choice(color_palette)
current_color = random.choice(color_palette)
if current_color == (255, 87, 51):
    color_name = "red"
elif current_color == (255, 165, 0):
    color_name = "orange"
elif current_color == (255, 255, 0):
    color_name = "yellow"
elif current_color == (40, 180, 99):
    color_name = "green"
elif current_color == (0, 176, 240):
    color_name = "light blue"
elif current_color == (0, 102, 204):
    color_name = "blue"
elif current_color == (142, 68, 173):
    color_name = "purple"


is_incorrect = False

user_text = ""
box_rect = pygame.Rect(100, 100, 440, 120)
score = 0 
running = True
feedback_message = ""

ans = ["red", "green", "blue", "yellow", "orange", "purple", "light blue"]

def new_color():
    global current_color, text_color, color_name
    current_color = random.choice(color_palette)
    text_color = random.choice(color_palette)

    if current_color == (255, 87, 51):
        color_name = "red"
    elif current_color == (255, 165, 0):
        color_name = "orange"
    elif current_color == (255, 255, 0):
        color_name = "yellow"
    elif current_color == (40, 180, 99):
        color_name = "green"
    elif current_color == (0, 176, 240):
        color_name = "light blue"
    elif current_color == (0, 102, 204):
        color_name = "blue"
    elif current_color == (142, 68, 173):
        color_name = "purple"

def messagebox(message):
    text_surface = message_font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=box_rect.center)
    screen.blit(text_surface, text_rect)


def draw_feedback():
    if feedback_message:
        text_surface = message_font.render(feedback_message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.centery + 180))
        screen.blit(text_surface, text_rect)


def correct():
    global feedback_message
    feedback_message = "Correct!"
    new_color()


def incorrect():
    global is_incorrect
    global feedback_message
    feedback_message = "Incorrect!"
    is_incorrect = True

def restart_game():
    global score
    global is_incorrect
    print("Restart Clicked")
    new_color()
    is_incorrect = False
    score = 0

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
                if user_text.lower()  == color_name:
                    correct()
                    new_color()
                    score += 1
                else:
                    incorrect()
                user_text = ""
            elif event.unicode.isprintable():
                user_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_incorrect and restart_buttonza.collidepoint(event.pos):
                restart_game()

    text_surface = font.render(
        color_name,
        True,
        text_color
    )

    screen.fill("cyan")
    restart = fontSmall.render("RESTART", True, "black")
    button_rect = pygame.Rect(250, 500, 140, 50)
    
    score_text = font.render("Score: " + str(score), True, "white")
    score_rect = score_text.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(score_text, score_rect)
    
    messagebox(user_text)
    draw_feedback()
    if is_incorrect == True:
        restart_buttonza = pygame.draw.rect(screen, (255, 255, 255), button_rect)
        textrestart_rect = restart.get_rect(center=restart_buttonza.center)
        screen.blit(restart, textrestart_rect)
    else:
        pygame.draw.rect(screen, (255, 255, 255), box_rect)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 3)
        screen.blit(text_surface, (150, 280))
        messagebox(user_text)
    pygame.display.flip()

pygame.quit()