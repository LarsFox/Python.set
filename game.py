#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Leo M.
# ¯\(°_o)/¯
#

from engine import *

class Game():

    def __init__(self):
        pg.init()
        pg.display.set_caption(name)
        self.screen = pg.display.set_mode(display)
        self.visible = pg.Surface(display)
        self.visible.fill(palette['Light Yellow'])
        self.engine = Engine()
        self.engine.launch()

        '''
        font = pg.font.Font(None, 36)
        text = font.render("text", 1, (10, 10, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        screen.blit(background, (0, 0))
        pg.display.flip()
        pg.draw.rect(screen, palette['White'], [150, 50, 75, 100])
        '''

    def main(self):
        done, clock = False, pg.time.Clock()
        while not done:
            clock.tick(10)
            for event in pg.event.get():
                if event.type == QUIT: done = True

            self.screen.fill(palette['Light Yellow'])
            self.screen.blit(self.visible, (0, 0))
            pg.display.update()
            self.draw_cards()
            pg.display.flip()
            done = True         # this thing just draws itself
        pg.time.wait(1000)      # and then kills itself. Artistic.

    def draw_cards(self):
        if len(self.engine.table) == 15: card_position['X'] -= 55
        card_x, card_y = card_position['X'], card_position['Y']
        for row in xrange(0, len(self.engine.table), 4):
            for column in xrange(4):
                card = self.engine.table[row+column]
                self.screen.blit(card.image, (card_x, card_y))
                # dot is only to calibrate the scales for the missing images
                self.screen.blit(card.dot, (
                    card_x+card_width/2-5, card_y+card_height/2-5))

                card_x += card_width + card_space
            card_y += card_height + card_space
            card_x = card_position['X']
        if len(self.engine.table) == 15: card_position['X'] += 55

if __name__ == "__main__":
    game = Game()
    game.main()

pg.quit()