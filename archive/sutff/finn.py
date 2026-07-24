"""
Highway Driver — Lanes Restored, Coins + Rewarding SFX (Pygame)

Features:
- Dashed lane markers between 3 lanes (animated with scroll)
- Speed ramps up over time (independent of score)
- Spawn rate scales with current speed (keeps spacing consistent)
- Coins worth +100 points with a 2-tone chime (procedurally generated)
- Cars in normal style (rects with visor + headlights)
- Start menu with card UI and "Click to Start" button
- ESC always returns to menu
- F11 toggles fullscreen (scaled to your 480x720 logical resolution)
- Police car chases behind the player with a slight delay, flashing lights
- Realistic wee-woo siren (700–1000 Hz, 1.2 s) that only plays during gameplay
"""

import sys
import math
import random
import pygame
from io import BytesIO
import struct
import array

# --------------------------- Config --------------------------- #
WIDTH, HEIGHT = 480, 720
FPS = 60

LANES = 3
ROAD_MARGIN_LEFT = 90
ROAD_MARGIN_RIGHT = WIDTH - 90

# Lane dash visuals
LANE_MARK_DASH_H = 40
LANE_MARK_GAP = 40
LANE_MARK_WIDTH = 6

PLAYER_W, PLAYER_H = 46, 74
OBST_W, OBST_H = 46, 74
COIN_SIZE = 26

BASE_SCROLL_PPS = 260.0
MAX_SCROLL_PPS = 700.0
SPEED_GROWTH_PPS_PER_SEC = 4.0   # speed increases by this per second (independent of score)

# Spawning scaled with speed to keep spacing ~consistent
BASE_OBS_SPAWN_INTERVAL = 1.0    # seconds at BASE_SCROLL_PPS
BASE_COIN_SPAWN_INTERVAL = 0.85  # seconds at BASE_SCROLL_PPS

LANE_CHANGE_SPEED = 12.0

# Colors
BG_COLOR = (20, 22, 26)
ROAD_COLOR = (40, 44, 52)
LANE_MARK_COLOR = (225, 225, 225)
SHOULDER_COLOR = (90, 96, 112)
UI_COLOR = (245, 245, 245)
UI_DIM = (210, 210, 210)
PLAYER_COLOR = (80, 200, 255)
OBST_COLORS = [(255, 96, 96), (255, 188, 64), (64, 240, 140), (180, 128, 255), (255, 224, 80)]

CARD_BG = (32, 35, 41)
CARD_OUTLINE = (80, 86, 102)
BTN_BG = (70, 140, 255)
BTN_TEXT = (255, 255, 255)
COIN_COLOR = (255, 212, 64)
COIN_RIM = (255, 236, 140)

# ------------------------ Helpers ----------------------------- #
def lane_centers():
    road_width = ROAD_MARGIN_RIGHT - ROAD_MARGIN_LEFT
    lane_width = road_width / LANES
    return [int(ROAD_MARGIN_LEFT + lane_width * (i + 0.5)) for i in range(LANES)]

def _pack_wav(buf, sample_rate):
    data_size = len(buf) * 2
    with BytesIO() as f:
        f.write(b'RIFF'); f.write(struct.pack('<I', 36 + data_size)); f.write(b'WAVE')
        f.write(b'fmt '); f.write(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate*2, 2, 16))
        f.write(b'data'); f.write(struct.pack('<I', data_size)); f.write(buf.tobytes())
        return f.getvalue()

def make_chime_wav_bytes(sample_rate=44100):
    """Rewarding coin chime: high then low tone."""
    buf = array.array('h')
    amp = 20000
    tones = [(1240, 0.12), (880, 0.18)]
    for freq, dur in tones:
        n = int(sample_rate * dur)
        for i in range(n):
            t = i / sample_rate
            buf.append(int(amp * math.sin(2 * math.pi * freq * t)))
    return _pack_wav(buf, sample_rate)

def make_siren_wav_bytes(sample_rate=44100, f_low=700.0, f_high=1000.0, sweep_time=1.2):
    """
    Realistic 'wee-woo' wail by sweeping frequency up (wee) then down (woo).
    - No windowing/fade so the loop is continuous and strong on both ends.
    - Loop duration = 2 * sweep_time seconds.
    """
    buf = array.array('h')
    amp = 16000
    dur = 2.0 * sweep_time
    total = int(sample_rate * dur)
    half = int(sample_rate * sweep_time)

    phase = 0.0
    two_pi = 2.0 * math.pi

    for i in range(total):
        if i < half:
            # sweep up (wee)
            t = i / half
            freq = f_low + (f_high - f_low) * t
        else:
            # sweep down (woo)
            t = (i - half) / half
            freq = f_high - (f_high - f_low) * t

        phase += two_pi * freq / sample_rate
        s = int(amp * math.sin(phase))
        buf.append(s)

    return _pack_wav(buf, sample_rate)

# ------------------------ Entities ---------------------------- #
class Player:
    def __init__(self, lanes):
        self.lanes = lanes
        self.lane_index = LANES // 2
        self.x = self.lanes[self.lane_index]
        self.target_x = self.x
        self.y = HEIGHT - 130
        self.w, self.h = PLAYER_W, PLAYER_H
        self.left_pressed_prev = False
        self.right_pressed_prev = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w // 2), int(self.y - self.h // 2), self.w, self.h)

    def update(self, dt, keys):
        left_now = keys[pygame.K_LEFT]
        right_now = keys[pygame.K_RIGHT]

        if left_now and not self.left_pressed_prev:
            self.lane_index = max(0, self.lane_index - 1)
            self.target_x = self.lanes[self.lane_index]
        if right_now and not self.right_pressed_prev:
            self.lane_index = min(LANES - 1, self.lane_index + 1)
            self.target_x = self.lanes[self.lane_index]

        self.left_pressed_prev = left_now
        self.right_pressed_prev = right_now

        dx = self.target_x - self.x
        self.x += dx * min(1.0, LANE_CHANGE_SPEED * dt)

    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect, border_radius=8)
        visor = self.rect.copy().inflate(-self.w * 0.5, -self.h * 0.6)
        visor.y += 10
        pygame.draw.rect(surf, (200, 240, 255), visor, border_radius=6)
        hl = self.rect.copy().inflate(-self.w * 0.6, -self.h * 0.7)
        hl.y -= 10
        pygame.draw.rect(surf, (255, 255, 180), hl, border_radius=4)

class Obstacle:
    def __init__(self, lane_x, y, color):
        self.x = lane_x
        self.y = y
        self.w, self.h = OBST_W, OBST_H
        self.color = color

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w // 2), int(self.y - self.h // 2), self.w, self.h)

    def update(self, dt, scroll_pps):
        self.y += scroll_pps * dt

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=8)
        hl = self.rect.copy().inflate(-self.w * 0.6, -self.h * 0.7)
        hl.y -= 10
        pygame.draw.rect(surf, (255, 255, 200), hl, border_radius=4)

class Coin:
    def __init__(self, lane_x, y):
        self.x = lane_x
        self.y = y
        self.size = COIN_SIZE

    @property
    def rect(self):
        r = pygame.Rect(0, 0, self.size, self.size)
        r.center = (int(self.x), int(self.y))
        return r

    def update(self, dt, scroll_pps):
        self.y += scroll_pps * dt

    def draw(self, surf):
        pygame.draw.circle(surf, COIN_RIM, self.rect.center, self.size // 2)
        pygame.draw.circle(surf, COIN_COLOR, self.rect.center, self.size // 2 - 3)

class PoliceCar:
    """Chases the player with a slight delay (lerp) and flashing lights."""
    def __init__(self, player):
        self.w, self.h = OBST_W, OBST_H
        self.player = player
        self.y_offset = 120
        self.flash_timer = 0.0
        self.flash_state = True

        # own position for delayed steering
        self.x = player.x
        self.y = player.y + self.y_offset
        self.lerp_speed = 4.0  # lower = more delay

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w // 2), int(self.y - self.h // 2), self.w, self.h)

    def update(self, dt):
        # delayed horizontal follow
        dx = self.player.x - self.x
        self.x += dx * min(1.0, self.lerp_speed * dt)
        # keep behind vertically
        self.y = self.player.y + self.y_offset

        # lights toggle
        self.flash_timer += dt
        if self.flash_timer > 0.25:
            self.flash_timer = 0.0
            self.flash_state = not self.flash_state

    def draw(self, surf):
        r = self.rect
        # body
        pygame.draw.rect(surf, (25, 32, 80), r, border_radius=8)
        # windshield
        visor = r.copy().inflate(-self.w * 0.5, -self.h * 0.6)
        visor.y += 10
        pygame.draw.rect(surf, (190, 210, 255), visor, border_radius=6)
        # roof lights
        light_w = r.w // 2 - 6
        light_h = 10
        left_light = pygame.Rect(r.left + 4, r.top + 6, light_w, light_h)
        right_light = pygame.Rect(r.centerx - 2, r.top + 6, light_w, light_h)
        if self.flash_state:
            pygame.draw.rect(surf, (255, 50, 50), left_light, border_radius=3)
            pygame.draw.rect(surf, (50, 80, 255), right_light, border_radius=3)
        else:
            pygame.draw.rect(surf, (50, 80, 255), left_light, border_radius=3)
            pygame.draw.rect(surf, (255, 50, 50), right_light, border_radius=3)

# ------------------------ Game ------------------------------- #
class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 256)
        pygame.init()
        pygame.display.set_caption("Highway Driver")

        # Scaled window so logical 480x720 is preserved in fullscreen
        self.fullscreen = False
        self.base_flags = pygame.SCALED
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), self.base_flags)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.bigfont = pygame.font.SysFont("consolas", 44, bold=True)
        self.titlefont = pygame.font.SysFont("consolas", 52, bold=True)

        self.lanes = lane_centers()
        road_width = ROAD_MARGIN_RIGHT - ROAD_MARGIN_LEFT
        self.lane_width = road_width / LANES

        self.state = "menu"
        self.high_score = 0

        # sounds
        self.coin_sound = pygame.mixer.Sound(file=BytesIO(make_chime_wav_bytes()))
        self.siren_sound = pygame.mixer.Sound(file=BytesIO(make_siren_wav_bytes()))
        self.siren_sound.set_volume(0.3)  # quiet siren

        # dashed lane markers
        self.dashes = []
        lane_w = self.lane_width
        self._line_xs = [int(ROAD_MARGIN_LEFT + lane_w * i) for i in range(1, LANES)]
        y = -LANE_MARK_DASH_H
        while y < HEIGHT + LANE_MARK_DASH_H:
            for lx in self._line_xs:
                self.dashes.append(pygame.Rect(lx - LANE_MARK_WIDTH // 2, y, LANE_MARK_WIDTH, LANE_MARK_DASH_H))
            y += LANE_MARK_DASH_H + LANE_MARK_GAP

        self.reset_run()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        flags = self.base_flags | (pygame.FULLSCREEN if self.fullscreen else 0)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    def reset_run(self):
        self.player = Player(self.lanes)
        self.obstacles = []
        self.coins = []
        self.scroll_pps = BASE_SCROLL_PPS
        self.elapsed = 0.0
        self.obs_spawn_timer = 0.0
        self.coin_spawn_timer = 0.0
        self.score = 0.0
        self.police = PoliceCar(self.player)
        # Do NOT start siren here; only start when the game starts

    def stop_siren(self):
        try:
            self.siren_sound.stop()
        except Exception:
            pass

    # spawn cadence scales with speed
    def current_obs_spawn_interval(self):
        return BASE_OBS_SPAWN_INTERVAL * (BASE_SCROLL_PPS / max(1.0, self.scroll_pps))

    def current_coin_spawn_interval(self):
        return BASE_COIN_SPAWN_INTERVAL * (BASE_SCROLL_PPS / max(1.0, self.scroll_pps))

    # spawners
    def spawn_obstacle(self):
        lane_idx = random.randrange(LANES)
        cx = self.lanes[lane_idx]
        y = -120
        color = random.choice(OBST_COLORS)
        self.obstacles.append(Obstacle(cx, y, color))

    def spawn_coin(self):
        lanes_to_try = list(range(LANES))
        random.shuffle(lanes_to_try)
        y = -220
        for lane_idx in lanes_to_try:
            cx = self.lanes[lane_idx]
            candidate = Coin(cx, y)
            crect = candidate.rect
            # avoid cars and existing coins
            if any(crect.colliderect(ob.rect) for ob in self.obstacles):
                continue
            if any(crect.colliderect(c.rect) for c in self.coins):
                continue
            self.coins.append(candidate)
            return

    # progression
    def update_progress(self, dt):
        self.elapsed += dt
        self.scroll_pps = min(BASE_SCROLL_PPS + SPEED_GROWTH_PPS_PER_SEC * self.elapsed, MAX_SCROLL_PPS)
        self.score += (self.scroll_pps * dt) * 0.1

    # collisions
    def check_obstacle_collisions(self):
        pr = self.player.rect.inflate(-8, -10)
        for ob in self.obstacles:
            if pr.colliderect(ob.rect.inflate(-6, -12)):
                return True
        return False

    def check_coin_collisions(self):
        pr = self.player.rect.inflate(-8, -10)
        keep = []
        for c in self.coins:
            if pr.colliderect(c.rect.inflate(-6, -6)):
                self.score += 100
                try:
                    self.coin_sound.play()
                except Exception:
                    pass
            else:
                keep.append(c)
        self.coins = keep

    def remove_coins_touching_cars(self):
        keep = []
        for c in self.coins:
            crect = c.rect.inflate(-2, -4)
            if any(crect.colliderect(ob.rect.inflate(-2, -6)) for ob in self.obstacles):
                continue
            keep.append(c)
        self.coins = keep

    # lane markers animation
    def update_lane_markers(self, dt):
        dy = int(self.scroll_pps * dt)
        if dy == 0:
            return
        for r in self.dashes:
            r.y += dy
            if r.top >= HEIGHT:
                r.y -= (HEIGHT + LANE_MARK_DASH_H + LANE_MARK_GAP)

    # drawing helpers
    def draw_road(self):
        pygame.draw.rect(self.screen, ROAD_COLOR,
                         (ROAD_MARGIN_LEFT, 0, ROAD_MARGIN_RIGHT - ROAD_MARGIN_LEFT, HEIGHT),
                         border_radius=18)
        for d in self.dashes:
            pygame.draw.rect(self.screen, LANE_MARK_COLOR, d, border_radius=6)
        pygame.draw.rect(self.screen, SHOULDER_COLOR, (ROAD_MARGIN_LEFT - 10, 0, 10, HEIGHT), border_radius=8)
        pygame.draw.rect(self.screen, SHOULDER_COLOR, (ROAD_MARGIN_RIGHT, 0, 10, HEIGHT), border_radius=8)

    def draw_ui_in_game(self):
        info = f"Score: {int(self.score)}   High: {self.high_score}"
        txt = self.font.render(info, True, UI_COLOR)
        self.screen.blit(txt, (14, 12))

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        self.draw_road()

        card_w, card_h = 360, 280
        card_rect = pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(self.screen, CARD_BG, card_rect, border_radius=24)
        pygame.draw.rect(self.screen, CARD_OUTLINE, card_rect, width=2, border_radius=24)

        title = self.titlefont.render("HIGHWAY DRIVER", True, UI_COLOR)
        self.screen.blit(title, title.get_rect(center=(card_rect.centerx, card_rect.top + 60)))

        hs = self.bigfont.render(f"High Score: {self.high_score}", True, UI_COLOR)
        self.screen.blit(hs, hs.get_rect(center=(card_rect.centerx, card_rect.centery)))

        btn_rect = pygame.Rect(0, 0, 200, 50)
        btn_rect.center = (card_rect.centerx, card_rect.bottom - 40)
        pygame.draw.rect(self.screen, BTN_BG, btn_rect, border_radius=20)
        start_txt = self.font.render("Click to Start", True, BTN_TEXT)
        self.screen.blit(start_txt, start_txt.get_rect(center=btn_rect.center))

    # states
    def to_menu(self):
        self.high_score = max(self.high_score, int(self.score))
        self.state = "menu"
        self.stop_siren()

    def start_game(self):
        self.reset_run()
        self.state = "playing"
        # Start siren ONLY when gameplay starts
        try:
            self.siren_sound.stop()
            self.siren_sound.play(loops=-1)
        except Exception:
            pass

    # main loop
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_siren()
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.to_menu()
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif self.state == "menu" and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu":
                        self.start_game()

            self.update_lane_markers(dt)

            if self.state == "playing":
                keys = pygame.key.get_pressed()
                self.player.update(dt, keys)
                self.update_progress(dt)

                # spawns
                self.obs_spawn_timer += dt
                self.coin_spawn_timer += dt
                if self.obs_spawn_timer >= self.current_obs_spawn_interval():
                    self.obs_spawn_timer = 0.0
                    self.spawn_obstacle()
                if self.coin_spawn_timer >= self.current_coin_spawn_interval():
                    self.coin_spawn_timer = 0.0
                    if random.random() < 0.7:
                        self.spawn_coin()

                # updates
                for ob in self.obstacles:
                    ob.update(dt, self.scroll_pps)
                for c in self.coins:
                    c.update(dt, self.scroll_pps)
                self.police.update(dt)

                # cleanup + pickups
                self.remove_coins_touching_cars()
                self.obstacles = [o for o in self.obstacles if o.y < HEIGHT + 40]
                self.coins = [c for c in self.coins if c.y < HEIGHT + 40]
                self.check_coin_collisions()

                # crash ends run
                if self.check_obstacle_collisions():
                    self.to_menu()

            # render
            self.screen.fill(BG_COLOR)
            if self.state == "playing":
                self.draw_road()
                for ob in self.obstacles:
                    ob.draw(self.screen)
                for c in self.coins:
                    c.draw(self.screen)
                self.police.draw(self.screen)  # behind player visually
                self.player.draw(self.screen)
                self.draw_ui_in_game()
            else:
                self.draw_road()
                self.draw_menu()

            pygame.display.flip()

# ------------------------ Entry ------------------------------ #
if __name__ == "__main__":
    Game().run()
