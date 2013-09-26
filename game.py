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
        pg.display.set_mode(display)
        pg.display.set_caption(name)
        self.engine = Engine()

        screen = pg.display.get_surface()
        screen.fill(palette['Light Yellow'])

    def main(self):
        running = True
        for event in pg.event.get():
            if event.type == QUIT: running = False
            if event.type == MOUSEBUTTONDOWN: print 'YAY'
            #while running:
            self.engine.launch()
            while self.engine.deck:
                self.engine.check()

                self.draw_cards()
                self.engine.action()

            while self.has_set(self.table):
                self.draw_cards()
                self.engine.action()

            self.deck, self.table, self.gone, = self.gone + self.table, [], []

            more = raw_input('Want another?\n> ')
            if not more: exit()

    def draw_cards(self):
        # make drawing replaced cards only
        print 'drawn'
        screen = pg.display.get_surface()

        # this lets to make 2D array from deck
        rows = len(self.engine.table)/3     # 3/6/9/12/15 cards in 3 rows
        card_x, card_y = card_attr['X'], card_attr['Y']
        for row in xrange(0, len(self.engine.table), rows):
            for column in xrange(rows):
                #print row,column, len(self.engine.table)
                card = self.engine.table[row+column]
                screen.blit(empty_card, (card_x, card_y))
                card.draw(card_x, card_y)
                
                card_x += card_attr['width'] + card_attr['space']
            card_y += card_attr['height'] + card_attr['space']
            card_x = card_attr['X']

        pg.display.flip()

if __name__ == "__main__":
    game = Game()
    try: game.main()
    except EOFError: print "Bye!"

pg.quit()
