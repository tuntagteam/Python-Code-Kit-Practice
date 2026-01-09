import random
import pygame
# Initialize Pygame
pygame.init()
# Create a game window
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Catch the Falling Object")
# Set up the basket
basket = pygame.Rect(200, 450, 100, 20)
# Set up the falling object
falling_object = pygame.Rect(250, 0, 20, 20)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket.x -= 5
    if keys[pygame.K_RIGHT]:
        basket.x += 5

    falling_object.y += 2
    if falling_object.colliderect(basket):
        print("You caught it!")
        falling_object.y = 0
        falling_object.x = random.randint(0, 480)

    if falling_object.y > 500:
        falling_object.y = 0
        falling_object.x = random.randint(0, 480)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), basket)
    pygame.draw.rect(screen, (255, 0, 0), falling_object)
    pygame.display.update()