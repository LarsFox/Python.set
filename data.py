# q: quantity, c: colour, f: fill, s: shape

import os
import pygame as pg
from pygame.locals import *

# basic and engine things.
quantity = ('1', '2', '3')  # or 0, 1, 2?
colours  = ('red', 'green', 'purple')
fill     = ('empty', 'striped', 'filled')
shapes   = ('Oval', 'Squiggle', 'Diamond')

# thigs for pygame:
name = "Set"
display = window_width, window_height = 800, 600

card_size = card_width, card_height = 106, 160
card_space = 10

card_position = {'X': 170, 'Y': 15}     # get item looks better

palette = {
    'Black':        (  0,   0,   0),    'White':        (255, 255, 255),
    'Yellow':       (255, 255,   0),    'Light Yellow': (250, 255, 150)
}

filepath = os.path.dirname(__file__)
png = '.png'

class Card(pg.sprite.Sprite):

    def __init__(self, q, c, f, s):
        self.attr = (
            self.quantity, self.colour, self.fill, self.shape) = (
            q, c, f, s)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('{}/cards/card{}'.format(filepath, png))
        self.dot = pg.image.load('{}/cards/dot{}'.format(filepath, png))
        # innerimgname = ''.join([x[0] for x in self.attr]) + png
        # self.innerimg = pg.imageload(innerimgname)

    def __str__(self):
        s = ''
        if self.quantity > '1': s = 's'
        return '{} {} {} {}'.format(*self.attr) + s

    ''' MAYBE there will be need in this thing
    def draw(self, x, y):
        self.rect = Rect(x, y, card_width, card_height)'''