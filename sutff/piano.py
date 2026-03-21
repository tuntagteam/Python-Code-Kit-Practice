# Controls:
#  - LOWER whites (C3..B3): Z X C V B N M
#  - UPPER whites (C4..F5): A S D F G H J K L ; '
#  - Lower blacks: 1 2   4 5 6   8 9
#  - Upper blacks: W E   T Y U   O P
#  - [ and ] : Octave down / up (C3..C6)  (you can also use , and .)
#  - F2    : Toggle scale highlight (C Major  ↔  A Minor)
#  - Space : Sustain on/off   |   Shift: louder (velocity)
#  - F1    : Show/Hide HELP overlay   |   Esc: quit
# Requires: pip install pygame numpy

import pygame
import numpy as np
import math

# ---------------- Audio Setup ----------------
SR = 44100
pygame.mixer.pre_init(SR, -16, 1, 512)
pygame.init()
pygame.mixer.set_num_channels(32)  # polyphony

# ---------------- Window/UI Setup ----------------
# Base (unscaled) sizes
BASE_H = 520
BASE_WHITE_KEY_W = 96
BASE_WHITE_KEY_H = 280
BASE_BLACK_KEY_W = 60
BASE_BLACK_KEY_H = 168
BASE_PIANO_LEFT = 60
BASE_PIANO_TOP = 140

# Live (scaled) sizes – set by apply_scale()
H = BASE_H
WHITE_KEY_W = BASE_WHITE_KEY_W
WHITE_KEY_H = BASE_WHITE_KEY_H
BLACK_KEY_W = BASE_BLACK_KEY_W
BLACK_KEY_H = BASE_BLACK_KEY_H
PIANO_LEFT = BASE_PIANO_LEFT
PIANO_TOP = BASE_PIANO_TOP

# initial scale and flags
scale = 1.0
fullscreen = False

# Compute dynamic width from white keys; set window (resizable)
W = PIANO_LEFT * 2 + WHITE_KEY_W * 18  # updated after layouts
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Piano – 2 octaves | F1 Help | [ ] Octave | Space Sustain | F2 Scale | -/= Resize | F11 Fullscreen")

# Fonts (will be refreshed on scale changes)
font = pygame.font.SysFont(None, 28)
font_big = pygame.font.SysFont(None, 36)

# Controls (no conflicts with play keys)
HELP_TOGGLE = pygame.K_F1
SCALE_TOGGLE = pygame.K_F2
SUSTAIN_TOGGLE = pygame.K_SPACE
OCT_DOWN = pygame.K_LEFTBRACKET
OCT_UP = pygame.K_RIGHTBRACKET
OCT_DOWN2 = pygame.K_COMMA
OCT_UP2 = pygame.K_PERIOD
SIZE_DOWN = pygame.K_MINUS
SIZE_UP = pygame.K_EQUALS
FULLSCREEN_TOGGLE = pygame.K_F11
show_help = False


def apply_scale(new_scale: float | None = None, new_h: int | None = None):
    global scale, H, WHITE_KEY_W, WHITE_KEY_H, BLACK_KEY_W, BLACK_KEY_H, PIANO_LEFT, PIANO_TOP, W, font, font_big, screen
    if new_scale is not None:
        scale = max(0.6, min(2.0, new_scale))
    if new_h is not None:
        # derive scale from height
        scale = max(0.6, min(2.0, new_h / BASE_H))
    # apply
    H = int(BASE_H * scale)
    WHITE_KEY_W = int(BASE_WHITE_KEY_W * scale)
    WHITE_KEY_H = int(BASE_WHITE_KEY_H * scale)
    BLACK_KEY_W = int(BASE_BLACK_KEY_W * scale)
    BLACK_KEY_H = int(BASE_BLACK_KEY_H * scale)
    PIANO_LEFT = int(BASE_PIANO_LEFT * scale)
    PIANO_TOP = int(BASE_PIANO_TOP * scale)
    # width depends on number of white keys (after layouts are defined len(WHITE_LAYOUT) is available)
    num_white = 18  # default before layouts init; will be reset later
    try:
        num_white = len(WHITE_LAYOUT)
    except NameError:
        pass
    W = PIANO_LEFT * 2 + WHITE_KEY_W * num_white
    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen = pygame.display.set_mode((W, H), flags)
    font = pygame.font.SysFont(None, max(18, int(28 * scale)))
    font_big = pygame.font.SysFont(None, max(22, int(36 * scale)))

# ---------------- Synth Helpers ----------------
# Very lightweight piano-ish additive synth with envelope + gentle low-pass

def midi_to_freq(m: int) -> float:
    return 440.0 * (2.0 ** ((m - 69) / 12.0))

# Cache generated sounds so we don't rebuild every key press
_sound_cache: dict[tuple[int, int], pygame.mixer.Sound] = {}

def make_piano_sound(midi_note: int, velocity: float = 1.0, seconds: float = 1.6) -> pygame.mixer.Sound:
    key = (midi_note, int(velocity * 100))
    if key in _sound_cache:
        return _sound_cache[key]

    f = midi_to_freq(midi_note)
    t = np.linspace(0, seconds, int(SR * seconds), False)

    # Additive partials (fundamental + a few harmonics) with slight detune for warmth
    # Coefficients loosely inspired by piano spectra (not physical modeling)
    partials = [
        (1.00, 1.00),  # (multiplier, amplitude)
        (2.01, 0.55),
        (3.00, 0.35),
        (4.02, 0.25),
        (5.00, 0.18),
    ]
    wave = np.zeros_like(t)
    for mul, amp in partials:
        wave += amp * np.sin(2 * math.pi * (f * mul) * t)

    # Simple exponential decay envelope (quick attack, then decay + sustain tail)
    attack = max(0.004, 0.002 + (0.0005 * (72 - midi_note)))  # slightly quicker for higher notes
    attack_samples = max(1, int(SR * attack))
    env = np.ones_like(t)
    env[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Decay to ~0.35 in ~0.35s, then long tail
    decay_time = 0.35
    sustain_level = 0.35
    start = attack_samples
    decay_samples = int(SR * decay_time)
    if start + decay_samples < env.size:
        env[start:start + decay_samples] = np.linspace(1, sustain_level, decay_samples)
        env[start + decay_samples:] = sustain_level * np.exp(-3.0 * (t[start + decay_samples:] - t[start + decay_samples]))

    # Gentle one-pole low-pass to soften brightness
    alpha = 0.12
    lp = np.zeros_like(wave)
    for i in range(1, wave.size):
        lp[i] = lp[i-1] + alpha * (wave[i] - lp[i-1])

    out = lp * env

    # Normalize and apply velocity
    out /= max(1e-9, np.max(np.abs(out)))
    out *= np.clip(velocity, 0.05, 1.0)

    snd = pygame.sndarray.make_sound((out * 32767).astype(np.int16))
    _sound_cache[key] = snd
    return snd

# ---------------- Keyboard Mapping ----------------
# Two-octave layout (left = C3..B3 on Z-row, right = C4..F5 on A-row)
WHITE_LAYOUT = [
    (pygame.K_z, -12),  # C3
    (pygame.K_x, -10),  # D3
    (pygame.K_c, -8),   # E3
    (pygame.K_v, -7),   # F3
    (pygame.K_b, -5),   # G3
    (pygame.K_n, -3),   # A3
    (pygame.K_m, -1),   # B3
    (pygame.K_a, 0),    # C4
    (pygame.K_s, 2),    # D4
    (pygame.K_d, 4),    # E4
    (pygame.K_f, 5),    # F4
    (pygame.K_g, 7),    # G4
    (pygame.K_h, 9),    # A4
    (pygame.K_j, 11),   # B4
    (pygame.K_k, 12),   # C5
    (pygame.K_l, 14),   # D5
    (pygame.K_SEMICOLON, 16),  # E5
    (pygame.K_QUOTE, 17),      # F5
]

BLACK_LAYOUT = [
    # Lower octave blacks using number row
    (pygame.K_1, -11),  # C#3
    (pygame.K_2, -9),   # D#3
    (pygame.K_4, -6),   # F#3
    (pygame.K_5, -4),   # G#3
    (pygame.K_6, -2),   # A#3
    (pygame.K_8, 1),    # C#4 (between C4 and D4)
    (pygame.K_9, 3),    # D#4
    # Upper octave blacks using QWERTY row
    (pygame.K_w, 1),    # C#4
    (pygame.K_e, 3),    # D#4
    (pygame.K_t, 6),    # F#4
    (pygame.K_y, 8),    # G#4
    (pygame.K_u, 10),   # A#4
    (pygame.K_o, 13),   # C#5
    (pygame.K_p, 15),   # D#5
]

apply_scale(scale)

# positions of white keys left-to-right
white_positions = list(range(len(WHITE_LAYOUT)))
# indices of white keys where a black key sits to the right of that index
BLACK_POS_INDICES = [0, 1, 3, 4, 5, 7, 8, 7, 8, 10, 11, 12, 14, 15]
# (The first 7 positions are for the number-row blacks, remaining for QWERTY-row blacks)
# map white index -> fractional x position for black keys (0.65 means slightly right of the white key)
black_over_white_index = {i: (i + 0.65) for i in set(BLACK_POS_INDICES)}

# Starting octave for C4 (MIDI 60)
base_c_midi = 60  # C4
current_octave = 0  # offset in semitones of 12 per octave change

# Scale highlighting (C Major vs A Minor)
SCALE_MAJOR = {0, 2, 4, 5, 7, 9, 11}
SCALE_A_MINOR = {0, 2, 3, 5, 7, 8, 10}
scale_is_major = True

sustain_on = True

# Track pressed keys for highlighting
pressed_keys: set[int] = set()

# Velocity control: hold Left Shift for forte

def get_velocity() -> float:
    mods = pygame.key.get_mods()
    return 1.0 if (mods & pygame.KMOD_SHIFT) else 0.7

# ---------------- Drawing the Piano ----------------

def draw_piano():
    screen.fill((245, 246, 250))

    # Header text
    hdr = f"Piano – 2 Octaves  |  Octave: {current_octave:+d}  |  Sustain: {'ON' if sustain_on else 'OFF'}  |  Scale: {'C Major' if scale_is_major else 'A Minor'}  |  F1: Help"
    screen.blit(font_big.render(hdr, True, (20, 20, 20)), (20, 20))
    screen.blit(font.render("Lower: Z X C V B N M   Upper: A S D F G H J K L ; '   Blacks: 1 2 4 5 6 8 9  |  W E T Y U O P   |   Octave: [ ] or , .   |   -/= resize, F11 fullscreen", True, (40, 40, 40)), (20, 56))

    # Draw white keys
    for i, (k, semi) in enumerate(WHITE_LAYOUT):
        x = PIANO_LEFT + white_positions[i] * WHITE_KEY_W
        rect = pygame.Rect(x, PIANO_TOP, WHITE_KEY_W - 2, WHITE_KEY_H)
        in_scale = semi % 12 in (SCALE_MAJOR if scale_is_major else SCALE_A_MINOR)
        color = (255, 255, 255) if in_scale else (235, 235, 235)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, (60, 60, 60), rect, 2, border_radius=4)
        # highlight if pressed
        if k in pressed_keys:
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            s.fill((30, 144, 255, 70))
            screen.blit(s, rect.topleft)
        # label
        label = pygame.key.name(k).upper()
        screen.blit(font.render(label, True, (10, 10, 10)), (x + 8, PIANO_TOP + WHITE_KEY_H - 28))
        # note name
        semi = dict(WHITE_LAYOUT)[k]
        midi = base_c_midi + semi + current_octave * 12
        names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        name = names[midi % 12] + str((midi // 12) - 1)
        screen.blit(font.render(name, True, (30, 30, 30)), (x + 8, PIANO_TOP + 10))

    # Draw black keys on top
    for idx, (k, semi) in enumerate(BLACK_LAYOUT):
        pos_key = BLACK_POS_INDICES[idx]
        x = PIANO_LEFT + (black_over_white_index[pos_key]) * WHITE_KEY_W - (BLACK_KEY_W // 2)
        rect = pygame.Rect(int(x), PIANO_TOP, BLACK_KEY_W, BLACK_KEY_H)
        shadow = rect.move(2, 3)
        pygame.draw.rect(screen, (0,0,0), shadow, border_radius=3)
        in_scale = semi % 12 in (SCALE_MAJOR if scale_is_major else SCALE_A_MINOR)
        color = (25, 25, 25) if in_scale else (45, 45, 45)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, (10, 10, 10), rect, 2, border_radius=4)
        if k in pressed_keys:
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            s.fill((255, 255, 255, 80))
            screen.blit(s, rect.topleft)
        label = pygame.key.name(k).upper()
        screen.blit(font.render(label, True, (240, 240, 240)), (rect.x + 8, rect.y + rect.h - 28))

    if show_help:
        panel_h = 170
        panel = pygame.Surface((W - 60, panel_h), pygame.SRCALPHA)
        panel.fill((255, 255, 255, 220))
        help_y = max(90, min(H - panel_h - 20, PIANO_TOP + WHITE_KEY_H - panel_h - 10))
        screen.blit(panel, (30, help_y))
        y0 = help_y + 10
        screen.blit(font_big.render("How to Play", True, (20,20,20)), (40, y0))
        y0 += 30
        lines = [
            "Whites: Z X C V B N M   |   A S D F G H J K L ; '",
            "Blacks: 1 2 4 5 6 8 9   |   W E T Y U O P",
            "Octave: [ and ]  (or , and .)     Sustain: Space     Scale: F2     Louder: Shift",
            "Toggle Help: F1     Quit: Esc",
        ]
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, (30,30,30)), (40, y0 + i*28))

# ---------------- Note Triggering ----------------
key_to_semitone = {**{k: semi for k, semi in WHITE_LAYOUT}, **{k: semi for k, semi in BLACK_LAYOUT}}

# Keep references to channels so notes can decay naturally (sustain)
active_channels: list[pygame.mixer.Channel] = []


def play_key(key_code: int):
    if key_code not in key_to_semitone:
        return
    pressed_keys.add(key_code)
    semi = key_to_semitone[key_code] + current_octave * 12
    midi = base_c_midi + semi
    velocity = get_velocity()
    snd = make_piano_sound(midi, velocity)
    ch = pygame.mixer.find_channel()
    if ch:
        ch.play(snd)
        if sustain_on:
            ch.set_volume(1.0)
        active_channels.append(ch)


def release_key(key_code: int):
    # We let sounds ring out naturally (no hard stop) for a piano feel
    if key_code in pressed_keys:
        pressed_keys.remove(key_code)


# ---------------- Main Loop ----------------
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == SUSTAIN_TOGGLE:
                sustain_on = not sustain_on
            elif event.key == OCT_DOWN:
                current_octave = max(-1, current_octave - 1)
            elif event.key == OCT_UP:
                current_octave = min(2, current_octave + 1)
            elif event.key == OCT_DOWN2:
                current_octave = max(-1, current_octave - 1)
            elif event.key == OCT_UP2:
                current_octave = min(2, current_octave + 1)
            elif event.key == SCALE_TOGGLE:
                scale_is_major = not scale_is_major
            elif event.key == HELP_TOGGLE:
                show_help = not show_help
            elif event.key == SIZE_DOWN:
                apply_scale(scale * 0.9)
            elif event.key == SIZE_UP:
                apply_scale(scale * 1.1)
            elif event.key == FULLSCREEN_TOGGLE:
                fullscreen = not fullscreen
                apply_scale(scale)
            else:
                play_key(event.key)
        elif event.type == pygame.KEYUP:
            release_key(event.key)
        elif event.type == pygame.VIDEORESIZE:
            apply_scale(new_h=event.h)

    draw_piano()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()