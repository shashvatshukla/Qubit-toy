import pygame

import bit_logic
import qubit_logic

pygame.init()

BIT_BG   = ( 20,  40,  80)
QUBIT_BG = ( 18,  10,  35)

TAB_COLORS = [
    ("Bit",   ( 50, 120, 220)),
    ("Qubit", (140,  60, 200)),
]

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Qubit Toy")
clock = pygame.time.Clock()

_W, _H = screen.get_size()
_scale = max(_H, 400) / 600

SWITCHER_HEIGHT = int(60 * _scale)
BUTTON_MARGIN   = int(10 * _scale)
BUTTON_RADIUS   = int( 8 * _scale)

font_large  = pygame.font.SysFont("Segoe UI", int(120 * _scale), bold=True)
font_medium = pygame.font.SysFont("Segoe UI", int(22  * _scale), bold=True)
font_tab    = pygame.font.SysFont("Segoe UI", int(16  * _scale), bold=True)
font_state  = pygame.font.SysFont("Segoe UI", int(18  * _scale), bold=True)

tab = 0

btn_flash: dict = {}
BTN_FLASH_MS = 150

def flash_btn(key):
    btn_flash[key] = pygame.time.get_ticks() + BTN_FLASH_MS

def is_btn_lit(key):
    return pygame.time.get_ticks() < btn_flash.get(key, 0)

def brighten(color, amount=70):
    return tuple(min(255, c + amount) for c in color)

def rrect(surf, color, rect, radius=BUTTON_RADIUS, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surf, border_color, rect, width=border, border_radius=radius)

def blit_centered(surf, text_surf, cx, cy):
    surf.blit(text_surf, (cx - text_surf.get_width() // 2, cy - text_surf.get_height() // 2))

def draw_btn(rect, key, base_col, border_col, text, text_col):
    lit = is_btn_lit(key)
    col = brighten(base_col) if lit else base_col
    bc  = (255, 255, 255)   if lit else border_col
    rrect(screen, col, rect)
    rrect(screen, col, rect, border=2, border_color=bc)
    blit_centered(screen, font_medium.render(text, True, text_col), rect.centerx, rect.centery)

def get_tab_rects():
    w, h = screen.get_size()
    n = len(TAB_COLORS)
    btn_w = (w - BUTTON_MARGIN * (n + 1)) // n
    return [pygame.Rect(BUTTON_MARGIN + i * (btn_w + BUTTON_MARGIN),
                        h - SWITCHER_HEIGHT + BUTTON_MARGIN,
                        btn_w, SWITCHER_HEIGHT - BUTTON_MARGIN * 2)
            for i in range(n)]

def draw_switcher():
    w, h = screen.get_size()
    pygame.draw.rect(screen, (20, 20, 20), (0, h - SWITCHER_HEIGHT, w, SWITCHER_HEIGHT))
    for i, rect in enumerate(get_tab_rects()):
        color = TAB_COLORS[i][1]
        rrect(screen, color, rect)
        if i == tab:
            rrect(screen, color, rect, border=3, border_color=(255, 255, 255))
        blit_centered(screen, font_tab.render(TAB_COLORS[i][0], True, (255, 255, 255)),
                      rect.centerx, rect.centery)

def draw():
    if tab == 0:
        bit_logic.draw_bit_screen()
    else:
        qubit_logic.draw_qubit_screen()
    draw_switcher()
    pygame.display.flip()


