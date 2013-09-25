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
        pg.time.wait(5000)      # and then kills itself. Artistic.

    def draw_cards(self):
        def draw_colour():
            print card.quantity,
            for i in xrange(int(card.quantity)):
            #self.screen.blit(pg.image.load('{}/cards/g.png'.format(filepath)), (card_x, card_y+card_attr['height']/2-30))
                pg.draw.rect(self.screen, palette[card.colour],
                    [card_x+add_x, card_y+add_y[card.quantity][i],
                    symbol_width, symbol_height])
                self.screen.blit(card.innerimg,
                    (card_x+add_x, card_y+add_y[card.quantity][i]))

        # these two checks move the whole table, so it looks much better.
        if len(self.engine.table) == 15:
            card_attr['X'] += 55
            card_attr['in_row'] += 1

        # this lets to make 2D array from deck
        card_x, card_y = card_attr['X'], card_attr['Y']
        for row in xrange(0, len(self.engine.table), card_attr['in_row']):
            for column in xrange(card_attr['in_row']):
                card = self.engine.table[row+column]
                self.screen.blit(empty_card, (card_x, card_y))

                draw_colour()
                
                card_x += card_attr['width'] + card_attr['space']
            card_y += card_attr['height'] + card_attr['space']
            card_x = card_attr['X']

        if len(self.engine.table) == 15:
            card_attr['X'] -= 55
            card_attr['in_row'] -= 1

if __name__ == "__main__":
    game = Game()
    game.main()

pg.quit()
