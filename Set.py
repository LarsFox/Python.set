#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The Set! game.
# using pygame.
#
# Leo Motovksikh, 2013
# multicoloursocks@gmail.com
#
# "If I enter Laconia, I will raze Sparta."
# "If."
#

import itertools
import sys
import time

import pygame
from pygame.locals import *

from data import ICON, PALETTE, \
                 HEADER, LINES, SIZE16, SIZE18, \
                 EMPTY_CARD, SELECTION, CARD_ROWS, \
                 CARD_WIDTH, CARD_HEIGHT, CARD_SPACE, \
                 CARD_START_X, CARD_START_Y, \
                 NAME_TEMPLATE, SYMBOL_X, SYMBOL_Y, \
                 SYMBOL_WIDTH, SYMBOL_HEIGHT, SYMBOL_SPACE, \
                 START_BUTTON, END_BUTTON, HELP_BUTTON, SET_BUTTONS, \
                 common_font, time_font, round_time

from game import Card, Board, Game, \
                 PLAYERS, TABLE_SIZE, QUANTITY, SET_FOUND, SET_NOT_FOUND

# ================================= Example ===========================
class GUICard(Card):
    @property
    def image(self):
        image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        image = image.convert_alpha()
        image.fill(PALETTE['Empty'])
        image.blit(EMPTY_CARD, (0, 0))

        symbol_img = pygame.image.load(NAME_TEMPLATE(
            self.symbol[0], self.fill[0]))

        for i in xrange(int(self.number)):
            x, y = SYMBOL_X, SYMBOL_Y[self.number][i]

            pygame.draw.rect(image, PALETTE[self.colour],
                (x, y, SYMBOL_WIDTH, SYMBOL_HEIGHT))
            image.blit(symbol_img, (x, y))

        return image

EXAMPLE_X, EXAMPLE_Y = 415, 45
EXAMPLE_ROWS = 2
SET_EXAMPLE = [
    GUICard('1', 'diamond', 'empty', 'green'),
    GUICard('2', 'squiggle', 'striped', 'purple'),
    GUICard('3', 'oval', 'filled', 'red'),
    GUICard('2', 'squiggle', 'filled', 'purple'),
    GUICard('2', 'diamond', 'filled', 'red'),
    GUICard('2', 'oval', 'filled', 'green'),
]


# ///////////////////////////////// GUIGame ///////////////////////////
GAME_NAME = "Set!"

# Everything is in here only because it's rarely relative
# to console game; or at least seem to be non-relative.
# That is why all the drawings/countdowns/roundings are here.
#
# Remember:
# GUIGame differs a lot from Console game.


# E.g. the display can draw help or can draw table.
HELP = 'help'
TABLE = 'table'


# Then:
# check() function differs a lot, because of the screen size limit.
# In real game player can add up to 21 card if there're still no sets.
# Same with ConsoleGame.


# But in GUIGame there's TABLE_LIMIT due_to window size.
# So the game will never draw more than the window could fit in.
WINDOW_SIZE = (800, 600)
TABLE_LIMIT = 15
CLOCK = pygame.time.Clock()
FPS = 30


# The input is also different.
# In ConsoleGame you make an input which refers to some cards.
# The input can be valid or not.

# In GUIGame user clicks 'Set!' button to show that he has found a set.
# Then he has some time to click on the valid cards.
TIME_LIMIT = 8

# Timers are refreshing too fast, so the specific area is created.
TIMER_AREA_COORD = (660, 520)

# Thing to-do: Timers' roundings kill all the 0 sometimes

# Here we go.

class GUIGame(Game):
    def __init__(self, name, WINDOW_SIZE):
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_icon(ICON)
        self.pyclock = pygame.time.Clock()

        # Saves each turn's time; doesn't reset with each new game.
        self.turns_times = []

        self.display_draws = HELP       # Show help on launch.
        self.cards_drawn = False        # Wait until the game is ready


    # ============================ Game Mechanics =====================

    # THE GAME IS LAUNCHED WITH MAIN FROM CONSOLE GAME!!

    # Starts the new game on table
    # NOT a recursion: just sets all the data to 0.
    def start(self, PLAYERS):               
        self.board = Board.initial(GUICard)

        # Clear the ingame data.
        self.start_turn_time = time.clock()
        self.set_time = 0
        self.players = {x: [] for x in xrange(PLAYERS)}

        #self.cards_drawn = False
        self.table_clickable = False    # Is it possible to select cards?
        self.draw_END_BUTTON = False    # Draw 'No Sets' and block the game?

        self.player_turn = None         # Whose turn (== player_id or None)

    # Adds cards if necessary
    def check(self):
        in_set = self.board.has_set()

        # 1. Add up to 12 cards
        if len(self.board.table) < TABLE_SIZE:
            self.board = self.board.add_cards()

        # 2. Continue adding cards until there's a set
        elif not in_set and len(self.board.table) < TABLE_LIMIT:
            self.board = self.board.add_cards()

        # 3. Reshuffle if no set and window can't handle more cards
        elif not in_set and len(self.board.table) == TABLE_LIMIT:
            cards = random.shuffle(self.board.deck + self.board.table)
            new_deck = cards[TABLE_SIZE:]
            new_table = cards[:TABLE_SIZE]
            self.board = Board(new_deck, new_table)

        # 4. Break if added more than window can handle
        assert(len(self.board.table) <= TABLE_LIMIT)

    # Gets the cards selected by user
    def get_user_turn(self, err=0.05):
        if self.table_clickable:

            # 1. 3 cards selected
            if len(self.board.selected) == QUANTITY:
                if self.board.is_set(self.board.selected):
                    self.table_clickable = False
                    return SET_FOUND

                # 1.2 It is not set; clear the selection
                self.board.selected = []

            # 2. User hasn't selected set in time
            elif time.clock() > self.set_time + TIME_LIMIT - err:
                self.table_clickable = False
                self.board.selected = []
                return SET_NOT_FOUND

    # Shows 'Game over'
    def ask_exit(self):
        self.draw_END_BUTTON = True


    # ============================ Drawings Tree ======================
    def display(self):
        def draw_start_text(x=15, y=15, padding_top=36):
            screen.blit(HEADER, (x, y))
            y += padding_top

            for line in LINES['start']:
                screen.blit(line, (x, y))
                y += SIZE16

        def draw_buttons():
            HELP_BUTTON.draw(screen)
            START_BUTTON.draw(screen)
            if self.draw_END_BUTTON:
                END_BUTTON.draw(screen)

        def draw_PLAYERS():
            for i in xrange(len(SET_BUTTONS)):
                text = LINES['player'].format(i+1, len(self.players[i]))
                screen.blit(common_font(text), SET_BUTTONS[i].text)
                if not self.draw_END_BUTTON:
                    SET_BUTTONS[i].draw(screen)


        # As it mentioned in pygame documentation, it helps the CPU
        tickFPS = CLOCK.tick(FPS)
        screen = pygame.display.get_surface()
        screen.fill(PALETTE['Background'])

        draw_buttons()

        if self.display_draws == HELP:
            draw_start_text()
            self.draw_cards(screen, False)

        else:
            draw_PLAYERS()
            # If there are cards to display, they will be displayed
            if self.board.table:
                self.draw_cards(screen)

        if self.cards_drawn:
            self.draw_turn_timer(screen)
            self.draw_stats(screen)
            self.set_countdown(screen)

        pygame.display.update()



    # ========================= Draw Cards Function ===================
    # Ss on module level because it is also used in drawing
    # SET_EXAMPLE in help menu (draw_table=False).
    #
    # With draw_table=True draws SELECTIONs, creates a card click-area
    # and allowes the game to launch safely (self.cards_drawn = True).

    def draw_cards(self, screen, draw_table=True):
        if draw_table:
            x, y = CARD_START_X, CARD_START_Y
            rows = CARD_ROWS
            cards = self.board.table
        else:
            x, y = EXAMPLE_X, EXAMPLE_Y
            rows = EXAMPLE_ROWS
            cards = SET_EXAMPLE

        columns = len(cards)/rows
        card_x, card_y = x, y

        for row in xrange(0, len(cards), columns):
            for column in xrange(columns):
                i = row + column
                card = cards[i]
                screen.blit(card.image, (card_x, card_y))

                if draw_table:
                    card.rect = pygame.Rect(
                        (card_x, card_y), (CARD_WIDTH, CARD_HEIGHT))

                    if card in self.board.selected:
                        screen.blit(SELECTION, (card_x-2, card_y-2))
                
                card_x += CARD_WIDTH + CARD_SPACE

            card_x = x
            card_y += CARD_HEIGHT + CARD_SPACE

        if draw_table and not self.cards_drawn:
            self.cards_drawn = True


    # =============================== Statuses ==============================

    # The size of this area is exactly to fit in the refreshing timer. 
    @property
    def timer_area(self, x=140, y=18):
        area = pygame.Surface((x, y))
        area.fill(PALETTE['Background'])
        return area

    def draw_turn_timer(self, screen, x=60, y=0, padding=60):
        timer_area = self.timer_area

        # Turn's timer stops when 'Set!' is clicked.
        if not self.draw_END_BUTTON:
            if self.set_time:
                current_time = round_time(self.set_time - self.start_turn_time)

            else:
                current_time = round_time(time.clock() - self.start_turn_time)

            timer_area.blit(LINES['current'], (x-padding, y))
            timer_area.blit(time_font(current_time, 'Black'), (x, y))

            screen.blit(timer_area, TIMER_AREA_COORD)

    def draw_stats(self, screen, x=720, y=538):
        def draw_stat(text, num, x, y, colour='Black', padding=60):
            screen.blit(text, (x-padding, y))
            screen.blit(time_font(num, colour), (x, y))


        if self.turns_times:
            last_time = round_time(self.turns_times[-1])
            draw_stat(LINES['last'], last_time, x, y, 'Red')

            y += SIZE18

            best_time = round_time(min(self.turns_times))
            draw_stat(LINES['best'], best_time, x, y, 'Green')

            y += SIZE18

            # The only word one symbol longer.
            total = str(len(self.turns_times))
            draw_stat(LINES['total'], total, x, y, 'Emerald', padding=70)

    def set_countdown(self, screen, space=3):
        # Display side turn timer when the 'Set!' button is clicked.
        if self.display_draws == TABLE and self.player_turn is not None:
            button = SET_BUTTONS[self.player_turn]
            timer_x = button.coord[0]
            timer_y = button.coord[1] + button.size[1] + space
            
            timer = round_time(TIME_LIMIT - (time.clock() - self.set_time))
            screen.blit(time_font(timer, 'Red'), (timer_x, timer_y))



    # =========================== Keys Controller ===========================
    def key_input(self):
        def click_buttons():
            # New Game is clicked.
            if START_BUTTON.rect.collidepoint(event.pos):
                self.start(PLAYERS)
                self.display_draws = TABLE

            # Help button is clicked.
            if HELP_BUTTON.rect.collidepoint(event.pos):
                # Very first reading of rules doesn't count as turn's time.
                if not self.cards_drawn:
                    self.turns_times = []
                    self.start_turn_time = time.clock()
                    self.set_time = 0

                if self.display_draws == HELP:
                    self.display_draws = TABLE
                else:
                    self.display_draws = HELP

            # 'Set!' button is clickable, when we have cards and game to play.
            if all([not self.table_clickable,
                        self.cards_drawn, not self.draw_END_BUTTON]):

                for i in xrange(len(SET_BUTTONS)):
                    if SET_BUTTONS[i].rect.collidepoint(event.pos):
                        self.table_clickable = True
                        self.player_turn = i
                        self.set_time = time.clock()

        def click_cards():
            for card in self.board.table:
                if card.rect.collidepoint(event.pos):

                    if card not in self.board.selected:
                        self.board.selected.append(card)
                    else:
                        self.board.selected.remove(card)


        # Main pygame loop
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:

                click_buttons()

                if self.table_clickable:
                    click_cards()

            if event.type == KEYDOWN and event.key == K_s:     # cheat
                print [card.attr for card in self.board.has_set()]

game = GUIGame(GAME_NAME, WINDOW_SIZE)
game.main()
