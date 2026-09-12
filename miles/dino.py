import pygame
import random
import sys

pygame.init()

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------
WIDTH = 1000
HEIGHT = 350

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (247, 247, 247)
DARK = (83, 83, 83)
BLACK = (25, 25, 25)

GROUND_Y = 280

FONT = pygame.font.SysFont("consolas", 22, bold=True)
SMALL_FONT = pygame.font.SysFont("consolas", 16, bold=True)


# --------------------------------------------------
# DINOSAUR
# --------------------------------------------------
class Dino:
    def __init__(self):
        self.x = 80
        self.width = 44
        self.height = 48

        self.y = GROUND_Y - self.height

        self.velocity_y = 0
        self.gravity = 0.9
        self.jump_power = -16

        self.jumping = False
        self.ducking = False

        self.animation_timer = 0
        self.run_frame = 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = self.jump_power
            self.jumping = True
            self.ducking = False

    def update(self, keys):
        self.ducking = keys[pygame.K_DOWN] and not self.jumping

        if self.jumping:
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            if self.y >= GROUND_Y - 48:
                self.y = GROUND_Y - 48
                self.velocity_y = 0
                self.jumping = False

        self.animation_timer += 1

        if self.animation_timer >= 6:
            self.run_frame = 1 - self.run_frame
            self.animation_timer = 0

    def get_rect(self):
        if self.ducking:
            return pygame.Rect(
                self.x,
                GROUND_Y - 30,
                58,
                30
            )

        return pygame.Rect(
            self.x + 5,
            self.y + 4,
            self.width - 10,
            self.height - 5
        )

    def draw(self, surface, dark_mode=False):
        color = WHITE if dark_mode else DARK

        if self.ducking:
            self.draw_duck(surface, color)
        else:
            self.draw_normal(surface, color)

    def draw_normal(self, surface, color):

        x = int(self.x)
        y = int(self.y)

        # tail
        pygame.draw.polygon(
            surface,
            color,
            [
                (x + 8, y + 30),
                (x - 10, y + 22),
                (x + 7, y + 38)
            ]
        )

        # body
        pygame.draw.rect(
            surface,
            color,
            (x + 8, y + 18, 25, 23)
        )

        # neck
        pygame.draw.rect(
            surface,
            color,
            (x + 25, y + 8, 12, 24)
        )

        # head
        pygame.draw.rect(
            surface,
            color,
            (x + 27, y, 26, 20)
        )

        # mouth opening
        background = BLACK if color == WHITE else WHITE

        pygame.draw.rect(
            surface,
            background,
            (x + 45, y + 13, 8, 4)
        )

        # eye
        pygame.draw.rect(
            surface,
            background,
            (x + 42, y + 4, 4, 4)
        )

        # arms
        pygame.draw.rect(
            surface,
            color,
            (x + 30, y + 27, 15, 5)
        )

        pygame.draw.rect(
            surface,
            color,
            (x + 41, y + 27, 4, 9)
        )

        # legs
        if self.jumping:
            pygame.draw.rect(
                surface,
                color,
                (x + 14, y + 37, 6, 11)
            )

            pygame.draw.rect(
                surface,
                color,
                (x + 27, y + 37, 6, 11)
            )

        elif self.run_frame == 0:
            pygame.draw.rect(
                surface,
                color,
                (x + 13, y + 37, 6, 11)
            )

            pygame.draw.rect(
                surface,
                color,
                (x + 26, y + 37, 9, 6)
            )

        else:
            pygame.draw.rect(
                surface,
                color,
                (x + 13, y + 37, 9, 6)
            )

            pygame.draw.rect(
                surface,
                color,
                (x + 28, y + 37, 6, 11)
            )

    def draw_duck(self, surface, color):

        x = int(self.x)
        y = GROUND_Y - 30

        background = BLACK if color == WHITE else WHITE

        # tail
        pygame.draw.polygon(
            surface,
            color,
            [
                (x + 8, y + 15),
                (x - 10, y + 8),
                (x + 8, y + 22)
            ]
        )

        # horizontal body
        pygame.draw.rect(
            surface,
            color,
            (x + 8, y + 8, 35, 18)
        )

        # head
        pygame.draw.rect(
            surface,
            color,
            (x + 35, y, 28, 18)
        )

        # eye
        pygame.draw.rect(
            surface,
            background,
            (x + 51, y + 4, 4, 4)
        )

        # legs
        if self.run_frame == 0:

            pygame.draw.rect(
                surface,
                color,
                (x + 17, y + 22, 9, 8)
            )

            pygame.draw.rect(
                surface,
                color,
                (x + 37, y + 22, 6, 5)
            )

        else:

            pygame.draw.rect(
                surface,
                color,
                (x + 19, y + 22, 6, 5)
            )

            pygame.draw.rect(
                surface,
                color,
                (x + 36, y + 22, 9, 8)
            )


# --------------------------------------------------
# CACTUS
# --------------------------------------------------
class Cactus:

    def __init__(self, speed):

        self.type = random.randint(0, 2)

        if self.type == 0:
            self.width = 20
            self.height = 45

        elif self.type == 1:
            self.width = 34
            self.height = 55

        else:
            self.width = 55
            self.height = 42

        self.x = WIDTH + 20
        self.y = GROUND_Y - self.height

        self.speed = speed

    def update(self, speed):
        self.x -= speed

    def get_rect(self):
        return pygame.Rect(
            self.x + 3,
            self.y + 3,
            self.width - 6,
            self.height - 3
        )

    def draw(self, surface, dark_mode):

        color = WHITE if dark_mode else DARK

        if self.type == 0:

            pygame.draw.rect(
                surface,
                color,
                (self.x + 7, self.y, 9, self.height)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x, self.y + 15, 8, 7)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x, self.y + 8, 5, 15)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 15, self.y + 22, 8, 7)
            )

        elif self.type == 1:

            pygame.draw.rect(
                surface,
                color,
                (self.x + 12, self.y, 11, self.height)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 3, self.y + 19, 10, 8)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 3, self.y + 10, 6, 17)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 22, self.y + 27, 11, 8)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 28, self.y + 18, 6, 17)
            )

        else:

            for offset in [0, 18, 36]:

                pygame.draw.rect(
                    surface,
                    color,
                    (self.x + offset + 4, self.y + 4, 10, self.height - 4)
                )


# --------------------------------------------------
# PTERODACTYL
# --------------------------------------------------
class Pterodactyl:

    def __init__(self):

        self.x = WIDTH + 20
        self.height = 32
        self.width = 48

        self.y = random.choice([
            GROUND_Y - 35,
            GROUND_Y - 65,
            GROUND_Y - 95
        ])

        self.frame = 0
        self.timer = 0

    def update(self, speed):

        self.x -= speed + 1

        self.timer += 1

        if self.timer >= 10:
            self.frame = 1 - self.frame
            self.timer = 0

    def get_rect(self):

        return pygame.Rect(
            self.x + 5,
            self.y + 5,
            self.width - 10,
            self.height - 10
        )

    def draw(self, surface, dark_mode):

        color = WHITE if dark_mode else DARK

        x = int(self.x)
        y = int(self.y)

        # body
        pygame.draw.rect(
            surface,
            color,
            (x + 13, y + 13, 27, 10)
        )

        # head
        pygame.draw.polygon(
            surface,
            color,
            [
                (x + 39, y + 12),
                (x + 50, y + 17),
                (x + 39, y + 20)
            ]
        )

        # wings
        if self.frame == 0:

            pygame.draw.polygon(
                surface,
                color,
                [
                    (x + 15, y + 14),
                    (x + 4, y),
                    (x + 28, y + 13)
                ]
            )

        else:

            pygame.draw.polygon(
                surface,
                color,
                [
                    (x + 15, y + 20),
                    (x + 5, y + 31),
                    (x + 30, y + 21)
                ]
            )


# --------------------------------------------------
# CLOUD
# --------------------------------------------------
class Cloud:

    def __init__(self):

        self.x = WIDTH + random.randint(0, 200)
        self.y = random.randint(40, 130)

        self.speed = random.uniform(0.5, 1.2)

    def update(self):

        self.x -= self.speed

    def draw(self, surface, dark_mode):

        color = (180, 180, 180) if not dark_mode else (100, 100, 100)

        x = int(self.x)
        y = int(self.y)

        pygame.draw.ellipse(
            surface,
            color,
            (x, y + 8, 45, 15)
        )

        pygame.draw.ellipse(
            surface,
            color,
            (x + 10, y, 25, 22)
        )


# --------------------------------------------------
# GAME
# --------------------------------------------------
def game():

    dino = Dino()

    obstacles = []
    clouds = []

    score = 0
    high_score = 0

    speed = 7

    obstacle_timer = 0
    next_obstacle = random.randint(70, 120)

    cloud_timer = 0

    game_over = False

    ground_offset = 0

    while True:

        CLOCK.tick(FPS)

        # ------------------------------------------
        # EVENTS
        # ------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if not game_over:

                    if event.key in (
                        pygame.K_SPACE,
                        pygame.K_UP
                    ):
                        dino.jump()

                else:

                    if event.key in (
                        pygame.K_SPACE,
                        pygame.K_RETURN
                    ):

                        dino = Dino()

                        obstacles.clear()
                        clouds.clear()

                        score = 0
                        speed = 7

                        obstacle_timer = 0
                        next_obstacle = random.randint(70, 120)

                        game_over = False

        keys = pygame.key.get_pressed()

        # ------------------------------------------
        # NIGHT MODE
        # ------------------------------------------

        night_cycle = int(score) // 700

        dark_mode = night_cycle % 2 == 1

        background = BLACK if dark_mode else WHITE

        SCREEN.fill(background)

        # ------------------------------------------
        # UPDATE
        # ------------------------------------------

        if not game_over:

            dino.update(keys)

            score += 0.15

            # increase game speed
            speed = 7 + min(score / 500, 8)

            # obstacle creation
            obstacle_timer += 1

            if obstacle_timer >= next_obstacle:

                # pterodactyl starts appearing later
                if score > 400 and random.random() < 0.25:
                    obstacles.append(Pterodactyl())

                else:
                    obstacles.append(Cactus(speed))

                obstacle_timer = 0

                next_obstacle = random.randint(
                    int(max(45, 85 - speed * 2)),
                    int(max(80, 135 - speed))
                )

            # clouds
            cloud_timer += 1

            if cloud_timer > random.randint(100, 180):

                clouds.append(Cloud())
                cloud_timer = 0

            # update obstacles
            for obstacle in obstacles:

                obstacle.update(speed)

            obstacles = [
                obstacle
                for obstacle in obstacles
                if obstacle.x > -100
            ]

            # update clouds
            for cloud in clouds:

                cloud.update()

            clouds = [
                cloud
                for cloud in clouds
                if cloud.x > -100
            ]

            # collision
            dino_rect = dino.get_rect()

            for obstacle in obstacles:

                if dino_rect.colliderect(
                    obstacle.get_rect()
                ):

                    game_over = True

                    high_score = max(
                        high_score,
                        int(score)
                    )

            # ground scrolling
            ground_offset -= speed

            if ground_offset <= -40:
                ground_offset = 0

        # ------------------------------------------
        # DRAW CLOUDS
        # ------------------------------------------

        for cloud in clouds:
            cloud.draw(SCREEN, dark_mode)

        # ------------------------------------------
        # GROUND
        # ------------------------------------------

        ground_color = WHITE if dark_mode else DARK

        pygame.draw.line(
            SCREEN,
            ground_color,
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            2
        )

        # little ground rocks
        for x in range(
            int(ground_offset),
            WIDTH,
            40
        ):

            pygame.draw.line(
                SCREEN,
                ground_color,
                (x, GROUND_Y + 8),
                (x + 8, GROUND_Y + 8),
                2
            )

            pygame.draw.line(
                SCREEN,
                ground_color,
                (x + 20, GROUND_Y + 13),
                (x + 25, GROUND_Y + 13),
                1
            )

        # ------------------------------------------
        # OBSTACLES
        # ------------------------------------------

        for obstacle in obstacles:
            obstacle.draw(SCREEN, dark_mode)

        # ------------------------------------------
        # DINO
        # ------------------------------------------

        dino.draw(SCREEN, dark_mode)

        # ------------------------------------------
        # SCORE
        # ------------------------------------------

        text_color = WHITE if dark_mode else DARK

        score_text = FONT.render(
            f"{int(score):05d}",
            True,
            text_color
        )

        hi_text = FONT.render(
            f"HI {high_score:05d}",
            True,
            text_color
        )

        SCREEN.blit(
            hi_text,
            (WIDTH - 230, 30)
        )

        SCREEN.blit(
            score_text,
            (WIDTH - 100, 30)
        )

        # ------------------------------------------
        # GAME OVER
        # ------------------------------------------

        if game_over:

            game_over_text = FONT.render(
                "G A M E   O V E R",
                True,
                text_color
            )

            restart_text = SMALL_FONT.render(
                "Press SPACE to restart",
                True,
                text_color
            )

            SCREEN.blit(
                game_over_text,
                (
                    WIDTH // 2 -
                    game_over_text.get_width() // 2,
                    120
                )
            )

            SCREEN.blit(
                restart_text,
                (
                    WIDTH // 2 -
                    restart_text.get_width() // 2,
                    160
                )
            )

        pygame.display.update()


game()