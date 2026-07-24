import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Flappy Bird")

font = pygame.font.Font(None,48)
clock = pygame.time.Clock()
bird_x = 150
bird_y = 300
bird_size = 25
bird_speed = 0
GRAVITY = 0.4
JUMP = -8

pipe_x = 600
pipe_w = 80
pipe_gap = 200
pipe_h = random.randint(100,300)
pipe_speed = 3

score = 0
passed_pipe = False
game_over = False

running = True

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_speed = JUMP

        if game_over == False:
            bird_speed += GRAVITY
            bird_y += bird_speed
            pipe_x -= pipe_speed

        if pipe_x < -pipe_w:
             pipe_x = 800
             pipe_h = random.randint(100,300)
             passed_pipe = False
            
        if pipe_x + pipe_w < bird_x and passed_pipe == False:
             score += 1
             passed_pipe = True

        screen.fill("skyblue")
        pygame.draw.circle(screen, "yellow", (bird_x, int(bird_y)), bird_size)
        pygame.draw.rect(screen,"green",(pipe_x, 0, pipe_w, pipe_h))
        pygame.draw.rect(screen,"green",(pipe_x, pipe_h + pipe_gap, pipe_w, 600 - pipe_h - pipe_gap))

        score_text = font.render("Score: " + str(score), True, "white")
        screen.blit(score_text,(20,20))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()