from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from math import floor
import random
import os

# -------------------- App / Window --------------------
app = Ursina(title="PaceCraft", vsync=False)
window.color = color.rgb(135, 206, 235)   # sky blue
Sky()
mouse.visible = False
application.frame_rate = 120
fps_text = Text(text='FPS: 0', position=(-.87, .45), background=True)

# -------------------- World Settings --------------------
CHUNK_SIZE = 64
TERRAIN_SCALE = 80
TERRAIN_HEIGHT = 14
SEA_LEVEL = 4
noise = PerlinNoise(octaves=3, seed=random.randint(0, 999_999))

# Optional: try to load an atlas if it's actually correct; otherwise we run color-only.
atlas = None
if os.path.exists('atlas.png'):
    try:
        atlas = load_texture('atlas.png')
    except Exception:
        atlas = None

# UV tile mapping only used if atlas is valid
TILE_COUNT = 16
TILE_SIZE = 1 / TILE_COUNT
UV_POSITIONS = {
    'grass_top': (0, 0),
    'grass_side': (1, 0),
    'dirt': (2, 0),
    'water': (0, 1),
    'wood': (3, 0),
    'leaves': (4, 0),
}

def get_uvs(tile_x, tile_y):
    u = tile_x * TILE_SIZE
    v = 1 - (tile_y + 1) * TILE_SIZE
    return [(u, v), (u + TILE_SIZE, v), (u + TILE_SIZE, v + TILE_SIZE), (u, v + TILE_SIZE)]

def get_block_uvs(block, face):
    if atlas is None:
        # we won't use UVs without a texture, but return a placeholder of correct length
        return [(0,0)] * 4
    if block == 'grass':
        if face == 'top':
            return get_uvs(*UV_POSITIONS['grass_top'])
        elif face == 'bottom':
            return get_uvs(*UV_POSITIONS['dirt'])
        else:
            return get_uvs(*UV_POSITIONS['grass_side'])
    return get_uvs(*UV_POSITIONS.get(block, UV_POSITIONS['dirt']))

# -------------------- Blocks --------------------
BLOCK_TYPES = ['grass', 'dirt', 'water', 'wood', 'leaves']
selected_block = 'water'

# Per-block per-vertex tints (water slightly transparent)
BLOCK_COLORS = {
    'grass': color.rgb(106, 169, 100),
    'dirt': color.rgb(123, 87, 58),
    'water': color.rgba(64, 128, 255, 180),
    'wood': color.rgb(140, 100, 60),
    'leaves': color.rgb(80, 170, 80),
}

# -------------------- World Data --------------------
# Store blocks in dict keyed by (x,y,z)
blocks = {}

def create_block(x, y, z, block_type):
    blocks[(x, y, z)] = block_type

def destroy_block(x, y, z):
    blocks.pop((x, y, z), None)

# -------------------- Mesh Builder (with occlusion + per-vertex color) --------------------
def build_mesh():
    verts, tris, uvs, cols = [], [], [], []
    vc = 0

    for (x, y, z), block in blocks.items():
        # neighbor positions for occlusion
        neighbors = {
            'top':    (x, y+1, z),
            'bottom': (x, y-1, z),
            'north':  (x, y, z+1),
            'south':  (x, y, z-1),
            'east':   (x+1, y, z),
            'west':   (x-1, y, z),
        }
        # face vertices + UVs
        face_defs = {
            'top': (
                [Vec3(0,1,0), Vec3(1,1,0), Vec3(1,1,1), Vec3(0,1,1)],
                get_block_uvs(block, 'top')
            ),
            'bottom': (
                [Vec3(0,0,0), Vec3(1,0,0), Vec3(1,0,1), Vec3(0,0,1)],
                get_block_uvs(block, 'bottom')
            ),
            'north': (
                [Vec3(0,0,1), Vec3(1,0,1), Vec3(1,1,1), Vec3(0,1,1)],
                get_block_uvs(block, 'side')
            ),
            'south': (
                [Vec3(0,0,0), Vec3(0,1,0), Vec3(1,1,0), Vec3(1,0,0)],
                get_block_uvs(block, 'side')
            ),
            'east': (
                [Vec3(1,0,0), Vec3(1,0,1), Vec3(1,1,1), Vec3(1,1,0)],
                get_block_uvs(block, 'side')
            ),
            'west': (
                [Vec3(0,0,0), Vec3(0,0,1), Vec3(0,1,1), Vec3(0,1,0)],
                get_block_uvs(block, 'side')
            ),
        }

        face_color = BLOCK_COLORS.get(block, color.white)

        for face_name, (face_verts, face_uvs) in face_defs.items():
            if neighbors.get(face_name) not in blocks:
                for v in face_verts:
                    verts.append(Vec3(x, y, z) + v)
                tris.extend([vc, vc+1, vc+2, vc, vc+2, vc+3])
                uvs.extend(face_uvs)
                cols.extend([face_color, face_color, face_color, face_color])
                vc += 4

    # When no texture, Mesh will still render using per-vertex colors
    mesh = Mesh(vertices=verts, triangles=tris, uvs=uvs, colors=cols, mode='triangle')
    return mesh

# -------------------- Chunk Entity --------------------
chunk_entity = Entity(model=None, texture=atlas, collider='mesh')  # atlas is None-safe here

def generate_terrain():
    for x in range(CHUNK_SIZE):
        for z in range(CHUNK_SIZE):
            n = noise([x / TERRAIN_SCALE, z / TERRAIN_SCALE])
            # height from noise
            h = int((n + 1) * 0.5 * TERRAIN_HEIGHT) + 2
            for y in range(h):
                if y <= SEA_LEVEL:
                    create_block(x, y, z, 'water')
                elif y == h - 1:
                    create_block(x, y, z, 'grass')
                else:
                    create_block(x, y, z, 'dirt')

generate_terrain()

def update_chunk():
    mesh = build_mesh()
    chunk_entity.model = mesh
    chunk_entity.collider = mesh

update_chunk()

# -------------------- Player / UI --------------------
player = FirstPersonController()
player.position = (CHUNK_SIZE / 2, TERRAIN_HEIGHT + 6, CHUNK_SIZE / 2)
player.cursor = Entity(parent=camera.ui, model='quad', scale=0.01, color=color.black)

hotbar = Text(
    text='1: Grass  2: Dirt  3: Water  4: Wood  5: Leaves',
    position=(-0.8, -0.45),
    scale=1.5,
    background=True
)

# -------------------- Crosshair Highlight (shadow overlay) --------------------
highlight_shadow = Entity(
    model='cube',
    color=color.rgba(0, 0, 0, 80),  # translucent shadow
    scale=0.25,                     # slightly bigger to avoid z-fighting
    enabled=False
)

def get_target_positions():
    """
    Return (break_pos, place_pos) based on current mouse raycast.
    break_pos is the block you are looking at.
    place_pos is the adjacent block position along the hit normal.
    """
    if mouse.hovered_entity != chunk_entity or mouse.world_point is None or mouse.normal is None:
        return None, None
    p = mouse.world_point
    n = mouse.normal
    break_pos = (floor(p.x), floor(p.y), floor(p.z))
    place_pos = (floor(p.x + n.x), floor(p.y + n.y), floor(p.z + n.z))
    return break_pos, place_pos

def update_highlight():
    break_pos, _ = get_target_positions()
    if break_pos and break_pos in blocks:
        bx, by, bz = break_pos
        highlight_shadow.position = (bx + 0.5, by + 0.5, bz + 0.5)
        highlight_shadow.enabled = True
    else:
        highlight_shadow.enabled = False

# -------------------- Input --------------------
def input(key):
    global selected_block

    if key in ['1', '2', '3', '4', '5']:
        idx = int(key) - 1
        if 0 <= idx < len(BLOCK_TYPES):
            selected_block = BLOCK_TYPES[idx]
            hotbar.text = f"Selected block: {selected_block.capitalize()}"

    if key == 'left mouse down':  # destroy
        if mouse.hovered_entity == chunk_entity:
            break_pos, _ = get_target_positions()
            if break_pos and break_pos in blocks:
                destroy_block(*break_pos)
                update_chunk()
                update_highlight()

    if key == 'right mouse down':  # place
        if mouse.hovered_entity == chunk_entity:
            _, place_pos = get_target_positions()
            if place_pos:
                # avoid placing inside player body cell
                if place_pos != (floor(player.x), floor(player.y), floor(player.z)):
                    create_block(*place_pos, selected_block)
                    update_chunk()
                    update_highlight()

# -------------------- Game Loop --------------------
def update():
    # Show FPS
    fps_text.text = f'FPS: {int(1 / time.dt) if time.dt else 0}'
    # Track highlight every frame
    update_highlight()

app.run()