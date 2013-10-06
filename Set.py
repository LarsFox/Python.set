#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The Set game.
# using pygame.
#
# Leo Motovksikh, 2013
# multicoloursocks@gmail.com
#
# "If I enter Laconia, I will raze Sparta."
# "If."
#

import pygame
from pygame.locals import *

from game import *
import strings

game_name = "Set"
window_size = (800, 600)
palette = {
    'Light Grey':   (200, 200, 200),    'green':        ( 55, 205,  65),
    'red':          (255,   0, 120),    'purple':       (120, 120, 210),
    'Black':        (  0,   0,   0),    'Empty':        (0,  0,  0,  0),
    'Red':          (240,  50,  50),    'Green':        (  0, 150,  17)
}

icon = pygame.image.load('images/icon.png')

table_limit = 15
time_limit = 5

# ================================== Fonts ==================================
pygame.font.init()
consolas = 'images/consolas.ttf'
maiandra_gd = 'images/maiandra_gd.ttf'
antialasing = True
size16 = 16
size18 = 18

header_font = pygame.font.Font(maiandra_gd, size18)
header = header_font.render(strings.header, antialasing, palette['Black'])

common_font = pygame.font.Font(maiandra_gd, size16)
def c_font(text, colour='Black'):
    return common_font.render(text, antialasing, palette[colour])

time_str = '{:0<4}'
time_font = pygame.font.Font(consolas, size18)

def t_font(text, colour):
    return time_font.render(text, antialasing, palette[colour])

# =================================== Card ==================================
empty_card = pygame.image.load('images/card.png')
selection = pygame.image.load('images/selection.png')
card_width, card_height, card_space = 106, 160, 10
card_start_x, card_start_y = 170, 15

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
    def draw(self, screen):
        self.rect = pygame.Rect(self.coord, self.size)
        screen.blit(self.image, self.coord)

class DownButton(Button):
    def __init__(self, image, x, y=520, size=(216, 57)):
        self.image = pygame.image.load(image)
        self.coord = (x, y)
        self.size = size

start_button = DownButton('images/start.png', 170)

end_button = DownButton('images/over.png', 396)

help_button = DownButton('images/help.png', 15, size=(140, 57))

class SetButton(Button):
    def __init__(self, y):
        self.image = pygame.image.load('images/set.png')
        self.coord = [20, y]
        self.size = (130, 42)

    @property
    def text(self, space=5):
        return self.coord[0], self.coord[1] - size16 - space

set_buttons = [SetButton(74+i*170) for i in xrange(3)]

# =============================== GUI Classes ===============================
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

# ================================= Example =================================
example_x, example_y = 415, 45
set_example = [
    GUICard('1', 'diamond', 'empty', 'green'),
    GUICard('2', 'squiggle', 'striped', 'purple'),
    GUICard('3', 'oval', 'filled', 'red'),
    GUICard('2', 'squiggle', 'filled', 'purple'),
    GUICard('2', 'diamond', 'filled', 'red'),
    GUICard('2', 'oval', 'filled', 'green'),
]



# ================================= GUIGame =================================

# Everything is in here only because it's rarely relative to console game
# Or at least seem to be non-relative
# That is why all the drawings/displays/countdowns/roundings are here

# Thing to-do: Timers' roundings kill all the 0 sometimes. Fix

class GUIGame(Game):
    def __init__(self, name, window_size):
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_mode(window_size)
        pygame.display.set_icon(icon)

        # These vars don't reload with every new game
        self.best_time = 0
        self.last_time = 0
        self.draw_help = True

        # The get-click function dies when cards are not drawn
        self.cards_drawn = False

    def start(self):
        # This is some kind of reset.
        self.board = GUIBoard.initial()
        self.cards_drawn = False
        self.table_clickable = False    # No card clicks until 'SET!' is called
        self.draw_end_button = False    # Draws 'No Sets' and blocks the game.

    def display(self):
        screen = pygame.display.get_surface()
        screen.fill(palette['Light Grey'])

        self.draw_buttons(screen)

        # The display has two states: help is shown / game is shown
        if self.draw_help:
            self.display_start_text(screen)
        else:
            self.draw_players(screen, i)
            # If there are cards to display, they will be displayed
            if self.board.table:
                self.draw_cards(
                    screen, self.board.table, card_start_x, card_start_y)

        # Timers change with each frame, time doesn't
        if self.cards_drawn:
            self.draw_time(screen)
            self.draw_timers(screen)

        pygame.display.flip()

    def display_start_text(self, screen, x=15, y=15, padding_top=36):
        screen.blit(header, (x, y))
        y += padding_top

        for line in strings.start:
            screen.blit(c_font(line), (x, y))
            y += size16

        self.draw_cards(screen, set_example, example_x, example_y, 2, False)

    def draw_buttons(self, screen):
        help_button.draw(screen)
        start_button.draw(screen)
        if self.draw_end_button:
            end_button.draw(screen)

    def draw_cards(self, screen, cards, x, y, rows=3, on_table=True):
        # on_table allowes to draw set_example with the same function,
        # but without setting clickable areas and selections
        columns = len(cards)/rows
        card_x, card_y = x, y

        for row in xrange(0, len(cards), columns):
            for column in xrange(columns):
                i = row + column
                card = cards[i]
                screen.blit(card.image, (card_x, card_y))

                if on_table:
                    card.rect = pygame.Rect(
                        (card_x, card_y), (card_width, card_height))

                    if card in self.board.selected:
                        screen.blit(selection, (card_x-2, card_y-2))
                
                card_x += card_width + card_space

            card_x = x
            card_y += card_height + card_space

        if on_table:
            self.cards_drawn = True

    def draw_players(self, screen, i):
        for i in xrange(len(set_buttons)):
            text = strings.player.format(i+1, len(self.board.players[i]))
            screen.blit(c_font(text), set_buttons[i].text)
            if not self.draw_end_button:
                set_buttons[i].draw(screen)

    def draw_time(self, screen, x=700, y=548, pt=2, padding=60):
        if self.last_time:
            screen.blit(t_font(strings.last, 'Red'), (x-padding, y))
            text = time_str.format(round((self.last_time), pt))
            screen.blit(t_font(text, 'Red'), (x, y))

        if self.best_time:
            y += size18
            screen.blit(t_font(strings.best, 'Green'), (x-padding, y))
            text = time_str.format(round((self.best_time), pt))
            screen.blit(t_font(text, 'Green'), (x, y))

    def draw_timers(self, screen, x=700, y=530, pt=2, space=3, padding=110):
        # When the 'Set' button is clicked, the timer stops
        if self.board.turn_time:
            num = time_str.format(
                round(self.board.turn_time - self.board.start_time, pt))

            # Player's turn timer
            if not self.draw_help:
                timer = (time_limit - (time.clock() - self.board.turn_time))
                timer = time_str.format(round(timer, pt))
                button = set_buttons[self.board.player_turn]
                timer_x = button.coord[0]
                timer_y = button.coord[1] + button.size[1] + space
                screen.blit(t_font(timer, 'Red'), (timer_x, timer_y))

        else:
            num = time_str.format(
                round((time.clock() - self.board.start_time), pt))

        screen.blit(t_font(strings.current, 'Black'), (x-padding, y))
        screen.blit(t_font(num, 'Black'), (x, y))

    def keys_controller(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            self.click_buttons(event)

            if self.cards_drawn and self.table_clickable:
                self.click_cards(event)

            ''' To enable the cheat, decomment and press S
                the cards full names will appear in console.'''

            if event.type == KEYDOWN and event.key == K_s:
                print self.board.players
                
                print len(self.board.deck)
                print [card.attr for card in self.board.has_set()]

    def click_buttons(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # New Game is clicked
            if start_button.rect.collidepoint(event.pos):
                self.start()
                self.draw_help = False

            # Help button is clicked
            if help_button.rect.collidepoint(event.pos):
                # Very first reading of rules shouldn't count as turn's time.
                if not self.cards_drawn:
                    self.board.start_time = time.clock()

                if self.draw_help:
                    self.draw_help = False
                else:
                    self.draw_help = True

            # Set button is clicked, when we have cards and game to play
            if all([not self.table_clickable,
                        self.cards_drawn, not self.draw_end_button]):

                for i in xrange(len(set_buttons)):
                    if set_buttons[i].rect.collidepoint(event.pos):
                        self.table_clickable = True
                        self.board.set_status(i, time.clock())

    def click_cards(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for card in self.board.table:
                if card.rect.collidepoint(event.pos):

                    if card not in self.board.selected:
                        self.board.selected.append(card)
                    else:
                        self.board.selected.remove(card)

    def check(self):
        # Chooses whether to add more cards or not (based on real-game rules)

        in_set = self.board.has_set()
        # If we have less than 12 cards, we add more
        if len(self.board.table) < table_size:
            self.board = self.board.add_cards()

        # Based on window size: if 12 <= cards < 15 is not enough, we add more.
        elif not in_set and len(self.board.table) < table_limit:
            self.board = self.board.add_cards()

        # And if 15 cards is not enough, we'd better shuffle the deck
        elif not in_set and len(self.board.table) == table_limit:
            cards = random.shuffle(self.board.deck + self.board.table)
            new_deck = cards[table_size:]
            new_table = cards[:table_size]
            self.board = Board(new_deck, new_table)
        assert(len(self.board.table) <= table_limit)

    def record_time(self):
        self.last_time = self.board.turn_time - self.board.start_time
        if self.best_time > self.last_time or not self.best_time:
            self.best_time = self.last_time

    def get_user_turn(self, cards_per_turn=3, err=0.05):
        # The input in GUIGame differs a lot from the ConsoleGame's one, e.g.
        # GUI: update board.selected with each click
        # Console: board.selected = input

        if self.table_clickable:
            # ...so the valid form checking is much easier:
            if len(self.board.selected) == cards_per_turn:
                if self.board.is_set(self.board.selected):
                    self.record_time()

                    self.table_clickable = False

                    self.board.success()
                    return True

                # Player can missclick, give him another try.
                self.board.selected = []

            # in console game there's no turn timer
            # the set form is whether correct or not.
            elif time.clock() > self.board.turn_time + time_limit - err:
                self.table_clickable = False
                self.board.selected = []
                return False

        return None

    def ask_exit(self):
        self.draw_end_button = True

game = GUIGame(game_name, window_size)
game.main()
