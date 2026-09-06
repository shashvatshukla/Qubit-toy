import pygame
import random

bit_value = 0

LABELS     = ["Set 0", "Set 1", "Flip", "Random"]
BTN_KEYS   = ["set0", "set1", "flip", "random"]
BTN_COLORS = [(50,130,220),(50,170,80),(200,140,30),(170,60,200)]


def get_action_button_rects():
    import qubit_toy as qt
    w, h = qt.screen.get_size()
    btn_w, btn_h = 130, 50
    gap = 18
    start_x = (w - (4 * btn_w + 3 * gap)) // 2
    y = h - qt.SWITCHER_HEIGHT - btn_h - 60
    return [pygame.Rect(start_x + i * (btn_w + gap), y, btn_w, btn_h) for i in range(4)]


def draw_bit_screen():
    import qubit_toy as qt
    w, h = qt.screen.get_size()
    qt.screen.fill(qt.BIT_BG)
    box_size = 160
    box_rect = pygame.Rect((w - box_size) // 2,
                           (h - qt.SWITCHER_HEIGHT) // 2 - box_size // 2 - 40,
                           box_size, box_size)
    qt.rrect(qt.screen, (30, 60, 120), box_rect, radius=16)
    qt.rrect(qt.screen, (30, 60, 120), box_rect, radius=16, border=2, border_color=(80, 140, 255))
    qt.blit_centered(qt.screen, qt.font_large.render(str(bit_value), True, (255, 255, 255)),
                     box_rect.centerx, box_rect.centery)
    for i, rect in enumerate(get_action_button_rects()):
        qt.draw_btn(rect, BTN_KEYS[i], BTN_COLORS[i], (255, 255, 255), LABELS[i], (255, 255, 255))


def handle_click(pos):
    import qubit_toy as qt
    global bit_value
    for i, rect in enumerate(get_action_button_rects()):
        if rect.collidepoint(pos):
            qt.flash_btn(BTN_KEYS[i])
            if   i == 0: bit_value = 0
            elif i == 1: bit_value = 1
            elif i == 2: bit_value = 1 - bit_value
            elif i == 3: bit_value = random.randint(0, 1)
