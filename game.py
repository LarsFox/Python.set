#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The Set game.
# Dedicated with love to those who I love
#
# Gently speaking, I would have done nothing without you.
# Using pygame (www.pygame.org), python, MS Windows, Paint and food.
# Leo Motovskikh aka
# Lars Fox
#

from engine import *

class Game():

    def __init__(self):
        pg.init()
        pg.display.set_caption(name)
        self.window = pg.display.set_mode(display)
        self.engine = Engine()

        screen = pg.display.get_surface()

    def main(self):
        self.engine.launch()
        running = True
        selected = set()
        while running:
            for e in pg.event.get():
                self.window.fill(palette['Light Grey'])
                if e.type == QUIT: running = False
                self.draw_cards()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    for card in self.engine.table:
                        if card.rect.collidepoint(e.pos):
                            card.selected = not card.selected
                            selected.add(card)

                # or press Up and see the hint.
                # sets usually start with the first one
                if e.type == KEYDOWN and e.key == K_UP:
                    print self.engine.has_set(self.engine.table)
            
            # the game is played until there are no sets
            if self.engine.has_set(self.engine.table):
                if len(selected) == 3:
                    for card in selected:
                        self.engine.table[card.index].selected = False

                    if self.engine.is_set(selected):
                        self.engine.action(selected)

                    selected.clear()

            # but if there're no sets, we add 3 more cards.
            elif self.engine.deck and len(self.engine.table) <= 12:
                self.engine.table += self.engine.deck[:3]
                self.engine.deck = self.engine.deck[3:]

            # in real game we keep adding cards, but that is crazy
            # to be honest, I don't want to enlarge the game display.
            elif len(self.engine.table) == 15:
                print '15 cards and no set! Reshuffling!'
                self.engine.deck += self.engine.table
                self.engine.launch()

            # and if all the sets are gone and there's nothing to add: GG
            else:
                more = raw_input('Want another?\n> ')
                if more:
                    self.engine.deck = self.engine.gone + self.engine.table
                    self.engine.table, self.engine.gone = [], []
                    self.engine.launch()
                else: running = False

    def draw_cards(self):
        screen = pg.display.get_surface()

        # this makes 2D array from deck
        rows = len(self.engine.table)/3     # 3/6/9/12/15 cards in 3 rows
        card_x, card_y = card_attr['X'], card_attr['Y']
        for row in xrange(0, len(self.engine.table), rows):
            for column in xrange(rows):
                i = row + column
                card = self.engine.table[i]
                card.index = i
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
