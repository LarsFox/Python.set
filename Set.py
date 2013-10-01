#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The Set game.
#
# Leo M.
#

from game import *

game_name = "Set"
window_size = (800, 600)
rows = 3
palette = {
    'Light Grey':   (200, 200, 200),    'Green':        ( 55, 205,  65),
    'Red':          (255,   0, 120),    'Purple':       (120, 120, 210),
    'Empty':        (0,  0,  0,  0)
}

# ================================== Card ==================================
empty_card = pygame.image.load('images/card.png')
selection = pygame.image.load('images/selection.png')
card_width, card_height, card_space = 106, 160, 10
card_start_x, card_start_y = 170, 15
card_attr = {
    'width': 106, 'height': 160,
    'X': 170, 'Y': 15, 'space': 10
}

# ============================ Symbols in card =============================
name_template = 'images/{}{}.png'.format
symbol_width, symbol_height, symbol_space = 80, 42, 4
symbol_x = (card_attr['width'] - symbol_width)/2
symbol_y = {
    '1': [(card_attr['height'] - symbol_height)/2],
    '2': [(card_attr['height'] - 2*symbol_height - symbol_space)/2, 
          (card_attr['height'] + symbol_space)/2],
    '3': [(card_attr['height'] - 3*symbol_height - 2*symbol_space)/2,
          (card_attr['height'] - symbol_height)/2,
          (card_attr['height'] + symbol_height + 2*symbol_space)/2]
}

# ============================== GUI Classes ===============================
class GUICard(Card):
    @property
    def image(self):
        image = pygame.Surface((card_width, card_height))
        image = image.convert_alpha()
        image.fill(palette['Empty'])
        image.blit(empty_card, (0, 0))

        symbol_img = pygame.image.load(name_template(
            self.symbol[0], self.fill[0]))

        for i in xrange(int(self.number)):
            x, y = symbol_x, symbol_y[self.number][i]

            pygame.draw.rect(image, palette[self.colour],
                (x, y, symbol_width, symbol_height))
            image.blit(symbol_img, (x, y))

        return image

class GUIBoard(Board):
    @classmethod
    def form_deck(cls):
        return [GUICard(*attrs) for attrs in
                itertools.product(cls.numbers, cls.symbols,
                                  cls.fill, cls.colours)]

class Button(object):
    def __init__(self, image, x, y=520, size=(216, 57)):
        self.image, self.coord, self.size = image, (x, y), size

    def draw(self, screen):
        self.rect = pygame.Rect(self.coord, self.size)
        screen.blit(self.image, self.coord)

start_button = Button(
    pygame.image.load('images/start.png'), 168)

end_button = Button(
    pygame.image.load('images/over.png'), 394)

# ================================== Game ==================================
class GUIGame(Game):
    def __init__(self, name, window_size):
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_mode(window_size)
        self.started = False

    def start(self):
        self.board = GUIBoard.initial()
        self.time = time.clock()
        self.draw_end_button = False

    def display(self):
        screen = pygame.display.get_surface()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            screen.fill(palette['Light Grey'])
            self.launch_buttons(event, screen)

            if self.board.table and self.started:
                self.launch_board(event)

            pygame.display.flip()

    def launch_buttons(self, event, screen):
        start_button.draw(screen)
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if start_button.rect.collidepoint(event.pos):
                self.start()
                self.started = True

        if self.draw_end_button:
            end_button.draw(screen)

    def launch_board(self, event):
        def draw_cards():
            screen = pygame.display.get_surface()
            columns = len(self.board.table)/rows
            card_x, card_y = card_start_x, card_start_y

            for row in xrange(0, len(self.board.table), columns):
                for column in xrange(columns):
                    i = row + column
                    card = self.board.table[i]
                    card.rect = pygame.Rect(
                        (card_x, card_y), (card_width, card_height))

                    screen.blit(card.image, (card_x, card_y))
                    if card in self.board.selected:
                        screen.blit(selection, (card_x-2, card_y-2))
                    
                    card_x += card_width + card_space

                card_x = card_start_x
                card_y += card_height + card_space

        def click_cards(event):
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for card in self.board.table:
                    if card.rect.collidepoint(event.pos):

                        if card not in self.board.selected:
                            self.board.selected.add(card)
                        else:
                            self.board.selected.remove(card)

            ''' To enable the cheat,
                decomment one line in game.Board.has_set()'''

            '''if e.type == KEYDOWN and e.key == K_UP:
                print self.board.has_set()'''

        draw_cards()
        click_cards(event)

    def check(self, table_limit=15, table_size=12, quantity=3):
        # If we have less than 12 cards, we add more
        if len(self.board.table) < table_size:
            self.board = self.board.add_cards()

        # Based on window size: if 12 <= cards < 15 is not enough, we add more.
        elif not self.board.has_set() and len(self.board.table) < table_limit:
            self.board = self.board.add_cards()

        # And if 15 cards is not enough, we'd better shuffle the deck
        elif not self.board.has_set() and len(self.board.table) == table_limit:
            cards = random.shuffle(self.board.deck + self.board.table)
            new_deck = cards[table_size:]
            new_table = cards[:table_size]
            self.board = Board(new_deck, new_table)
        assert(len(self.board.table) <= table_limit)

    def get_user_turn(self, limit=3):
        if len(self.board.selected) == limit:
            if self.board.is_set(self.board.selected):
                print round((time.clock() - self.time), limit)
                self.time = time.clock()
                return self.board.selected

            self.board.selected = set()

    def ask_exit(self):
        self.draw_end_button = True

game = GUIGame(game_name, window_size)
game.main()