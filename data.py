# check if there's no need in extra vars!!
# squiggle texture is the worst, need to be fixed.
import os
import pygame as pg
from pygame.locals import *

# basic and engine things. # q: quantity, c: colour, f: fill, s: shape
quantity = ('1', '2', '3')  # or 0, 1, 2?
colours  = ('Red', 'Green', 'Purple')
fill     = ('empty', 'striped', 'filled')
shapes   = ('oval', 'squiggle', 'diamond')

# thigs for pygame:
name = "Set"
filepath = os.path.dirname(__file__)
display = window_width, window_height = 800, 600

# card has lots of attributes, so it's better to store them in dict
card_attr = {
    'width': 106, 'height': 160,
    'X': 170, 'Y': 15, 'space': 10
}
empty_card = pg.image.load('{}/cards/card.png'.format(filepath))

symbol_width, symbol_height = 80, 42  # 42!!
add_x = (card_attr['width'] - symbol_width)/2
add_space = 4
add_y = {  # unite three and one? # hope, you'll see where the values come from
    '1': [(card_attr['height'] - symbol_height)/2],
    '2': [(card_attr['height'] - 2*symbol_height - add_space)/2, 
          (card_attr['height'] + add_space)/2],
    '3': [(card_attr['height'] - 3*symbol_height - 2*add_space)/2,
          (card_attr['height'] - symbol_height)/2,
          (card_attr['height'] + symbol_height + 2*add_space)/2]
}

# Green, Purple and Red do NOT look as they are named. Don't ask why
palette = {
    'Black':        (  0,   0,   0),    'White':        (255, 255, 255),
    'Yellow':       (255, 255,   0),    'Light Yellow': (250, 255, 150),
    'Red':          (255,   0, 120),    'Purple':       (120, 120, 210),
    'Green':        ( 55, 205,  65)
}

#png = '.png'   # do I really need this thing?

class Card(pg.sprite.Sprite):

    def __init__(self, q, c, f, s):
        self.attr = (
            self.quantity, self.colour, self.fill, self.shape) = (
            q, c, f, s)
        pg.sprite.Sprite.__init__(self)

    def draw(self, x, y):
        # the symbol(s) = filled coloured rectangle + alpha-mask over
        screen = pg.display.get_surface()
        innername = '{}/cards/{}{}.png'.format(
            filepath, self.fill[0], self.shape[0])
        innerimg = pg.image.load(innername)
        for i in xrange(int(self.quantity)):
            pg.draw.rect(screen, palette[self.colour],
                [x+add_x, y+add_y[self.quantity][i],
                symbol_width, symbol_height])
            screen.blit(innerimg,
                (x+add_x, y+add_y[self.quantity][i]))

    ''' MAYBE there will be need in it
    def __str__(self):
        s = ''
        if self.quantity > '1': s = 's'
        return '{} {} {} {}'.format(*self.attr) + s'''