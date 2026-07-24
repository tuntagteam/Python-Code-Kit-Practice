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

def draw_background(win):
    win.fill(SKY)
    for i in range(3):
        pygame.draw.ellipse(win, WHITE, (60 + 110*i, 80 + 10*i, 80, 40))
    pygame.draw.circle(win, (255,255,180) , (WIDTH-60,80),32)
    pygame.draw.rect(win, GROUND, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    for i in range(0, WIDTH, 20):
        pygame.draw.rect(win, (120,200,60), (i, HEIGHT - GROUND_HEIGHT,14,20))

def draw_bird(win, x, y, frame=0, angle=0):
    bird_surface = pygame.Surface((BIRD_RADIUS*2+10, BIRD_RADIUS*2+10), pygame.SRCALPHA)
    cx, cy = BIRD_RADIUS+5, BIRD_RADIUS+5
    #shadow
    pygame.draw.circle(bird_surface, (90,90,90,100), (cx ,cy), BIRD_RADIUS)
    #body
    pygame.draw.circle(bird_surface, BIRD_YELLOW, (cx,cy), BIRD_RADIUS)
    #belly
    pygame.draw.ellipse(bird_surface, (255,255,255), (cx-11, cy+8, 22, 9))
    #beak
    pygame.draw.polygon(bird_surface, BIRD_ORANGE, [(cx+BIRD_RADIUS-2, cy), 
                                                    (cx+BIRD_RADIUS+12, cy-5), 
                                                    (cx+BIRD_RADIUS+12, cy+5)])
    #eye
    pygame.draw.circle(bird_surface, (255,255,255), (cx+8, cy-6), 6)
    pygame.draw.circle(bird_surface, (0,0,0), (cx+11, cy-6), 2)
    #wing
    flap=12*math.sin(frame/5)
    pygame.draw.ellipse(bird_surface, (210,170,20), (cx-14, cy+2-flap,28,12))
    #spinbirdwhen died
    rot = pygame.transform.rotate(bird_surface, angle)
    rect = rot.get_rect(center=(x,y))
    win.blit(rot, rect)

def main():
    running = True
    frame = 0
    bird_x = WIDTH // 3
    bird_y = BIRD_START

    while running:
        clock.tick(FPS) 
        frame += 1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_background(WIN)
        draw_bird(WIN, bird_x, bird_y, frame, angle=0)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()