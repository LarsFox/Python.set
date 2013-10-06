import os, itertools, random, time
from sys import exit

table_size = 12
quantity = 3

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
    def form_deck(cls):
        return [Card(*attrs) for attrs in
                itertools.product(cls.numbers, cls.symbols,
                                  cls.fill, cls.colours)]

    @classmethod
    def initial(cls, players=3):
        cards = cls.form_deck()
        random.shuffle(cards)
        table, deck = cards[:table_size], cards[table_size:]
        players = {x: [] for x in xrange(players)}
        return cls(deck, table, players, time.clock())

    def __init__(self, deck, table, players, start_time):
        self.deck = deck
        self.table = table
        self.players = players
        self.selected = []

        self.start_time = time.clock()

        self.reset_status()

    def reset_status(self):
        self.player_turn = None
        self.turn_time = 0

    def set_status(self, player_id, turn_time):
        self.player_turn = player_id
        self.turn_time = turn_time

    def is_set(self, cards):
        assert(len(cards) == 3)
        for i in xrange(4):
            if len(set(card.attr[i] for card in cards)) == 2:
                return False
        return True
 
    def has_set(self):
        for cards in itertools.combinations(self.table, r=3):
            if self.is_set(cards):
                return cards
        return False

    def success(self):
        self.players[self.player_turn].append(self.selected)
        self.reset_status()

    def replace_set(self):
        assert(self.selected)
        print 'REP'
        new_table, new_deck = self.table[:], self.deck[:]
        replacing_card_indexes = [i for i in xrange(len(new_table))
                                    if new_table[i] in self.selected][::-1]

        for i in replacing_card_indexes:
            new_table[i] = new_deck.pop(0)

        return Board(new_deck, new_table, self.players, self.start_time)

    def remove_set(self):
        print 'REM'
        new_table = [card for card in self.table if card not in self.selected]
        return Board(self.deck, new_table, self.players, self.start_time)

    def add_cards(self):
        new_table = self.table + self.deck[:quantity]
        new_deck = self.deck[quantity:]
        return Board(new_deck, new_table, self.players, self.start_time)

    def penalty(self):
        if self.players.get(self.player_turn, False):
            new_deck = self.deck + self.players[self.player_turn].pop()
            random.shuffle(new_deck)

            return Board(new_deck, self.table, self.players, self.start_time)

        return Board(self.deck, self.table, self.players, self.start_time)

    def has_more_turns(self):
        return self.deck or self.has_set()

class Game(object):
    def __init__(self):
        self.board = None
 
    def start(self):
        self.board = Board.initial()

    def main(self):
        self.start()

        while True:
            # If the deck isn't empty, check whether there's need to add cards.
            if self.board.deck:
                self.check()

            # Draw/print + grab the keys.
            self.display()
            self.keys_controller()

            player_found_set = self.get_user_turn()

            # Player claims that he has found the set
            if player_found_set is True:
                # If there's need and posibility to replace, replace.
                if self.board.deck and len(self.board.table) <= table_size:
                    self.board = self.board.replace_set()
                else:
                    self.board = self.board.remove_set()

            # If he has mistaken, punish him a bit.
            elif player_found_set is False:
                self.board = self.board.penalty()

            # And if he did nothing and keeps thinking, don't reset anything.
            if player_found_set is not None:
                self.board.reset_status()

            if not self.board.has_more_turns():
                self.ask_exit()
 
    def check(self):
        while not self.board.has_set():
            self.board = self.board.add_cards()

    def get_user_turn(self):
        while True:
            cards = self.ask_for_cards()
            if self.board.is_set(cards):
                return cards