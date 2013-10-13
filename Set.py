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

from data import icon, palette, \
                 common_font, time_font, round_time, \
                 header, lines, size16, size18, \
                 empty_card, selection, card_rows, \
                 card_width, card_height, card_space, \
                 card_start_x, card_start_y, \
                 name_template, symbol_x, symbol_y, \
                 symbol_width, symbol_height, symbol_space, \
                 start_button, end_button, help_button, set_buttons

from game import Card, Board, Game, \
                 players, table_size, set_found, set_not_found

# ================================= Example =================================
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

example_x, example_y = 415, 45
example_rows = 2
set_example = [
    GUICard('1', 'diamond', 'empty', 'green'),
    GUICard('2', 'squiggle', 'striped', 'purple'),
    GUICard('3', 'oval', 'filled', 'red'),
    GUICard('2', 'squiggle', 'filled', 'purple'),
    GUICard('2', 'diamond', 'filled', 'red'),
    GUICard('2', 'oval', 'filled', 'green'),
]


# ///////////////////////////////// GUIGame /////////////////////////////////

game_name = "Set!"

# Everything is in here only because it's rarely relative to console game
# Or at least seem to be non-relative
# That is why all the drawings/displays/countdowns/roundings are here
#
# Remember:
# GUIGame differs a lot with Console game.
#
# The display can draw help or can draw table.

help = 'help'
table = 'table'

# check() function differs a lot, because of the screen size limit.
# In real game players can add up to 21 card if there're still no sets.
# Same with ConsoleGame.
# In GUIGame there's table_limit which is used because of the window size.
# So the game will never draw more than it could handle in.

window_size = (800, 600)
table_limit = 15
fps = 30

# The input is also different.
# In ConsoleGame you make an input which refers to some cards.
# The input can be valid or not.
# In GUIGame user clicks 'Set!' button to show that he has found a set.
# Then he has a few seconds to click on the valid cards.

time_limit = 8

# Timers are refreshing too fast, so the specific area is created for them.

timer_area_coord = (640, 520)

# Thing to-do: Timers' roundings kill all the 0 sometimes

class GUIGame(Game):
    def __init__(self, name, window_size):
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_mode(window_size)
        pygame.display.set_icon(icon)
        self.pyclock = pygame.time.Clock()

        screen = pygame.display.get_surface()
        screen.fill(palette['Light Grey'])

        # Saves each turn's time; doesn't reset with each new game.
        self.turns_times = []

        self.display_draws = help       # Show help on launch.
        self.cards_drawn = False        # Wait until the game is ready

    # ============================ Game Mechanics ===========================
    def start(self, players):
        self.board = Board.initial(GUICard)

        # Clear the ingame data.
        self.start_turn_time = time.clock()
        self.set_time = 0
        self.players = {x: [] for x in xrange(players)}

        self.cards_drawn = False        # Game has run succesfully;
        self.table_clickable = False    # Select cards after clicking 'Set!';
        self.draw_end_button = False    # Draws 'No Sets' and blocks the game;

        self.player_turn = None         # is equal to player_id or None


    def check(self):
        in_set = self.board.has_set()
        if len(self.board.table) < table_size:
            self.board = self.board.add_cards()

        elif not in_set and len(self.board.table) < table_limit:
            self.board = self.board.add_cards()

        elif not in_set and len(self.board.table) == table_limit:
            cards = random.shuffle(self.board.deck + self.board.table)
            new_deck = cards[table_size:]
            new_table = cards[:table_size]
            self.board = Board(new_deck, new_table)

        assert(len(self.board.table) <= table_limit)

    def get_user_turn(self, cards_per_turn=3, err=0.05):
        if self.table_clickable:
            if len(self.board.selected) == cards_per_turn:
                if self.board.is_set(self.board.selected):
                    self.table_clickable = False
                    return set_found

                # Player can missclick
                self.board.selected = []

            elif time.clock() > self.set_time + time_limit - err:
                self.table_clickable = False
                self.board.selected = []
                return set_not_found

    def ask_exit(self):
        self.draw_end_button = True


    # ============================ Drawings Tree ============================
    def display(self):
        def draw_start_text(x=15, y=15, padding_top=36):
            screen.blit(header, (x, y))
            y += padding_top

            for line in lines['start']:
                screen.blit(line, (x, y))
                y += size16

        def draw_buttons():
            help_button.draw(screen)
            start_button.draw(screen)
            if self.draw_end_button:
                end_button.draw(screen)

        def draw_players():
            for i in xrange(len(set_buttons)):
                text = lines['player'].format(i+1, len(self.players[i]))
                screen.blit(common_font(text), set_buttons[i].text)
                if not self.draw_end_button:
                    set_buttons[i].draw(screen)


        # As it mentioned in pygame documentation, it helps the CPU
        self.pyclock.tick(fps)
        screen = pygame.display.get_surface()
        screen.fill(palette['Light Grey'])

        draw_buttons()

        if self.display_draws == help:
            draw_start_text()
            self.draw_cards(screen, False)

        else:
            draw_players()
            # If there are cards to display, they will be displayed
            if self.board.table:
                self.draw_cards(screen)

        if self.cards_drawn:
            self.draw_turn_timer(screen)
            self.draw_stats(screen)
            self.set_countdown(screen)

        pygame.display.flip()



    # ========================= Draw Cards Function =========================
    # This function is on module level because it is also used in drawing
    # set_example in help menu (draw_table=False).
    #
    # With draw_table=True draws selections, creates a card click-area
    # and allowes the game to launch safely (self.cards_drawn = True).

    def draw_cards(self, screen, draw_table=True):
        if draw_table:
            x, y = card_start_x, card_start_y
            rows = card_rows
            cards = self.board.table
        else:
            x, y = example_x, example_y
            rows = example_rows
            cards = set_example

        columns = len(cards)/rows
        card_x, card_y = x, y

        for row in xrange(0, len(cards), columns):
            for column in xrange(columns):
                i = row + column
                card = cards[i]
                screen.blit(card.image, (card_x, card_y))

                if draw_table:
                    card.rect = pygame.Rect(
                        (card_x, card_y), (card_width, card_height))

                    if card in self.board.selected:
                        screen.blit(selection, (card_x-2, card_y-2))
                
                card_x += card_width + card_space

            card_x = x
            card_y += card_height + card_space

        if draw_table and not self.cards_drawn:
            self.cards_drawn = True


    # =============================== Statuses ==============================

    # The size of this area is exactly to fit in the refreshing timer. 
    @property
    def timer_area(self, x=160, y=18):
        area = pygame.Surface((x, y))
        area.fill(palette['Light Grey'])
        return area

    def draw_turn_timer(self, screen, x=60, y=0, padding=60):
        timer_area = self.timer_area

        # Turn's timer stops when 'Set!' is clicked.
        if not self.draw_end_button:
            if self.set_time:
                current_time = round_time(self.set_time - self.start_turn_time)

            else:
                current_time = round_time(time.clock() - self.start_turn_time)

            timer_area.blit(lines['current'], (x-padding, y))
            timer_area.blit(time_font(current_time, 'Black'), (x, y))

            screen.blit(timer_area, timer_area_coord)

    def draw_stats(self, screen, x=700, y=538):
        def draw_stat(text, num, x, y, colour='Black', padding=60):
            screen.blit(text, (x-padding, y))
            screen.blit(time_font(num, colour), (x, y))


        if self.turns_times:
            last_time = round_time(self.turns_times[-1])
            draw_stat(lines['last'], last_time, x, y, 'Red')

            y += size18

            best_time = round_time(min(self.turns_times))
            draw_stat(lines['best'], best_time, x, y, 'Green')

            y += size18

            # The only word one symbol longer.
            total = str(len(self.turns_times))
            draw_stat(lines['total'], total, x, y, 'Emerald', padding=70)

    def set_countdown(self, screen, space=3):
        # Display side turn timer when the 'Set!' button is clicked.
        if self.display_draws == table and self.player_turn is not None:
            button = set_buttons[self.player_turn]
            timer_x = button.coord[0]
            timer_y = button.coord[1] + button.size[1] + space
            
            timer = round_time(time_limit - (time.clock() - self.set_time))
            screen.blit(time_font(timer, 'Red'), (timer_x, timer_y))



    # =========================== Keys Controller ===========================
    def key_input(self):
        def click_buttons():
            # New Game is clicked.
            if start_button.rect.collidepoint(event.pos):
                self.start(players)
                self.display_draws = table

            # Help button is clicked.
            if help_button.rect.collidepoint(event.pos):
                # Very first reading of rules doesn't count as turn's time.
                if not self.cards_drawn:
                    self.turns_times = [time.clock()]

                if self.display_draws == help:
                    self.display_draws = table
                else:
                    self.display_draws = help

            # 'Set!' button is clickable, when we have cards and game to play.
            if all([not self.table_clickable,
                        self.cards_drawn, not self.draw_end_button]):

                for i in xrange(len(set_buttons)):
                    if set_buttons[i].rect.collidepoint(event.pos):
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

            #if event.type == KEYDOWN and event.key == K_s:     # cheat
                #print [card.attr for card in self.board.has_set()]

game = GUIGame(game_name, window_size)
game.main()
