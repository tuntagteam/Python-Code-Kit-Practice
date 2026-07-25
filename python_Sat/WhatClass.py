import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("MAHASANOOK")

clock = pygame.time.Clock()
font = pygame.font.Font(None,40)

score = 0
running = True

class Player:
    def __init__(self):
        self.x = 300
        self.y = 520
        self.width = 100
        self.height = 40
        self.speed = 7
    
    def move(self):
        keys= pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(
            screen,
            (0,0,255),
            (self.x,self.y,self.width,self.height),
        )
    
    def get_rect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)
    
class Coin:
    def __init__(self):
        self.radius = 20
        self.x = 300
        self.y = 0
        self.speed = 5
    
    def fall(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (self.x,self.y),
            self.radius
        )

    def reset(self):
        self.x = 300
        self.y = 0
    
    def get_circle(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


player = Player()
coin = Coin()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    player.move()
    coin.fall()

    screen.fill("lightblue")

    if player.get_rect().colliderect(coin.get_circle()):
        score += 1
        coin.reset()

    if coin.y > 600:
        coin.reset()

    player.draw()
    coin.draw()

    score_text = font.render("Score:" + str(score),True,(0,0,0))

    
    screen.blit(score_text, (20,20))
    pygame.display.update()
    clock.tick(60)

pygame.quit()