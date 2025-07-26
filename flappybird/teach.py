import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

FPS = 60
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsansms",36, bold=True)

BIRD_RADIUS = 18
BIRD_START = HEIGHT // 2
GRAVITY = 0.4
FLAP_POWER = -7.5
MAX_DROP = 12

WHITE = (255, 255 ,255)
SKY = (115,197,241)
GROUND = (222,197,127)
PIPE_GREEN = (70 , 207 ,85)
PIPE_DARK = (60, 160, 70)
BIRD_YELLOW = (255, 240, 80)
BIRD_ORANGE = (255, 180, 30)
SHADOW = (100, 100, 100, 30)

BIRD_RADIUS = 18
BIRD_START = HEIGHT // 2
GRAVITY = 0.4
FLAP_POWER = -7.5
MAX_DROP = 12

PIPE_WIDTH = 65
PIPE_GAP = 150
PIPE_DIST = 250
PIPE_SPEED = 2.5

GROUND_HEIGHT = 100