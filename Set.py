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

import time

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
class GUIGame(Game):
    def __init__(self, name, window_size):
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_mode(window_size)
        pygame.display.set_icon(icon)

        # Vars that don't reload with every new game
        self.best_time = 0
        self.last_time = 0
        self.draw_help = True

        # Cards' click area appears after(!) being drawn
        self.cards_drawn = False

    def start(self, players=3):
        # Vars that reload with every new game
        self.board = GUIBoard.initial()
        self.cards_drawn = False
        self.draw_end_button = False
        self.players = [[] for x in xrange(players)]
        self.reset_vars()

    def reset_vars(self):
        self.clickable = False
        self.turn_time = 0
        self.player_turn = None

    def display(self):
        screen = pygame.display.get_surface()
        screen.fill(palette['Light Grey'])

        self.draw_buttons(screen)

        if self.draw_help:
            self.display_start_text(screen)
        elif self.board.table:
            self.draw_cards(
                screen, self.board.table, card_start_x, card_start_y)
            self.draw_timers(screen)

            self.draw_players(screen, i)

        self.draw_time(screen)
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
            text = strings.player.format(i+1, len(self.players[i]))
            screen.blit(c_font(text), set_buttons[i].text)
            set_buttons[i].draw(screen)

    # All time roundings come here!
    def draw_time(self, screen, x=700, y=548, pt=2, padding=54):
        if self.last_time:
            screen.blit(t_font(strings.last, 'Red'), (x-padding, y))
            text = time_str.format(round((self.last_time), pt))
            screen.blit(t_font(text, 'Red'), (x, y))

        if self.best_time:
            y += size18
            screen.blit(t_font(strings.best, 'Green'), (x-padding, y))
            text = time_str.format(round((self.best_time), pt))
            screen.blit(t_font(text, 'Green'), (x, y))

    def draw_timers(self, screen, x=700, y=530, pt=2, space=3, padding=115):
        if self.turn_time:
            num = round(self.turn_time, pt)

            # Player turn timer
            timer = (time_limit - (time.clock() - self.turn_time))
            timer = time_str.format(round(timer, pt))
            button = set_buttons[self.player_turn]
            timer_x = button.coord[0]
            timer_y = button.coord[1] + button.size[1] + space
            screen.blit(t_font(timer, 'Red'), (timer_x, timer_y))

        else:
            num = time_str.format(round((time.clock() - self.new_time), pt))

        screen.blit(t_font(strings.current, 'Black'), (x-padding, y))
        screen.blit(t_font(str(num), 'Black'), (x, y))

    def keys_controller(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            self.click_buttons(event)

            if self.cards_drawn and self.clickable:
                self.click_cards(event)

            ''' To enable the cheat, decomment and press S
                the cards full names will appear in console.'''

            '''if event.type == KEYDOWN and event.key == K_s:
                print [card.attr for card in self.board.has_set()]'''

    def click_buttons(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # New Game is clicked
            if start_button.rect.collidepoint(event.pos):
                self.start()
                self.new_time = time.clock()
                self.draw_help = False

            # Help button is clicked
            if help_button.rect.collidepoint(event.pos):
                if not self.cards_drawn:
                    self.new_time = time.clock()

                if self.draw_help:
                    self.draw_help = False
                else:
                    self.draw_help = True

            # Set button is clicked
            if not self.clickable and self.cards_drawn:
                for i in xrange(len(set_buttons)):
                    if set_buttons[i].rect.collidepoint(event.pos):
                        self.player_turn = i
                        self.clickable = True
                        self.turn_time = time.clock()

    def click_cards(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for card in self.board.table:
                if card.rect.collidepoint(event.pos):

                    if card not in self.board.selected:
                        self.board.selected.append(card)
                    else:
                        self.board.selected.remove(card)

    def check(self, table_limit=15, table_size=12, quantity=3):
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

    def get_user_turn(self, limit=3, err=0.05):
        if self.clickable:
            if len(self.board.selected) == limit:
                if self.board.is_set(self.board.selected):

                    self.last_time = self.get_time - self.new_time
                    if self.best_time > self.last_time or not self.best_time:
                        self.best_time = self.last_time

                    self.players[self.player_turn].append(self.board.selected)

                    self.new_time = time.clock()
                    self.reset_vars()
                    return self.board.selected

                self.board.selected = []

            if time.clock() > self.turn_time + time_limit - err:
                if self.players[self.player_turn]:
                    self.board = self.board.penalty(
                        self.players[self.player_turn].pop())
                self.reset_vars()

    def ask_exit(self):
        self.draw_end_button = True

game = GUIGame(game_name, window_size)
game.main()