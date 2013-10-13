import pygame

import texts

# ================================== Basic ==================================
icon = pygame.image.load('images/icon.png')

palette = {
    'Light Grey':   (200, 200, 200),    'green':        ( 55, 205,  65),
    'red':          (255,   0, 120),    'purple':       (120, 120, 210),
    'Black':        (  0,   0,   0),    'Empty':        (0,  0,  0,  0),
    'Red':          (240,  50,  50),    'Green':        (  0, 150,  17),
    'Emerald':      (  0, 180, 150)
}

# ============================= Fonts and Text ==============================
pygame.font.init()
consolas = 'images/consolas.ttf'
maiandra_gd = 'images/maiandra_gd.ttf'
antialasing = True
size16 = 16
size18 = 18

header_font = pygame.font.Font(maiandra_gd, size18)
header = header_font.render(texts.header, antialasing, palette['Black'])

c_font = pygame.font.Font(maiandra_gd, size16)
def common_font(text, colour='Black'):
    return c_font.render(text, antialasing, palette[colour])

time_str = '{:0<4}'
t_font = pygame.font.Font(consolas, size18)

def time_font(text, colour):
    return t_font.render(text, antialasing, palette[colour])

def round_time(time, nround=2):
    return time_str.format(round(time, nround))

# Formatting texts:
lines = {
    'current': time_font(texts.current, 'Black'),
    'last': time_font(texts.last, 'Red'),
    'best': time_font(texts.best, 'Green'),
    'total': time_font(texts.total, 'Emerald'),
    'player': 'Player {}: {}',
    'start': [common_font(line) for line in texts.start.split('\n')]
}

# =================================== Card ==================================
empty_card = pygame.image.load('images/card.png')
selection = pygame.image.load('images/selection.png')
card_width, card_height, card_space = 106, 160, 10
card_start_x, card_start_y = 170, 15
card_rows = 3

# ============================= Symbols in card =============================
name_template = 'images/{}{}.png'.format
symbol_width, symbol_height, symbol_space = 80, 42, 4
symbol_x = (card_width - symbol_width)/2
symbol_y = {
    '1': [(card_height - symbol_height)/2],
    '2': [(card_height - 2*symbol_height - symbol_space)/2, 
          (card_height + symbol_space)/2],
    '3': [(card_height - 3*symbol_height - 2*symbol_space)/2,
          (card_height - symbol_height)/2,
          (card_height + symbol_height + 2*symbol_space)/2]
}

# ================================= Buttons =================================
class Button(object):
    def __init__(self, image, x, y, size):
        self.image = pygame.image.load(image)
        self.coord = (x, y)
        self.size = size

    def draw(self, screen):
        self.rect = pygame.Rect(self.coord, self.size)
        screen.blit(self.image, self.coord)

start_button = Button('images/start.png', 170, 520, (216, 57))
end_button = Button('images/over.png', 396, 520, (216, 57))
help_button = Button('images/help.png', 15, 520, (140, 57))


class SetButton(Button):
    @property
    def text(self, space=5):
        return self.coord[0], self.coord[1] - size16 - space

set_buttons = [
    SetButton('images/set.png', 20, 74+i*170, (130, 42)) for i in xrange(3)
]
