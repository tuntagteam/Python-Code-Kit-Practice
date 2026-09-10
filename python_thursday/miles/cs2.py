from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

window.title = "Mini Counter-Strike"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

PLAYER_SPEED = 5
PLAYER_HEALTH = 100

MAG_SIZE = 30
ammo = MAG_SIZE
reserve_ammo = 90

DAMAGE = 34
FIRE_DELAY = 0.12
RELOAD_TIME = 1.4

round_number = 1
round_active = True
enemies = []
shots = []
score = 0

bomb_planted = False
bomb_timer = 45

# --------------------------------------------------
# COLORS
# --------------------------------------------------

GROUND = color.rgb(55, 60, 55)
WALL = color.rgb(100, 105, 100)
CRATE = color.rgb(120, 80, 45)
ENEMY_COLOR = color.rgb(180, 55, 45)

# --------------------------------------------------
# MAP
# --------------------------------------------------

ground = Entity(
    model='plane',
    texture='white_cube',
    texture_scale=(30, 30),
    scale=(30, 1, 30),
    color=GROUND,
    collider='box'
)

# Border walls
walls = []

def make_wall(position, scale):
    wall = Entity(
        model='cube',
        position=position,
        scale=scale,
        color=WALL,
        collider='box'
    )
    walls.append(wall)
    return wall

make_wall((0, 2, 15), (30, 4, 1))
make_wall((0, 2, -15), (30, 4, 1))
make_wall((15, 2, 0), (1, 4, 30))
make_wall((-15, 2, 0), (1, 4, 30))

# Interior walls
make_wall((0, 2, 7), (12, 4, 1))
make_wall((-7, 2, 0), (1, 4, 10))
make_wall((7, 2, -5), (1, 4, 10))

# Crates
for x, z in [
    (-4, 5), (-2, 5), (4, 10),
    (-11, -5), (10, 4),
    (3, -10), (-5, -9)
]:
    Entity(
        model='cube',
        position=(x, 1, z),
        scale=(2, 2, 2),
        color=CRATE,
        collider='box'
    )

# Bomb site
site = Entity(
    model='cube',
    position=(9, 0.03, 9),
    scale=(6, .05, 6),
    color=color.rgba(40, 100, 40, 150)
)

Text(
    text='B',
    parent=site,
    origin=(0, 0),
    scale=4,
    color=color.white
)

# --------------------------------------------------
# PLAYER
# --------------------------------------------------

player = FirstPersonController()
player.position = (-10, 2, -10)
player.speed = PLAYER_SPEED
player.gravity = 1
player.cursor.visible = False

# Player weapon
weapon = Entity(
    parent=camera,
    model='cube',
    color=color.rgb(35, 35, 35),
    scale=(.18, .12, .65),
    position=(.45, -.35, .75),
    rotation=(0, 0, 0)
)

# Weapon barrel
Entity(
    parent=weapon,
    model='cube',
    color=color.black,
    scale=(.6, .5, .25),
    position=(0, 0, .55)
)

# --------------------------------------------------
# HUD
# --------------------------------------------------

health_text = Text(
    text='HEALTH: 100',
    position=(-.86, -.44),
    scale=1.3,
    color=color.lime
)

ammo_text = Text(
    text=f'{ammo}/{reserve_ammo}',
    position=(.68, -.44),
    scale=1.3
)

round_text = Text(
    text='ROUND 1',
    origin=(0, 0),
    position=(0, .45),
    scale=1.4
)

status_text = Text(
    text='',
    origin=(0, 0),
    position=(0, .35),
    scale=1.1,
    color=color.yellow
)

score_text = Text(
    text='KILLS: 0',
    position=(-.86, .45),
    scale=1
)

# Crosshair
crosshair = Text(
    text='+',
    origin=(0, 0),
    scale=2,
    color=color.white
)

# --------------------------------------------------
# ENEMY
# --------------------------------------------------

class Enemy(Entity):

    def __init__(self, position):
        super().__init__(
            model='cube',
            position=position,
            scale=(.8, 1.8, .8),
            color=ENEMY_COLOR,
            collider='box'
        )

        self.health = 100
        self.speed = random.uniform(1.2, 1.8)
        self.attack_timer = random.uniform(1, 2)

        # Head
        self.head = Entity(
            parent=self,
            model='cube',
            y=.65,
            scale=(.65, .45, .65),
            color=color.rgb(210, 160, 120)
        )

        # Gun
        self.gun = Entity(
            parent=self,
            model='cube',
            position=(.45, .1, .25),
            scale=(.15, .15, .7),
            color=color.black
        )

    def update(self):
        if not round_active:
            return

        distance = distance_xz(self.position, player.position)

        # Move toward player
        if distance > 3:
            direction = Vec3(
                player.x - self.x,
                0,
                player.z - self.z
            )

            if direction.length() > 0:
                direction = direction.normalized()

                # Simple obstacle-aware movement
                self.position += direction * self.speed * time.dt
                self.look_at(
                    Vec3(player.x, self.y, player.z),
                    axis=Vec3.forward
                )

        # Attack player
        self.attack_timer -= time.dt

        if distance < 15 and self.attack_timer <= 0:
            self.attack_timer = random.uniform(1.2, 2.0)

            # Accuracy isn't perfect
            if random.random() < .45:
                damage_player(random.randint(8, 18))

    def take_damage(self, amount):
        global score

        self.health -= amount

        # Flash red
        self.color = color.white
        invoke(setattr, self, 'color', ENEMY_COLOR, delay=.05)

        if self.health <= 0:
            score += 1
            score_text.text = f'KILLS: {score}'
            destroy(self.head)
            destroy(self.gun)
            destroy(self)

            if self in enemies:
                enemies.remove(self)

# --------------------------------------------------
# SPAWNING
# --------------------------------------------------

spawn_positions = [
    (10, 1, 12),
    (-10, 1, 10),
    (11, 1, -10),
    (5, 1, 12),
    (-11, 1, 0),
    (10, 1, 0)
]

def spawn_enemies():
    global enemies

    for enemy in enemies:
        destroy(enemy)

    enemies.clear()

    count = min(3 + round_number, 8)

    for i in range(count):
        pos = random.choice(spawn_positions)

        # Avoid spawning exactly on another enemy
        enemies.append(Enemy(pos))

# --------------------------------------------------
# DAMAGE
# --------------------------------------------------

def damage_player(amount):
    global PLAYER_HEALTH

    PLAYER_HEALTH -= amount
    PLAYER_HEALTH = max(PLAYER_HEALTH, 0)

    health_text.text = f'HEALTH: {PLAYER_HEALTH}'

    if PLAYER_HEALTH <= 0:
        end_round(False)

# --------------------------------------------------
# SHOOTING
# --------------------------------------------------

can_shoot = True
reloading = False

def shoot():
    global ammo, can_shoot

    if not round_active or reloading:
        return

    if ammo <= 0:
        status_text.text = 'OUT OF AMMO - PRESS R'
        return

    if not can_shoot:
        return

    ammo -= 1
    update_ammo()

    can_shoot = False
    invoke(enable_shooting, delay=FIRE_DELAY)

    # Weapon recoil
    weapon.animate_position(
        (0.45, -.31, .72),
        duration=.04
    )

    weapon.animate_position(
        (.45, -.35, .75),
        duration=.08,
        delay=.04
    )

    # Raycast from camera
    hit = raycast(
        camera.world_position,
        camera.forward,
        distance=100,
        ignore=[player, weapon]
    )

    if hit.hit:
        # Bullet mark
        mark = Entity(
            model='quad',
            texture='white_cube',
            color=color.black,
            scale=.08,
            position=hit.world_point + hit.normal * .01,
            billboard=True
        )

        destroy(mark, delay=2)

        if isinstance(hit.entity, Enemy):
            hit.entity.take_damage(DAMAGE)

def enable_shooting():
    global can_shoot
    can_shoot = True

# --------------------------------------------------
# RELOAD
# --------------------------------------------------

def reload():
    global ammo, reserve_ammo, reloading

    if reloading:
        return

    if ammo >= MAG_SIZE:
        return

    if reserve_ammo <= 0:
        return

    reloading = True
    status_text.text = 'RELOADING...'

    invoke(finish_reload, delay=RELOAD_TIME)

def finish_reload():
    global ammo, reserve_ammo, reloading

    needed = MAG_SIZE - ammo
    amount = min(needed, reserve_ammo)

    ammo += amount
    reserve_ammo -= amount

    reloading = False
    status_text.text = ''

    update_ammo()

def update_ammo():
    ammo_text.text = f'{ammo}/{reserve_ammo}'

# --------------------------------------------------
# BOMB SYSTEM
# --------------------------------------------------

def plant_bomb():
    global bomb_planted, bomb_timer

    if bomb_planted:
        return

    if distance_xz(player.position, site.position) < 3.5:
        bomb_planted = True
        bomb_timer = 45
        status_text.text = 'BOMB PLANTED!'

def defuse_bomb():
    global bomb_planted

    if bomb_planted and distance_xz(player.position, site.position) < 3.5:
        bomb_planted = False
        status_text.text = 'BOMB DEFUSED!'
        invoke(clear_status, delay=2)

def clear_status():
    status_text.text = ''

# --------------------------------------------------
# ROUNDS
# --------------------------------------------------

def end_round(player_won):
    global round_active

    round_active = False

    if player_won:
        round_text.text = f'ROUND {round_number} WON!'
        round_text.color = color.lime
    else:
        round_text.text = 'ROUND LOST'
        round_text.color = color.red

    status_text.text = 'Press ENTER for next round'

def next_round():
    global round_number
    global round_active
    global PLAYER_HEALTH
    global ammo
    global reserve_ammo
    global bomb_planted
    global bomb_timer

    round_number += 1
    round_active = True

    PLAYER_HEALTH = 100
    ammo = MAG_SIZE
    reserve_ammo = 90

    bomb_planted = False
    bomb_timer = 45

    player.position = (-10, 2, -10)

    health_text.text = 'HEALTH: 100'
    update_ammo()

    round_text.text = f'ROUND {round_number}'
    round_text.color = color.white
    status_text.text = ''

    spawn_enemies()

# --------------------------------------------------
# INPUT
# --------------------------------------------------

def input(key):

    if key == 'left mouse down':
        shoot()

    if key == 'r':
        reload()

    if key == 'e':
        plant_bomb()

    if key == 'f':
        defuse_bomb()

    if key == 'enter' and not round_active:
        next_round()

    if key == 'escape':
        application.quit()

# --------------------------------------------------
# GAME UPDATE
# --------------------------------------------------

def update():

    global bomb_timer

    if not round_active:
        return

    # Bomb countdown
    if bomb_planted:
        bomb_timer -= time.dt

        status_text.text = f'BOMB: {max(0, int(bomb_timer))}'

        if bomb_timer <= 0:
            end_round(False)
            return

    # Win when all enemies are dead
    if len(enemies) == 0:
        end_round(True)

# --------------------------------------------------
# START
# --------------------------------------------------

spawn_enemies()

status_text.text = 'WASD = MOVE | LMB = SHOOT | R = RELOAD | E = PLANT'

invoke(clear_status, delay=4)

app.run()
