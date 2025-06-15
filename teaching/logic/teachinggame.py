import pygame
import random

WIDTH, HEIGHT = 700, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nǐ hǎo shìjiè")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial" ,48 ,bold=True)

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 20
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - 70
player_speed = 8

balls = []
misses = 0
max_miss = 3
score = 0

def spawn_ball():
    return {
        "x" : random.randint(20, WIDTH - 20),
        "y" : -20,
        "radius" : 20,
        "color" : [(0, 204, 204)],
        "speed" : 4,
    }

balls.append(spawn_ball())
game_over = False

running = True

while running:
    clock.tick(FPS)
    screen.fill((102, 0, 51))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    py.game.draw.circle(screen, (255,153,153), player_rect)