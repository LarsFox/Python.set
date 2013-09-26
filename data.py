import os
import pygame as pg
from pygame.locals import *

# basic and engine things. # q: quantity, c: colour, f: fill, s: shape
quantity = ('1', '2', '3')
colours  = ('Red', 'Green', 'Purple')
fill     = ('empty', 'striped', 'filled')
shapes   = ('oval', 'squiggle', 'diamond')

display = (800, 600)
name = "Set"
filepath = os.path.dirname(__file__)
#png = '.png'   # do I really need this thing?

card_attr = {
    'width': 106, 'height': 160,
    'X': 170, 'Y': 15, 'space': 10
}
empty_card = pg.image.load('{}/cards/card.png'.format(filepath))
selection = pg.image.load('{}/cards/selection.png'.format(filepath))

# these are added to x and y so the right position is chosen.
symbol_width, symbol_height = 80, 42  # 42!!
add_x = (card_attr['width'] - symbol_width)/2
add_space = 4
add_y = {
    '1': [(card_attr['height'] - symbol_height)/2],
    '2': [(card_attr['height'] - 2*symbol_height - add_space)/2, 
          (card_attr['height'] + add_space)/2],
    '3': [(card_attr['height'] - 3*symbol_height - 2*add_space)/2,
          (card_attr['height'] - symbol_height)/2,
          (card_attr['height'] + symbol_height + 2*add_space)/2]
}

# Green, Purple and Red do NOT look as they are named. Don't ask why
palette = {
    'Light Grey':   (200, 200, 200),    'Green':        ( 55, 205,  65),
    'Red':          (255,   0, 120),    'Purple':       (120, 120, 210)
}

class Card(pg.sprite.Sprite):

    def __init__(self, q, c, f, s):
        self.attr = (
            self.quantity, self.colour, self.fill, self.shape) = (
            q, c, f, s)
        self.selected = False

    def draw(self, x, y):
        #pg.sprite.Sprite.__init__(self)
        self.coord = (x, y)
        self.rect = pg.Rect(self.coord,
            (card_attr['width'], card_attr['height']))
        screen = pg.display.get_surface()
        screen.blit(empty_card, self.coord)

        # the symbol(s) == filled coloured rectangle + alpha-mask over
        symbol_name = '{}/cards/{}{}.png'.format(
            filepath, self.fill[0], self.shape[0])
        symbol_img = pg.image.load(symbol_name)
        for i in xrange(int(self.quantity)):
            pg.draw.rect(screen, palette[self.colour],
                [x+add_x, y+add_y[self.quantity][i],
                symbol_width, symbol_height])
            screen.blit(symbol_img,
                (x+add_x, y+add_y[self.quantity][i]))
        if self.selected: screen.blit(selection, (x-2, y-2))