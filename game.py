import itertools
import os
import random
import time

PLAYERS = 3
TABLE_SIZE = 12
QUANTITY = 3

SET_FOUND = 'Set'
SET_NOT_FOUND = 'No set'

class Card(object):
    def __init__(self, number, symbol, fill, colour):
        self.number = number
        self.symbol = symbol
        self.fill = fill
        self.colour = colour

    @property
    def attr(self):
        return (self.number, self.symbol, self.fill, self.colour)

class Board(object):
    numbers = ('1', '2', '3')
    symbols = ('diamond', 'squiggle', 'oval')
    fill = ('empty', 'striped', 'filled')
    colours = ('red', 'green', 'purple')

    @classmethod
    def initial(cls, card_type):
        def form_deck():
            return [card_type(*attrs) for attrs in
                    itertools.product(cls.numbers, cls.symbols,
                                      cls.fill, cls.colours)]
        cards = form_deck()
        random.shuffle(cards)
        table, deck = cards[:TABLE_SIZE], cards[TABLE_SIZE:]
        return cls(deck, table)

    def __init__(self, deck, table):
        self.deck = deck
        self.table = table
        self.selected = []

    def is_set(self, cards):
        assert(len(cards) == 3)
        for i in xrange(4):
            if len(set(card.attr[i] for card in cards)) == 2:
                return False
        return True
 
    def has_set(self):
        for cards in itertools.combinations(self.table, r=3):
            if self.is_set(cards):
                return True
                #return cards   # cheat
        return False

    def replace_set(self):
        assert(self.selected and self.deck)
        new_table, new_deck = self.table[:], self.deck[:]
        replacing_card_indexes = [i for i in xrange(len(new_table))
                                    if new_table[i] in self.selected][::-1]

        for i in replacing_card_indexes:
            new_table[i] = new_deck.pop(0)

        return Board(new_deck, new_table)

    def remove_set(self):
        new_table = [card for card in self.table if card not in self.selected]
        return Board(self.deck, new_table)

    def add_cards(self):
        new_table = self.table + self.deck[:QUANTITY]
        new_deck = self.deck[QUANTITY:]
        return Board(new_deck, new_table)

    def penalty(self, penalty_set):
        new_deck = self.deck + penalty_set
        random.shuffle(new_deck)
        return Board(new_deck, self.table)

    def has_more_turns(self):
        return self.deck or self.has_set()



# /////////////////////////////////// Game //////////////////////////////////
#
# A short brief to what's going on in here:
# The main thing is the main() function, so.
#
# Game spawns 12 cards. Game has launched.
#
# First of all, check() if there's need and possibility to add cards.
# If there are no set on a table, game adds until there's Set.
# Max table size = 21, it gives 100% chance of Set in it.
#
# After all table cards are drawn, input form proceeds.
# If a player provided the game with any input, input is checked to be valid.
# Then it's checked to be a Set.
# If it is not a Set, the player gives one Set from his pocket back to deck.
# If it is a Set, the player gets it in his pocket.
#
# The Set is 'replaced'. It means that new cards go to the same positions where
# the removed Set's cards were.
# If the deck is empty, Set is removed and game continues until no Sets left.
#
# In both cases, if there was any input, prepare the game for the next turn.

class Game(object):
    def __init__(self):
        self.board = None
 
    # Overridden in GUIGame
    def start(self, PLAYERS):
        self.board = Board.initial(Card)
        self.turns_times = [0]
        self.players = {x: [] for x in xrange(PLAYERS)}

    def main(self):
        self.start(PLAYERS)

        while True:
            if self.board.deck:
                self.check()

            self.display()
            self.key_input()

            player_found_set = self.get_user_turn()

            if player_found_set == SET_FOUND:
                self.players[self.player_turn].append(self.board.selected)

                if self.board.deck and len(self.board.table) <= TABLE_SIZE:
                    self.board = self.board.replace_set()

                else:
                    self.board = self.board.remove_set()

                self.turns_times.append(self.set_time - self.start_turn_time)
                self.start_turn_time = time.clock()

            elif player_found_set == SET_NOT_FOUND:
                if self.players[self.player_turn]:
                    removed_set = self.players[self.player_turn].pop(0)
                    self.board = self.board.penalty(removed_set)

            if player_found_set:
                self.player_turn = None
                self.set_time = 0

            if not self.board.has_more_turns():
                self.ask_exit()
 
    # Overridden in GUIGame
    def check(self):
        while not self.board.has_set():
            self.board = self.board.add_cards()

    # Overridden in GUIGame
    def get_user_turn(self):
        while True:
            cards = self.ask_for_cards()
            if self.board.is_set(cards):
                return cards

    # Overridden in GUIGame
    def ask_exit(self):
        pass