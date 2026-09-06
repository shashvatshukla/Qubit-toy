import pygame
import random
from enum import Enum


class Q(Enum):
    ZERO  = '0'
    ONE   = '1'
    PLUS  = '+'
    MINUS = '-'


def hadamard(s):
    return {Q.ZERO: Q.PLUS, Q.ONE: Q.MINUS, Q.PLUS: Q.ZERO, Q.MINUS: Q.ONE}[s]

def measure_z(s):
    p0 = {Q.ZERO: 1.0, Q.ONE: 0.0, Q.PLUS: 0.5, Q.MINUS: 0.5}[s]
    return Q.ZERO if random.random() < p0 else Q.ONE

def measure_x(s):
    pp = {Q.PLUS: 1.0, Q.MINUS: 0.0, Q.ZERO: 0.5, Q.ONE: 0.5}[s]
    return Q.PLUS if random.random() < pp else Q.MINUS


# --- Level definitions ---
# Each level is a list of Q values the player must light up in sequence.
LEVELS = [
    [Q.ZERO,  Q.ZERO,  Q.ZERO,  Q.ZERO,  Q.ZERO],
    [Q.ONE,   Q.ONE,   Q.ONE,   Q.ONE,   Q.ONE],
    [Q.PLUS,  Q.PLUS,  Q.PLUS,  Q.PLUS,  Q.PLUS],
    [Q.MINUS, Q.MINUS, Q.MINUS, Q.MINUS, Q.MINUS],
    [Q.ONE,   Q.ONE,   Q.ONE,   Q.ZERO,  Q.ZERO],
    [Q.ONE,   Q.ONE,   Q.ZERO,  Q.ZERO,  Q.ONE],
    [Q.PLUS,  Q.PLUS,  Q.MINUS, Q.MINUS, Q.MINUS],
    [Q.PLUS,  Q.MINUS, Q.MINUS, Q.MINUS, Q.PLUS],
    [Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS],
    [Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS],
    [Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS,  Q.ZERO,  Q.PLUS],
    [Q.ONE,   Q.MINUS, Q.ONE,   Q.MINUS, Q.ONE,   Q.MINUS, Q.ONE,   Q.MINUS, Q.ONE,   Q.MINUS, Q.ONE,   Q.MINUS],
    [Q.ZERO,  Q.PLUS,  Q.ONE,   Q.MINUS, Q.ZERO,  Q.PLUS,  Q.ONE,   Q.MINUS],
]

current_level  = 0
level_progress = 0   # number of steps correctly lit so far


# --- Qubit state ---
qubit_value          = Q.ZERO
qubit_lit            = None
qubit_flash_end      = 0
level_complete_until = 0   # nonzero while showing the 1.5s completion flash

LIGHT_DEFS = {
    Q.ZERO:  {"label": "0",      "color_on": (100, 200, 255), "color_off": ( 30,  60,  80)},
    Q.ONE:   {"label": "1",      "color_on": ( 80, 255, 140), "color_off": ( 20,  60,  35)},
    Q.PLUS:  {"label": "+",      "color_on": (255, 180,  60), "color_off": ( 70,  50,  20)},
    Q.MINUS: {"label": "\u2212", "color_on": (220,  80, 255), "color_off": ( 60,  20,  70)},
}
LIGHT_RADIUS = 28
LIGHT_GLOW_R = 54

DOT_RADIUS = 10
DOT_GAP    = 30


def get_light_positions():
    import qubit_toy as qt
    w, h = qt.screen.get_size()
    play_h = h - qt.SWITCHER_HEIGHT
    cx, cy = w // 2, play_h // 2
    arm = min(w, play_h) * 0.28
    return {
        Q.ZERO:  (cx,            int(cy - arm)),
        Q.ONE:   (cx,            int(cy + arm)),
        Q.PLUS:  (int(cx + arm), cy),
        Q.MINUS: (int(cx - arm), cy),
    }

def get_qubit_btn_rects():
    pos = get_light_positions()
    sx, sy = pos[Q.ONE]
    ex, ey = pos[Q.PLUS]
    bw, bh = 130, 44
    mz  = pygame.Rect(sx - bw // 2, sy + 46, bw, bh)
    mx  = pygame.Rect(ex + 46, ey - bh // 2, bw, bh)
    had = pygame.Rect(mx.x, mz.y, bw, bh)
    return mz, mx, had

def get_level_dot_positions():
    import qubit_toy as qt
    w, _ = qt.screen.get_size()
    n = len(LEVELS[current_level])
    margin = 18
    end_x = w - margin - DOT_RADIUS
    start_x = end_x - (n - 1) * DOT_GAP
    return [(start_x + i * DOT_GAP, 28) for i in range(n)]

def get_nav_arrow_rects():
    import qubit_toy as qt
    w, _ = qt.screen.get_size()
    bw, bh = 44, 28
    # anchor to same right edge as dots
    margin = 18
    right_edge = w - margin
    right = pygame.Rect(right_edge - bw,          62, bw, bh)
    left  = pygame.Rect(right_edge - bw * 2 - 8,  62, bw, bh)
    return left, right


def _draw_glow_circle(surf, cx, cy, radius, color, glow_radius, glow_color):
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    for r in range(glow_radius, radius - 1, -2):
        alpha = int(120 * (1 - (r - radius) / (glow_radius - radius + 1)))
        pygame.draw.circle(glow_surf, (*glow_color, alpha), (glow_radius, glow_radius), r)
    surf.blit(glow_surf, (cx - glow_radius, cy - glow_radius))
    pygame.draw.circle(surf, color, (cx, cy), radius)


def draw_qubit_screen():
    import qubit_toy as qt
    qt.screen.fill(qt.QUBIT_BG)
    positions = get_light_positions()

    line_color = (50, 35, 70)
    pygame.draw.line(qt.screen, line_color, positions[Q.ZERO], positions[Q.ONE],  1)
    pygame.draw.line(qt.screen, line_color, positions[Q.PLUS], positions[Q.MINUS], 1)

    for key, (lx, ly) in positions.items():
        d     = LIGHT_DEFS[key]
        lit   = qubit_lit == key
        color = d["color_on"]  if lit else d["color_off"]
        g_col = d["color_on"]  if lit else (50, 40, 70)
        g_r   = LIGHT_GLOW_R   if lit else LIGHT_RADIUS + 8
        _draw_glow_circle(qt.screen, lx, ly, LIGHT_RADIUS, color, g_r, g_col)
        state_col = (255, 255, 255) if lit else (80, 65, 100)
        qt.blit_centered(qt.screen, qt.font_state.render(d["label"], True, state_col), lx, ly)

    mz, mx, had = get_qubit_btn_rects()
    qt.draw_btn(mz,  'measure_z', (60, 40, 120), (160, 100, 255), "Measure Z", (220, 180, 255))
    qt.draw_btn(mx,  'measure_x', (80, 50, 20),  (255, 180, 60),  "Measure X", (255, 210, 140))
    qt.draw_btn(had, 'hadamard',  (20, 70, 60),  (60, 220, 160),  "Hadamard",  (140, 255, 210))

    _draw_level_indicator()
    _draw_nav_arrows()


def _draw_level_indicator():
    import qubit_toy as qt
    w, _ = qt.screen.get_size()
    level = LEVELS[current_level]
    dot_positions = get_level_dot_positions()

    # Label left of the dots
    label = qt.font_tab.render(f"Lv {current_level + 1}", True, (180, 160, 220))
    lx = dot_positions[0][0] - label.get_width() - 10
    qt.screen.blit(label, (lx, 28 - label.get_height() // 2))

    for i, (dx, dy) in enumerate(dot_positions):
        q = level[i]
        d = LIGHT_DEFS[q]
        if i < level_progress:
            pygame.draw.circle(qt.screen, d["color_on"], (dx, dy), DOT_RADIUS)
        else:
            pygame.draw.circle(qt.screen, d["color_off"], (dx, dy), DOT_RADIUS)
            pygame.draw.circle(qt.screen, d["color_on"],  (dx, dy), DOT_RADIUS, 2)


def _draw_nav_arrows():
    import qubit_toy as qt
    left, right = get_nav_arrow_rects()
    qt.draw_btn(left,  'nav_prev', (40, 30, 60), (120, 90, 160), "<", (200, 180, 240))
    qt.draw_btn(right, 'nav_next', (40, 30, 60), (120, 90, 160), ">", (200, 180, 240))


def _check_level_progress(lit_q):
    global level_progress, level_complete_until
    if level_complete_until:
        return  # waiting to advance; ignore input
    level = LEVELS[current_level]
    if lit_q == level[level_progress]:
        level_progress += 1
        if level_progress == len(level):
            level_complete_until = pygame.time.get_ticks() + 1500
    else:
        level_progress = 0


def handle_click(pos):
    import qubit_toy as qt
    global qubit_value, qubit_lit, qubit_flash_end, current_level, level_progress
    mz, mx, had = get_qubit_btn_rects()
    if mz.collidepoint(pos):
        qt.flash_btn('measure_z')
        qubit_value = measure_z(qubit_value)
        qubit_lit = qubit_value
        qubit_flash_end = pygame.time.get_ticks() + 300
        _check_level_progress(qubit_lit)
    if mx.collidepoint(pos):
        qt.flash_btn('measure_x')
        qubit_value = measure_x(qubit_value)
        qubit_lit = qubit_value
        qubit_flash_end = pygame.time.get_ticks() + 300
        _check_level_progress(qubit_lit)
    if had.collidepoint(pos):
        qt.flash_btn('hadamard')
        qubit_value = hadamard(qubit_value)

    if not level_complete_until:
        left, right = get_nav_arrow_rects()
        if left.collidepoint(pos):
            qt.flash_btn('nav_prev')
            current_level  = (current_level - 1) % len(LEVELS)
            level_progress = 0
        if right.collidepoint(pos):
            qt.flash_btn('nav_next')
            current_level  = (current_level + 1) % len(LEVELS)
            level_progress = 0


def tick():
    global qubit_lit, current_level, level_progress, level_complete_until
    if qubit_lit and pygame.time.get_ticks() > qubit_flash_end:
        qubit_lit = None
    if level_complete_until and pygame.time.get_ticks() >= level_complete_until:
        current_level        = (current_level + 1) % len(LEVELS)
        level_progress       = 0
        level_complete_until = 0
