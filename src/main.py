import asyncio
import pygame

import qubit_toy as qt


async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = qt.scale_pos(event.pos)
                for i, rect in enumerate(qt.get_tab_rects()):
                    if rect.collidepoint(pos):
                        qt.tab = i
                if qt.tab == 0:
                    qt.bit_logic.handle_click(pos)
                if qt.tab == 1:
                    qt.qubit_logic.handle_click(pos)
        qt.qubit_logic.tick()
        qt.draw()
        qt.clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
