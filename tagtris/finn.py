import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 10
FALL_TIME = 500
HIGH_SCORE_FILE = "highscore.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tetromino shapes and colors
SHAPES = {
    "I": ([[1, 1, 1, 1]], (0, 255, 255)),
    "O": ([[1, 1], [1, 1]], (255, 255, 0)),
    "T": ([[0, 1, 0], [1, 1, 1]], (128, 0, 128)),
    "Z": ([[1, 1, 0], [0, 1, 1]], (255, 0, 0)),
    "S": ([[0, 1, 1], [1, 1, 0]], (0, 255, 0)),
    "L": ([[1, 0, 0], [1, 1, 1]], (255, 165, 0)),
    "J": ([[0, 0, 1], [1, 1, 1]], (0, 0, 255))
}

class Tetromino:
    def __init__(self):
        self.shape_name, (self.shape, self.color) = random.choice(list(SHAPES.items()))
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            if block:
                pygame.draw.rect(screen, block, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_tetromino(screen, tetromino, ghost=False, time_ms=0):
    color = tetromino.color
    if ghost:
        pulse = (math.sin(time_ms / 100.0) + 1) / 2
        brightness = 0.10 + 0.30 * pulse
        color = tuple(min(255, int(c * brightness)) for c in color)

    for y, row in enumerate(tetromino.shape):
        for x, block in enumerate(row):
            if block:
                pygame.draw.rect(
                    screen,
                    color,
                    ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )

def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_menu(screen, high_score):
    screen.fill(BLACK)
    font = pygame.font.SysFont("Arial", 32)
    title = font.render("TETRIS", True, WHITE)
    prompt = font.render("Click to Start", True, WHITE)
    hs_font = pygame.font.SysFont("Arial", 24)
    hs_text = hs_font.render(f"High Score: {high_score}", True, WHITE)

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 260))
    screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 320))
    pygame.display.flip()

def check_collision(board, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, block in enumerate(row):
            if block:
                board_x = tetromino.x + x
                board_y = tetromino.y + y
                if board_x < 0 or board_x >= SCREEN_WIDTH // BLOCK_SIZE or board_y >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if board_y >= 0 and board[board_y][board_x]:
                    return True
    return False

def place_tetromino(board, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, block in enumerate(row):
            if block:
                board[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = SCREEN_HEIGHT // BLOCK_SIZE - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
    return new_board, lines_cleared

def get_ghost_position(board, tetromino):
    ghost = Tetromino()
    ghost.shape = [row[:] for row in tetromino.shape]
    ghost.color = tetromino.color
    ghost.x = tetromino.x
    ghost.y = tetromino.y

    while not check_collision(board, ghost):
        ghost.y += 1
    ghost.y -= 1
    return ghost

def calculate_score(lines):
    if lines == 1:
        return 100
    elif lines == 2:
        return 300
    elif lines == 3:
        return 500
    elif lines >= 4:
        return 800
    return 0

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    high_score = load_high_score()
    score = 0
    game_state = "menu"

    board = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    current_tetromino = Tetromino()
    fall_time = 0

    running = True
    while running:
        time_ms = pygame.time.get_ticks()
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    high_score = 0
                    save_high_score(0)

                if game_state == "playing":
                    if event.key == pygame.K_LEFT:
                        current_tetromino.x -= 1
                        if check_collision(board, current_tetromino):
                            current_tetromino.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_tetromino.x += 1
                        if check_collision(board, current_tetromino):
                            current_tetromino.x -= 1
                    elif event.key == pygame.K_UP:
                        current_tetromino.rotate()
                        if check_collision(board, current_tetromino):
                            for _ in range(3):
                                current_tetromino.rotate()
                    elif event.key == pygame.K_SPACE:
                        ghost = get_ghost_position(board, current_tetromino)
                        current_tetromino.y = ghost.y
                        place_tetromino(board, current_tetromino)
                        board, lines_cleared = clear_lines(board)
                        score += calculate_score(lines_cleared)
                        current_tetromino = Tetromino()
                        if check_collision(board, current_tetromino):
                            if score > high_score:
                                high_score = score
                                save_high_score(high_score)
                            game_state = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game_state == "menu":
                    game_state = "playing"
                    score = 0
                    board = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
                    current_tetromino = Tetromino()

        if game_state == "menu":
            draw_menu(screen, high_score)
        elif game_state == "playing":
            draw_board(screen, board)
            draw_score(screen, score)
            font = pygame.font.SysFont("Arial", 24)
            hs_text = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(hs_text, (10, 40))

            ghost_tetromino = get_ghost_position(board, current_tetromino)
            draw_tetromino(screen, ghost_tetromino, ghost=True, time_ms=time_ms)
            draw_tetromino(screen, current_tetromino)

            fall_time += clock.get_time()
            if fall_time >= FALL_TIME:
                current_tetromino.y += 1
                if check_collision(board, current_tetromino):
                    current_tetromino.y -= 1
                    place_tetromino(board, current_tetromino)
                    board, lines_cleared = clear_lines(board)
                    score += calculate_score(lines_cleared)
                    current_tetromino = Tetromino()
                    if check_collision(board, current_tetromino):
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                        game_state = "menu"
                fall_time = 0

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
#mmmmmmmmmmmmeeeeeeeeeeeeeeeeeeeeoooooooooooooooooooowwwwwwwwwwwwwwwwwwww