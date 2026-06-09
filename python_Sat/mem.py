import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Memory Game")

font = pygame.font.SysFont("arial",50)
small_font = pygame.font.SysFont("arial",30)

CARD_SIZE = 150
GAP = 30

item = ["A", "B", "C", "D","E","F"]
cards = item * 2
random.shuffle(cards)

flipped = []
matched = []

running = True

def draw_game():
    screen.fill((240,240,255))

    for i in range(16):
        row = i // 4
        col = i % 4

        x = 40 + col * (CARD_SIZE + GAP)
        y = 40 + row * (CARD_SIZE + GAP)

        rect = pygame.Rect(x,y,CARD_SIZE,CARD_SIZE)

        if i in flipped or i in matched:
            pygame.draw.rect(screen, (255,255,255), rect, border_radius=15)
            text = font.render(cards[i], True, (0,0,0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, (80,120,255), rect,border_radius=15)
        
    if len(matched) == 16:
        win_text = small_font.render("You Win!", True, (0,0,0))
        screen.blit(win_text, (230,550))

while running:
    draw_game()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
        
            for i in range(16):
                row = i // 4
                col = i % 4

                x = 40 + col * (CARD_SIZE + GAP)
                y = 40 + row * (CARD_SIZE + GAP)

                rect = pygame.Rect(x,y,CARD_SIZE,CARD_SIZE)

                if rect.collidepoint(mouse_x,mouse_y):
                    if i not in flipped and i not in matched:
                        flipped.append(i)
                    if len(flipped) == 2:
                        first = flipped[0]
                        second = flipped[1]
                        if cards[first] == cards [second]:
                            matched.append(first)
                            matched.append(second)

                        pygame.time.wait(500)
                        flipped=[]
pygame.quit()