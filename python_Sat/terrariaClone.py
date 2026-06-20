"""
=============================================================
   MINI TERRARIA  -  a tiny block-building game in Python
=============================================================

A little world made of blocks that you can walk around, dig,
and build in -- just like Minecraft or Terraria, but small
enough to read and understand in one file!

HOW TO RUN:
   1) Install pygame once:   pip install pygame
   2) Run the game:          python mini_terraria.py

CONTROLS:
   A / D   or  Left / Right ....... walk
   Space / W / Up ................. jump
   Left mouse button .............. break (dig) a block
   Right mouse button ............. place the selected block
   Number keys 1-7 ................ pick which block to place
   Mouse wheel .................... scroll through the blocks

THE BIG IDEA:
   The whole world is just a grid of numbers (a list of lists).
   Each number is a "block id" that says what is in that square:
   0 = air (nothing), 1 = grass, 2 = dirt, and so on.
   Drawing the game = looking at every number and drawing a
   colored square for it. That's the secret behind block games!
"""

import sys
import math
import pygame

# Start up pygame (this gets the window and graphics ready).
pygame.init()

# =============================================================
#  SETTINGS  (change these numbers to experiment!)
# =============================================================
WIDTH, HEIGHT = 1000, 640          # size of the game window in pixels
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Terraria - Python Block World")

CLOCK = pygame.time.Clock()
FPS = 60                            # how many times we update per second

TILE = 40                          # each block is 40x40 pixels
COLS = 100                         # how many blocks wide the world is
ROWS = 30                          # how many blocks tall the world is

FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 28, bold=True)

# =============================================================
#  COLORS  (red, green, blue -- each from 0 to 255)
# =============================================================
WHITE      = (255, 255, 255)
BLACK      = (25, 25, 25)
LIGHT_GRAY = (175, 175, 175)

GRASS_C  = (70, 190, 75)
DIRT_C   = (140, 95, 55)
STONE_C  = (120, 120, 130)
WOOD_C   = (125, 80, 40)
LEAVES_C = (45, 150, 55)
SAND_C   = (225, 205, 130)
WATER_C  = (55, 130, 235)
PLAYER_C = (255, 205, 70)
OUTLINE  = (0, 0, 0)               # thin line drawn around each block

# =============================================================
#  BLOCK TYPES
#  Every block has a number (its "id"), a name, a color, and
#  whether it is "solid". Solid blocks stop the player; you can
#  walk THROUGH non-solid ones (like water and air).
# =============================================================
AIR    = 0                          # air is special: it means "empty"
GRASS  = 1
DIRT   = 2
STONE  = 3
WOOD   = 4
LEAVES = 5
SAND   = 6
WATER  = 7

BLOCKS = {
    GRASS:  {"name": "Grass",  "color": GRASS_C,  "solid": True},
    DIRT:   {"name": "Dirt",   "color": DIRT_C,   "solid": True},
    STONE:  {"name": "Stone",  "color": STONE_C,  "solid": True},
    WOOD:   {"name": "Wood",   "color": WOOD_C,   "solid": True},
    LEAVES: {"name": "Leaves", "color": LEAVES_C, "solid": True},
    SAND:   {"name": "Sand",   "color": SAND_C,   "solid": True},
    WATER:  {"name": "Water",  "color": WATER_C,  "solid": False},
}

# The blocks shown in the bar at the bottom, in order (keys 1-7).
HOTBAR = [GRASS, DIRT, STONE, WOOD, LEAVES, SAND, WATER]
selected = 0                        # which hotbar slot is chosen right now

def is_solid(block):
    """True if the player should bump into this block."""
    return block != AIR and BLOCKS[block]["solid"]


# =============================================================
#  BUILD THE WORLD
# =============================================================
# First, decide the height of the ground in each column so we get
# gentle rolling hills instead of a flat, boring line. We use sine
# waves because they make nice smooth bumps.
GROUND = 16                         # the average ground row
surface = []                        # surface[col] = the grass row for that column
for col in range(COLS):
    bump = 2 * math.sin(col * 0.15) + 1 * math.sin(col * 0.06)
    surface.append(GROUND + int(round(bump)))

# Now fill the grid. For each square we ask: is it above the ground
# (air), exactly the surface (grass), just below (dirt), or deep
# down (stone)?
world = []
for row in range(ROWS):
    line = []
    for col in range(COLS):
        top = surface[col]
        if row < top:
            line.append(AIR)
        elif row == top:
            line.append(GRASS)
        elif row <= top + 4:
            line.append(DIRT)
        else:
            line.append(STONE)
    world.append(line)

# --- Dig a little pond and give it a sandy beach ---
pond_left, pond_right = 42, 50
pond_top = GROUND + 2
for col in range(pond_left, pond_right):
    surface[col] = pond_top         # remember the pond is the surface here
    for row in range(ROWS):
        if row < pond_top:
            world[row][col] = AIR
        elif row <= pond_top + 1:
            world[row][col] = WATER     # two layers of water
        elif row == pond_top + 2:
            world[row][col] = SAND      # sandy bottom
        elif row <= pond_top + 5:
            world[row][col] = DIRT
        else:
            world[row][col] = STONE
# Put sand on the banks right next to the pond for a beach look.
for col in (pond_left - 1, pond_left - 2, pond_right, pond_right + 1):
    if 0 <= col < COLS:
        world[surface[col]][col] = SAND


def add_tree(col):
    """Grow a simple tree (trunk + leafy blob) at this column."""
    if col < 3 or col >= COLS - 3:
        return
    ground = surface[col]
    # Trunk: three wood blocks going up from the ground.
    for i in range(1, 4):
        if ground - i >= 0:
            world[ground - i][col] = WOOD
    # Leaves: a 5-wide, 3-tall blob on top, plus one block at the peak.
    center = ground - 4
    for ry in range(center - 1, center + 2):
        for rx in range(col - 2, col + 3):
            if 0 <= ry < ROWS and 0 <= rx < COLS and world[ry][rx] == AIR:
                world[ry][rx] = LEAVES
    if center - 2 >= 0:
        world[center - 2][col] = LEAVES

# Plant a few trees (we skip the pond area on purpose).
for tree_col in (10, 16, 24, 34, 60, 72, 88):
    add_tree(tree_col)


# =============================================================
#  THE PLAYER
# =============================================================
# The player is a rectangle. We track its speed in x and y.
spawn_col = 5
player = pygame.Rect(spawn_col * TILE + 6, (surface[spawn_col] - 4) * TILE, 26, 36)

vel_x = 0                # left/right speed
vel_y = 0               # up/down speed (gravity changes this)
SPEED = 5               # how fast we walk
JUMP_POWER = -13        # how hard we jump (negative = upward)
GRAVITY = 0.6           # pulls the player down a little each frame
MAX_FALL = 16           # never fall faster than this
on_ground = False
facing = 1              # 1 = looking right, -1 = looking left

# These two timers make jumping feel nice and forgiving:
#  - coyote time: you can still jump for a few frames after walking
#    off a ledge (named after cartoon coyotes hanging in the air!).
#  - jump buffer: if you press jump just BEFORE landing, we remember
#    it and jump the instant you touch the ground.
coyote_timer = 0
jump_buffer = 0
COYOTE_FRAMES = 7
BUFFER_FRAMES = 7

# The camera is the part of the world we can see. It smoothly
# follows the player. We use floats so the movement is buttery.
camera_x = 0.0
camera_y = 0.0

REACH = 5               # how many blocks away you can dig/build


# =============================================================
#  COLLISION  (stopping the player from walking through blocks)
# =============================================================
def solid_tiles_touching(rect):
    """Return rectangles for every solid block the player overlaps."""
    tiles = []
    left   = rect.left // TILE
    right  = rect.right // TILE
    top    = rect.top // TILE
    bottom = rect.bottom // TILE
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            if 0 <= row < ROWS and 0 <= col < COLS and is_solid(world[row][col]):
                tiles.append(pygame.Rect(col * TILE, row * TILE, TILE, TILE))
    return tiles


# =============================================================
#  DIGGING AND BUILDING
# =============================================================
def mouse_to_tile():
    """Turn the mouse position into a (row, col) in the world grid."""
    mx, my = pygame.mouse.get_pos()
    col = int((mx + camera_x) // TILE)
    row = int((my + camera_y) // TILE)
    return row, col

def within_reach(row, col):
    """True if a block is close enough to the player to interact with."""
    prow = player.centery // TILE
    pcol = player.centerx // TILE
    return abs(row - prow) <= REACH and abs(col - pcol) <= REACH

def break_block():
    row, col = mouse_to_tile()
    if 0 <= row < ROWS and 0 <= col < COLS and within_reach(row, col):
        if world[row][col] != AIR:
            world[row][col] = AIR       # turn the block into empty air

def place_block():
    row, col = mouse_to_tile()
    if 0 <= row < ROWS and 0 <= col < COLS and within_reach(row, col):
        if world[row][col] == AIR:      # only build into empty space
            block_rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
            if not block_rect.colliderect(player):   # don't trap ourselves!
                world[row][col] = HOTBAR[selected]


# =============================================================
#  DRAWING
# =============================================================
def make_sky():
    """Make a pretty sky that fades from light blue to a deeper blue."""
    sky = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(155 + (110 - 155) * t)
        g = int(215 + (175 - 215) * t)
        b = int(245 + (235 - 245) * t)
        pygame.draw.line(sky, (r, g, b), (0, y), (WIDTH, y))
    return sky

SKY_IMAGE = make_sky()              # made once, then reused every frame

def draw_block(block, sx, sy):
    """Draw one block at screen position (sx, sy) with a little detail."""
    if block == GRASS:
        pygame.draw.rect(SCREEN, DIRT_C, (sx, sy, TILE, TILE))       # dirt body
        pygame.draw.rect(SCREEN, GRASS_C, (sx, sy, TILE, 13))        # green top
    elif block == WOOD:
        pygame.draw.rect(SCREEN, WOOD_C, (sx, sy, TILE, TILE))
        grain = (95, 58, 28)
        pygame.draw.line(SCREEN, grain, (sx + 13, sy), (sx + 13, sy + TILE), 2)
        pygame.draw.line(SCREEN, grain, (sx + 27, sy), (sx + 27, sy + TILE), 2)
    elif block == LEAVES:
        pygame.draw.rect(SCREEN, LEAVES_C, (sx, sy, TILE, TILE))
        light = (75, 175, 80)
        pygame.draw.circle(SCREEN, light, (sx + 12, sy + 14), 4)
        pygame.draw.circle(SCREEN, light, (sx + 28, sy + 26), 4)
    elif block == WATER:
        pygame.draw.rect(SCREEN, WATER_C, (sx, sy, TILE, TILE))
        pygame.draw.rect(SCREEN, (95, 165, 245), (sx, sy, TILE, 7))  # shiny top
        return                                                       # no outline
    else:
        pygame.draw.rect(SCREEN, BLOCKS[block]["color"], (sx, sy, TILE, TILE))
    pygame.draw.rect(SCREEN, OUTLINE, (sx, sy, TILE, TILE), 1)        # tidy edge

def draw_world():
    SCREEN.blit(SKY_IMAGE, (0, 0))
    # Only draw the blocks we can actually see (this keeps the game fast).
    start_col = max(0, int(camera_x) // TILE)
    end_col   = min(COLS, start_col + WIDTH // TILE + 3)
    start_row = max(0, int(camera_y) // TILE)
    end_row   = min(ROWS, start_row + HEIGHT // TILE + 3)
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            block = world[row][col]
            if block != AIR:
                draw_block(block, col * TILE - int(camera_x), row * TILE - int(camera_y))

def draw_highlight():
    """Draw an outline around the block the mouse is pointing at."""
    row, col = mouse_to_tile()
    if 0 <= row < ROWS and 0 <= col < COLS:
        sx = col * TILE - int(camera_x)
        sy = row * TILE - int(camera_y)
        color = WHITE if within_reach(row, col) else (120, 120, 120)
        pygame.draw.rect(SCREEN, color, (sx, sy, TILE, TILE), 2)

def draw_player():
    sx = player.x - int(camera_x)
    sy = player.y - int(camera_y)
    body = pygame.Rect(sx, sy, player.width, player.height)
    pygame.draw.rect(SCREEN, PLAYER_C, body)
    pygame.draw.rect(SCREEN, BLACK, body, 2)
    # Two little eyes that look the way the player is moving.
    eye_y = sy + 11
    if facing >= 0:
        ex1, ex2 = sx + 13, sx + 20
    else:
        ex1, ex2 = sx + 6, sx + 13
    pygame.draw.circle(SCREEN, WHITE, (ex1, eye_y), 4)
    pygame.draw.circle(SCREEN, WHITE, (ex2, eye_y), 4)
    pygame.draw.circle(SCREEN, BLACK, (ex1 + facing, eye_y), 2)
    pygame.draw.circle(SCREEN, BLACK, (ex2 + facing, eye_y), 2)

def draw_heart(cx, cy):
    c = (225, 70, 80)
    pygame.draw.circle(SCREEN, c, (cx - 5, cy - 3), 6)
    pygame.draw.circle(SCREEN, c, (cx + 5, cy - 3), 6)
    pygame.draw.polygon(SCREEN, c, [(cx - 11, cy - 1), (cx + 11, cy - 1), (cx, cy + 12)])

def hotbar_rect():
    """Where the bottom block bar sits on the screen."""
    box, pad = 64, 6
    total = len(HOTBAR) * (box + pad) - pad
    x = WIDTH // 2 - total // 2
    y = HEIGHT - box - 14
    return pygame.Rect(x, y, total, box)

def draw_ui():
    # Title and a few decorative hearts up top.
    SCREEN.blit(BIG_FONT.render("Mini Terraria", True, BLACK), (20, 12))
    for i in range(3):
        draw_heart(36 + i * 30, 62)

    name = BLOCKS[HOTBAR[selected]]["name"]
    SCREEN.blit(FONT.render("Selected: " + name, True, BLACK), (20, 84))

    SCREEN.blit(FONT.render(
        "A/D move  -  Space jump  -  Left click dig  -  Right click build  -  1-7 / wheel pick",
        True, BLACK), (250, 18))

    # The hotbar: one box per block, with the chosen one highlighted.
    bar = hotbar_rect()
    box, pad = 64, 6
    for i, block in enumerate(HOTBAR):
        x = bar.x + i * (box + pad)
        slot = pygame.Rect(x, bar.y, box, box)
        if i == selected:
            pygame.draw.rect(SCREEN, WHITE, slot)
            pygame.draw.rect(SCREEN, BLACK, slot, 4)
        else:
            pygame.draw.rect(SCREEN, LIGHT_GRAY, slot)
            pygame.draw.rect(SCREEN, BLACK, slot, 2)
        # A little picture of the block inside the box.
        draw_block(block, x + 16, bar.y + 10)
        SCREEN.blit(FONT.render(str(i + 1), True, BLACK), (x + 6, bar.y + 40))


# =============================================================
#  THE GAME LOOP  (this runs ~60 times every second)
# =============================================================
running = True
while running:
    CLOCK.tick(FPS)                 # keep a steady, smooth speed

    # ---- 1. Handle input (key presses and mouse clicks) ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Number keys 1-7 pick a block from the hotbar.
            if pygame.K_1 <= event.key <= pygame.K_7:
                slot = event.key - pygame.K_1
                if slot < len(HOTBAR):
                    selected = slot
            # Jump keys just REMEMBER that we want to jump (the buffer).
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                jump_buffer = BUFFER_FRAMES

        elif event.type == pygame.MOUSEWHEEL:
            # Scroll the wheel to move through the hotbar (wraps around).
            selected = (selected - event.y) % len(HOTBAR)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Ignore clicks on the hotbar so we don't dig by accident.
            if not hotbar_rect().collidepoint(event.pos):
                if event.button == 1:
                    break_block()
                elif event.button == 3:
                    place_block()

    # ---- 2. Move left and right ----
    keys = pygame.key.get_pressed()
    vel_x = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        vel_x = -SPEED
        facing = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        vel_x = SPEED
        facing = 1

    player.x += vel_x
    for tile in solid_tiles_touching(player):
        if vel_x > 0:               # moving right -> stop at the block's left side
            player.right = tile.left
        elif vel_x < 0:             # moving left -> stop at the block's right side
            player.left = tile.right

    # ---- 3. Gravity and up/down movement ----
    vel_y += GRAVITY
    if vel_y > MAX_FALL:
        vel_y = MAX_FALL

    player.y += vel_y
    on_ground = False
    for tile in solid_tiles_touching(player):
        if vel_y > 0:               # falling -> land on top of the block
            player.bottom = tile.top
            vel_y = 0
            on_ground = True
        elif vel_y < 0:             # jumping up -> bonk the block above
            player.top = tile.bottom
            vel_y = 0

    # ---- 4. Friendly jumping (coyote time + buffer) ----
    if on_ground:
        coyote_timer = COYOTE_FRAMES
    else:
        coyote_timer = max(0, coyote_timer - 1)

    if jump_buffer > 0 and coyote_timer > 0:
        vel_y = JUMP_POWER          # leap!
        jump_buffer = 0
        coyote_timer = 0
        on_ground = False
    jump_buffer = max(0, jump_buffer - 1)

    # ---- 5. If you fall off the world, respawn safely ----
    if player.top > ROWS * TILE + 200:
        player.x = spawn_col * TILE + 6
        player.y = (surface[spawn_col] - 4) * TILE
        vel_y = 0

    # ---- 6. Move the camera smoothly toward the player ----
    target_x = player.centerx - WIDTH // 2
    target_y = player.centery - HEIGHT // 2
    camera_x += (target_x - camera_x) * 0.12
    camera_y += (target_y - camera_y) * 0.12
    # Keep the camera inside the world so we never see past the edges.
    camera_x = max(0, min(camera_x, COLS * TILE - WIDTH))
    camera_y = max(0, min(camera_y, ROWS * TILE - HEIGHT))

    # ---- 7. Draw everything (order matters: back to front) ----
    draw_world()
    draw_highlight()
    draw_player()
    draw_ui()
    pygame.display.update()

# When the loop ends, close the window cleanly.
pygame.quit()
sys.exit()