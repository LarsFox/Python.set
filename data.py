import pygame

import texts

# ================================== Basic ==================================
ICON = pygame.image.load('images/icon.png')

PALETTE = {
    'Background':   (216, 209, 232),    'green':        ( 55, 205,  65),
    'red':          (255,   0, 120),    'purple':       ( 60,  10, 110),
    'Black':        (  0,   0,   0),    'Empty':        (0,  0,  0,  0),
    'Red':          (240,  50,  50),    'Green':        (  0, 150,  17),
    'Emerald':      (  0, 180, 150)
}

# ============================= Fonts and Text ==============================
pygame.font.init()
CONSOLAS = 'images/consolas.ttf'
MAIANDRA_GD = 'images/maiandra_gd.ttf'
ANTIALASING = True
SIZE16 = 16
SIZE18 = 18

H_FONT = pygame.font.Font(MAIANDRA_GD, SIZE18)
HEADER = H_FONT.render(texts.header, ANTIALASING, PALETTE['Black'])

C_FONT = pygame.font.Font(MAIANDRA_GD, SIZE16)
def common_font(text, colour='Black'):
    return C_FONT.render(text, ANTIALASING, PALETTE[colour])

TIME_STR = '{:0<4}'
T_FONT = pygame.font.Font(CONSOLAS, SIZE18)

def time_font(text, colour):
    return T_FONT.render(text, ANTIALASING, PALETTE[colour])

def round_time(time, nround=2):
    return TIME_STR.format(round(time, nround))

# Formatting texts:
LINES = {
    'current': time_font(texts.current, 'Black'),
    'last': time_font(texts.last, 'Red'),
    'best': time_font(texts.best, 'Green'),
    'total': time_font(texts.total, 'Emerald'),
    'player': 'Player {}: {}',
    'start': [common_font(line) for line in texts.start.split('\n')]
}

# =================================== Card ==================================
EMPTY_CARD = pygame.image.load('images/card.png')
SELECTION = pygame.image.load('images/selection.png')
CARD_WIDTH, CARD_HEIGHT, CARD_SPACE = 106, 160, 10
CARD_START_X, CARD_START_Y = 170, 15
CARD_ROWS = 3

# ============================= Symbols in card =============================
NAME_TEMPLATE = 'images/{}{}.png'.format
SYMBOL_WIDTH, SYMBOL_HEIGHT, SYMBOL_SPACE = 80, 42, 4
SYMBOL_X = (CARD_WIDTH - SYMBOL_WIDTH)/2
SYMBOL_Y = {
    '1': [(CARD_HEIGHT - SYMBOL_HEIGHT)/2],
    '2': [(CARD_HEIGHT - 2*SYMBOL_HEIGHT - SYMBOL_SPACE)/2, 
          (CARD_HEIGHT + SYMBOL_SPACE)/2],
    '3': [(CARD_HEIGHT - 3*SYMBOL_HEIGHT - 2*SYMBOL_SPACE)/2,
          (CARD_HEIGHT - SYMBOL_HEIGHT)/2,
          (CARD_HEIGHT + SYMBOL_HEIGHT + 2*SYMBOL_SPACE)/2]
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

START_BUTTON = Button('images/start.png', 170, 520, (216, 57))
END_BUTTON = Button('images/over.png', 396, 520, (216, 57))
HELP_BUTTON = Button('images/help.png', 15, 520, (140, 57))


class SetButton(Button):
    @property
    def text(self, space=5):
        return self.coord[0], self.coord[1] - SIZE16 - space

SET_BUTTONS = [
    SetButton('images/set.png', 20, 74+i*170, (130, 42)) for i in xrange(3)
]
