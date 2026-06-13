import pygame
import sys

pygame.init()

# =========================
# BASIC SETUP
# =========================
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Terraria - Python Block World")

CLOCK = pygame.time.Clock()
FPS = 60

TILE_SIZE = 40
ROWS = 25
COLS = 80

FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 28, bold=True)

# =========================
# COLORS
# =========================
SKY = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (80, 80, 80)
LIGHT_GRAY = (170, 170, 170)

GRASS = (50, 180, 60)
DIRT = (139, 90, 43)
WOOD = (120, 75, 35)
LEAVES = (35, 140, 45)
WATER = (40, 120, 230)
PLAYER_COLOR = (255, 210, 80)

# =========================
# BLOCK IDS
# =========================
AIR = 0
GRASS_BLOCK = 1
DIRT_BLOCK = 2
WOOD_BLOCK = 3
LEAVES_BLOCK = 4
WATER_BLOCK = 5

BLOCK_COLORS = {
    GRASS_BLOCK: GRASS,
    DIRT_BLOCK: DIRT,
    WOOD_BLOCK: WOOD,
    LEAVES_BLOCK: LEAVES,
    WATER_BLOCK: WATER,
}

BLOCK_NAMES = {
    GRASS_BLOCK: "Grass",
    DIRT_BLOCK: "Dirt",
    WOOD_BLOCK: "Wood",
    LEAVES_BLOCK: "Leaves",
    WATER_BLOCK: "Water",
}

HOTBAR_BLOCKS = [
    GRASS_BLOCK,
    DIRT_BLOCK,
    WOOD_BLOCK,
    LEAVES_BLOCK,
    WATER_BLOCK,
]

selected_index = 0

# =========================
# WORLD GENERATION
# =========================
world = []

for row in range(ROWS):
    line = []
    for col in range(COLS):
        if row < 14:
            line.append(AIR)
        elif row == 14:
            line.append(GRASS_BLOCK)
        else:
            line.append(DIRT_BLOCK)
    world.append(line)

# Add water pond
for r in range(13, 15):
    for c in range(25, 33):
        world[r][c] = WATER_BLOCK

# Add trees
def add_tree(x, ground_y):
    # trunk
    world[ground_y - 1][x] = WOOD_BLOCK
    world[ground_y - 2][x] = WOOD_BLOCK
    world[ground_y - 3][x] = WOOD_BLOCK

    # leaves
    for r in range(ground_y - 5, ground_y - 2):
        for c in range(x - 2, x + 3):
            if 0 <= r < ROWS and 0 <= c < COLS:
                world[r][c] = LEAVES_BLOCK

    world[ground_y - 6][x] = LEAVES_BLOCK

add_tree(10, 14)
add_tree(18, 14)
add_tree(45, 14)
add_tree(60, 14)

# =========================
# PLAYER
# =========================
player = pygame.Rect(120, 200, 28, 36)
vel_x = 0
vel_y = 0
speed = 5
jump_power = -13
gravity = 0.6
on_ground = False

camera_x = 0

# =========================
# HELPER FUNCTIONS
# =========================
def is_solid(block):
    return block in [GRASS_BLOCK, DIRT_BLOCK, WOOD_BLOCK, LEAVES_BLOCK]

def get_tile_at_pixel(x, y):
    col = x // TILE_SIZE
    row = y // TILE_SIZE

    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col

    return None, None

def check_collision(rect):
    touched_tiles = []

    left = rect.left // TILE_SIZE
    right = rect.right // TILE_SIZE
    top = rect.top // TILE_SIZE
    bottom = rect.bottom // TILE_SIZE

    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            if 0 <= row < ROWS and 0 <= col < COLS:
                if is_solid(world[row][col]):
                    tile_rect = pygame.Rect(
                        col * TILE_SIZE,
                        row * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    touched_tiles.append(tile_rect)

    return touched_tiles

def draw_world():
    SCREEN.fill(SKY)

    start_col = max(0, camera_x // TILE_SIZE)
    end_col = min(COLS, start_col + WIDTH // TILE_SIZE + 3)

    for row in range(ROWS):
        for col in range(start_col, end_col):
            block = world[row][col]

            if block != AIR:
                color = BLOCK_COLORS[block]
                rect = pygame.Rect(
                    col * TILE_SIZE - camera_x,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pygame.draw.rect(SCREEN, color, rect)

                # block border
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1)

def draw_player():
    player_screen_rect = pygame.Rect(
        player.x - camera_x,
        player.y,
        player.width,
        player.height
    )

    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_screen_rect)
    pygame.draw.rect(SCREEN, BLACK, player_screen_rect, 2)

def draw_ui():
    # Top UI
    title = BIG_FONT.render("Mini Terraria", True, BLACK)
    SCREEN.blit(title, (20, 15))

    hp_text = FONT.render("HP: ♥ ♥ ♥", True, BLACK)
    SCREEN.blit(hp_text, (20, 55))

    selected_block = HOTBAR_BLOCKS[selected_index]
    selected_text = FONT.render(
        f"Selected: {BLOCK_NAMES[selected_block]}",
        True,
        BLACK
    )
    SCREEN.blit(selected_text, (20, 85))

    help_text = FONT.render(
        "A/D Move | Space Jump | Left Click Break | Right Click Place | 1-5 Select Block",
        True,
        BLACK
    )
    SCREEN.blit(help_text, (250, 20))

    # Hotbar
    box_size = 70
    start_x = WIDTH // 2 - (box_size * len(HOTBAR_BLOCKS)) // 2
    y = HEIGHT - 90

    for i, block in enumerate(HOTBAR_BLOCKS):
        x = start_x + i * box_size
        box = pygame.Rect(x, y, box_size - 8, box_size - 8)

        if i == selected_index:
            pygame.draw.rect(SCREEN, WHITE, box)
            pygame.draw.rect(SCREEN, BLACK, box, 4)
        else:
            pygame.draw.rect(SCREEN, LIGHT_GRAY, box)
            pygame.draw.rect(SCREEN, BLACK, box, 2)

        inner = pygame.Rect(x + 15, y + 10, 32, 32)
        pygame.draw.rect(SCREEN, BLOCK_COLORS[block], inner)
        pygame.draw.rect(SCREEN, BLACK, inner, 1)

        label = FONT.render(str(i + 1), True, BLACK)
        SCREEN.blit(label, (x + 25, y + 43))

def break_block(mouse_pos):
    mx, my = mouse_pos
    world_x = mx + camera_x
    world_y = my

    row, col = get_tile_at_pixel(world_x, world_y)

    if row is not None and col is not None:
        if world[row][col] != AIR:
            world[row][col] = AIR

def place_block(mouse_pos):
    mx, my = mouse_pos
    world_x = mx + camera_x
    world_y = my

    row, col = get_tile_at_pixel(world_x, world_y)

    if row is not None and col is not None:
        if world[row][col] == AIR:
            selected_block = HOTBAR_BLOCKS[selected_index]

            new_block_rect = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            # prevent placing block inside player
            if not new_block_rect.colliderect(player):
                world[row][col] = selected_block

# =========================
# GAME LOOP
# =========================
running = True

while running:
    CLOCK.tick(FPS)

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_index = 0
            elif event.key == pygame.K_2:
                selected_index = 1
            elif event.key == pygame.K_3:
                selected_index = 2
            elif event.key == pygame.K_4:
                selected_index = 3
            elif event.key == pygame.K_5:
                selected_index = 4

            if event.key == pygame.K_SPACE and on_ground:
                vel_y = jump_power

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                break_block(pygame.mouse.get_pos())

            if event.button == 3:
                place_block(pygame.mouse.get_pos())

    # -------------------------
    # PLAYER MOVEMENT
    # -------------------------
    keys = pygame.key.get_pressed()

    vel_x = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        vel_x = -speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        vel_x = speed

    # Horizontal movement
    player.x += vel_x
    collisions = check_collision(player)

    for tile in collisions:
        if vel_x > 0:
            player.right = tile.left
        elif vel_x < 0:
            player.left = tile.right

    # Gravity
    vel_y += gravity

    if vel_y > 15:
        vel_y = 15

    player.y += vel_y
    on_ground = False

    collisions = check_collision(player)

    for tile in collisions:
        if vel_y > 0:
            player.bottom = tile.top
            vel_y = 0
            on_ground = True
        elif vel_y < 0:
            player.top = tile.bottom
            vel_y = 0

    # Prevent player falling forever
    if player.y > HEIGHT + 300:
        player.x = 120
        player.y = 200
        vel_y = 0

    # -------------------------
    # CAMERA
    # -------------------------
    camera_x = player.centerx - WIDTH // 2

    max_camera = COLS * TILE_SIZE - WIDTH

    if camera_x < 0:
        camera_x = 0

    if camera_x > max_camera:
        camera_x = max_camera

    # -------------------------
    # DRAW
    # -------------------------
    draw_world()
    draw_player()
    draw_ui()

    pygame.display.update()

pygame.quit()
sys.exit()