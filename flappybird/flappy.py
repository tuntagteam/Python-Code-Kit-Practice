import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
SKY = (115, 197, 241)
GROUND = (222, 197, 127)
PIPE_GREEN = (70, 207, 85)
PIPE_DARK = (60, 160, 70)
BIRD_YELLOW = (255, 240, 80)
BIRD_ORANGE = (255, 180, 30)
SHADOW = (100, 100, 100, 30)

FPS = 60
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsansms", 36, bold=True)

# Bird settings
BIRD_RADIUS = 18
BIRD_START = HEIGHT // 2
GRAVITY = 0.4
FLAP_POWER = -7.5
MAX_DROP = 12

# Pipe settings
PIPE_WIDTH = 65
PIPE_GAP = 150
PIPE_DIST = 250
PIPE_SPEED = 2.5

# Ground settings
GROUND_HEIGHT = 100

def draw_background(win):
    win.fill(SKY)
    for i in range(3):
        pygame.draw.ellipse(win, WHITE, (60 + 110*i, 80 + 10*i, 80, 40))
    pygame.draw.circle(win, (255,255,180), (WIDTH-60, 80), 32)
    pygame.draw.rect(win, GROUND, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    for i in range(0, WIDTH, 20):
        pygame.draw.rect(win, (120, 200, 60), (i, HEIGHT-GROUND_HEIGHT, 14, 20))

def draw_bird(win, x, y, frame=0, angle=0):
    bird_surface = pygame.Surface((BIRD_RADIUS*2+10, BIRD_RADIUS*2+10), pygame.SRCALPHA)
    cx, cy = BIRD_RADIUS+5, BIRD_RADIUS+5
    # Shadow
    pygame.draw.circle(bird_surface, (90,90,90,100), (cx+7, cy+16), BIRD_RADIUS-3)
    # Body
    pygame.draw.circle(bird_surface, BIRD_YELLOW, (cx, cy), BIRD_RADIUS)
    # Belly
    pygame.draw.ellipse(bird_surface, (255,255,255), (cx-11, cy+8, 22, 9))
    # Beak
    pygame.draw.polygon(bird_surface, BIRD_ORANGE, [(cx+BIRD_RADIUS-2, cy), (cx+BIRD_RADIUS+12, cy-5), (cx+BIRD_RADIUS+12, cy+5)])
    # Eye
    pygame.draw.circle(bird_surface, (255,255,255), (cx+8, cy-6), 6)
    pygame.draw.circle(bird_surface, (0,0,0), (cx+11, cy-6), 2)
    # Wing
    flap = 12 * math.sin(frame/5)
    pygame.draw.ellipse(bird_surface, (210,170,20), (cx-14, cy+2-flap, 28, 12))
    # Spin the whole bird
    rot = pygame.transform.rotate(bird_surface, angle)
    rect = rot.get_rect(center=(x, y))
    win.blit(rot, rect)

def draw_pipe(win, x, gap_y):
    pygame.draw.rect(win, PIPE_DARK, (x, gap_y+PIPE_GAP, PIPE_WIDTH, HEIGHT-gap_y-PIPE_GAP-GROUND_HEIGHT))
    pygame.draw.rect(win, PIPE_GREEN, (x+3, gap_y+PIPE_GAP, PIPE_WIDTH-6, HEIGHT-gap_y-PIPE_GAP-GROUND_HEIGHT))
    pygame.draw.rect(win, PIPE_GREEN, (x-6, gap_y+PIPE_GAP-14, PIPE_WIDTH+12, 16))
    pygame.draw.rect(win, PIPE_DARK, (x, 0, PIPE_WIDTH, gap_y))
    pygame.draw.rect(win, PIPE_GREEN, (x+3, 0, PIPE_WIDTH-6, gap_y))
    pygame.draw.rect(win, PIPE_GREEN, (x-6, gap_y-2, PIPE_WIDTH+12, 16))

def draw_score(win, score):
    surf = FONT.render(str(score), True, (255,255,255))
    win.blit(surf, (WIDTH//2 - surf.get_width()//2, 40))

def draw_gameover(win, score, best):
    msg = "GAME OVER"
    surf = FONT.render(msg, True, (230,60,60))
    win.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2-60))
    surf2 = FONT.render(f"Score: {score}", True, (90,60,60))
    win.blit(surf2, (WIDTH//2 - surf2.get_width()//2, HEIGHT//2-10))
    surf3 = FONT.render(f"Best: {best}", True, (80,160,80))
    win.blit(surf3, (WIDTH//2 - surf3.get_width()//2, HEIGHT//2+35))
    inst = pygame.font.SysFont("comicsansms", 20).render("Press SPACE to Restart", True, (90,90,90))
    win.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT//2+80))

def bird_death_animation(win, pipes, bird_x, bird_y, bird_frame):
    """Animation: bird falls and spins, pipes stop moving"""
    vel = 2
    angle = 0
    dead_time = 45  # frames
    for i in range(dead_time):
        clock.tick(FPS)
        draw_background(win)
        # Draw pipes (not moving)
        for pipe_x, gap_y, _ in pipes:
            draw_pipe(win, pipe_x, gap_y)
        # Draw bird spinning and falling
        angle += 12
        vel += GRAVITY*2
        bird_y += vel
        draw_bird(win, bird_x, int(bird_y), bird_frame+i, angle)
        pygame.display.update()
    return bird_y

def main():
    bird_x = 90
    bird_y = BIRD_START
    bird_vel = 0
    bird_dead = False
    bird_frame = 0

    pipes = []
    for i in range(3):
        gap_y = random.randint(90, HEIGHT-GROUND_HEIGHT-PIPE_GAP-80)
        pipes.append([WIDTH+200+i*PIPE_DIST, gap_y, False])

    score = 0
    best = 0
    running = True
    started = False
    death_animation_played = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not bird_dead:
                    bird_vel = FLAP_POWER
                    started = True
                if event.key == pygame.K_SPACE and bird_dead:
                    main()

        if not started and not bird_dead:
            draw_background(WIN)
            draw_bird(WIN, bird_x, int(bird_y), bird_frame)
            draw_score(WIN, score)
            inst = pygame.font.SysFont("comicsansms", 23).render("Press SPACE to start!", True, (120,120,120))
            WIN.blit(inst, (WIDTH//2-inst.get_width()//2, HEIGHT//2-40))
            pygame.display.update()
            bird_frame += 1
            continue

        bird_vel += GRAVITY
        bird_vel = min(bird_vel, MAX_DROP)
        bird_y += bird_vel
        bird_frame += 1

        # Move pipes
        for pipe in pipes:
            pipe[0] -= PIPE_SPEED

        # New pipes
        if pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)
            gap_y = random.randint(90, HEIGHT-GROUND_HEIGHT-PIPE_GAP-80)
            pipes.append([pipes[-1][0]+PIPE_DIST, gap_y, False])

        # Score check: if pipe passed the bird and not yet scored
        for pipe in pipes:
            if not pipe[2] and pipe[0] + PIPE_WIDTH < bird_x:
                score += 1
                pipe[2] = True

        # Collision check
        bird_rect = pygame.Rect(bird_x-BIRD_RADIUS+6, bird_y-BIRD_RADIUS+6, BIRD_RADIUS*2-12, BIRD_RADIUS*2-12)
        hit = False
        for pipe_x, gap_y, _ in pipes:
            pipe_rects = [
                pygame.Rect(pipe_x, 0, PIPE_WIDTH, gap_y),
                pygame.Rect(pipe_x, gap_y+PIPE_GAP, PIPE_WIDTH, HEIGHT-gap_y-PIPE_GAP-GROUND_HEIGHT)
            ]
            for rect in pipe_rects:
                if bird_rect.colliderect(rect):
                    hit = True
        if bird_y+BIRD_RADIUS > HEIGHT-GROUND_HEIGHT or bird_y-BIRD_RADIUS < 0:
            hit = True

        # --- Play death animation ONCE ---
        if hit and not death_animation_played:
            bird_dead = True
            if score > best:
                best = score
            # Play animation!
            bird_y = bird_death_animation(WIN, pipes, bird_x, bird_y, bird_frame)
            death_animation_played = True

        # Draw everything
        draw_background(WIN)
        for pipe_x, gap_y, _ in pipes:
            draw_pipe(WIN, pipe_x, gap_y)
        # If dead, draw bird crashed on ground
        if bird_dead and death_animation_played:
            draw_bird(WIN, bird_x, min(int(bird_y), HEIGHT-GROUND_HEIGHT-BIRD_RADIUS), bird_frame, 90)
        else:
            draw_bird(WIN, bird_x, int(bird_y), bird_frame)
        draw_score(WIN, score)

        if bird_dead and death_animation_played:
            draw_gameover(WIN, score, best)
            pygame.display.update()
            continue

        pygame.display.update()

if __name__ == "__main__":
    main()
