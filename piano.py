# Advanced but kid-friendly Piano: C major keyboard with minor mode, polyphony, and piano-ish synth
# Controls:
#  - White keys: A S D F G H J K  -> C D E F G A B C (C4..C5)
#  - Black keys:   W E   T Y U    -> C# D#  F# G# A#
#  - Q / E : octave down / up (range C3..C6)
#  - M     : toggle scale highlight (C Major  <->  A Minor)
#  - Space : toggle Sustain
#  - Esc or close window to exit
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
W, H = 900, 320
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Piano – C Major / A Minor (A,S,D,F,G,H,J,K + W,E,T,Y,U)")
font = pygame.font.SysFont(None, 24)
font_big = pygame.font.SysFont(None, 30)

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
# Base layout for one octave C..C' on home row, sharps on the row above
WHITE_LAYOUT = [
    (pygame.K_a, 0),    # C
    (pygame.K_s, 2),    # D
    (pygame.K_d, 4),    # E
    (pygame.K_f, 5),    # F
    (pygame.K_g, 7),    # G
    (pygame.K_h, 9),    # A
    (pygame.K_j, 11),   # B
    (pygame.K_k, 12),   # C'
    (pygame.K_l, 14),   # D'
    (pygame.K_SEMICOLON, 16),  # E'
    (pygame.K_QUOTE, 17),      # F'
]

BLACK_LAYOUT = [
    (pygame.K_w, 1),    # C#
    (pygame.K_e, 3),    # D#
    (pygame.K_t, 6),    # F#
    (pygame.K_y, 8),    # G#
    (pygame.K_u, 10),   # A#
    (pygame.K_o, 13),   # C#'
    (pygame.K_p, 15),   # D#'
]

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
WHITE_KEY_W = 70
WHITE_KEY_H = 180
BLACK_KEY_W = 42
BLACK_KEY_H = 110
PIANO_LEFT = 40
PIANO_TOP = 110

# positions of white keys across ~1.5 octaves (C..F')
white_positions = list(range(len(WHITE_LAYOUT)))
# which white-key slots have black keys above them
black_over_white_index = {0: 0.65, 1: 1.65, 3: 3.65, 4: 4.65, 5: 5.65, 7: 7.65, 8: 8.65}


def draw_piano():
    screen.fill((245, 246, 250))

    # Header text
    hdr = f"C Major/A Minor Piano  |  Octave: {current_octave:+d}  |  Sustain: {'ON' if sustain_on else 'OFF'}  |  Scale: {'C Major' if scale_is_major else 'A Minor'}"
    screen.blit(font_big.render(hdr, True, (20, 20, 20)), (20, 20))
    screen.blit(font.render("White: A S D F G H J K   Black: W E T Y U   Shift = louder  |  Q/E = octave +/-  |  M = toggle scale", True, (40, 40, 40)), (20, 56))

    # Draw white keys
    for i, (k, semi) in enumerate(WHITE_LAYOUT):
        x = PIANO_LEFT + white_positions[i] * WHITE_KEY_W
        rect = pygame.Rect(x, PIANO_TOP, WHITE_KEY_W - 2, WHITE_KEY_H)
        in_scale = semi % 12 in (SCALE_MAJOR if scale_is_major else SCALE_A_MINOR)
        color = (255, 255, 255) if in_scale else (235, 235, 235)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (60, 60, 60), rect, 2)
        # highlight if pressed
        if k in pressed_keys:
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            s.fill((30, 144, 255, 70))
            screen.blit(s, rect.topleft)
        # label
        label = pygame.key.name(k).upper()
        screen.blit(font.render(label, True, (10, 10, 10)), (x + 8, PIANO_TOP + WHITE_KEY_H - 28))

    # Draw black keys on top
    for idx, (k, semi) in enumerate(BLACK_LAYOUT):
        # map to position over white keys using the pattern indices
        # keys order corresponds to C#, D#, F#, G#, A#
        pos_key = [0, 1, 3, 4, 5, 7, 8][idx]
        x = PIANO_LEFT + (black_over_white_index[pos_key]) * WHITE_KEY_W - (BLACK_KEY_W // 2)
        rect = pygame.Rect(int(x), PIANO_TOP, BLACK_KEY_W, BLACK_KEY_H)
        in_scale = semi % 12 in (SCALE_MAJOR if scale_is_major else SCALE_A_MINOR)
        color = (25, 25, 25) if in_scale else (45, 45, 45)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (10, 10, 10), rect, 2)
        if k in pressed_keys:
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            s.fill((255, 255, 255, 80))
            screen.blit(s, rect.topleft)
        label = pygame.key.name(k).upper()
        screen.blit(font.render(label, True, (240, 240, 240)), (rect.x + 8, rect.y + rect.h - 28))


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
            elif event.key == pygame.K_SPACE:
                sustain_on = not sustain_on
            elif event.key == pygame.K_q:
                current_octave = max(-1, current_octave - 1)  # down to C3
            elif event.key == pygame.K_e:
                current_octave = min(2, current_octave + 1)   # up to C6
            elif event.key == pygame.K_m:
                scale_is_major = not scale_is_major
            else:
                play_key(event.key)
        elif event.type == pygame.KEYUP:
            release_key(event.key)

    draw_piano()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()