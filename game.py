import os, itertools, random
from sys import exit

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

    table_size = 12
    
    @classmethod
    def form_deck(cls):
        return [Card(*attrs) for attrs in
                itertools.product(cls.numbers, cls.symbols,
                                  cls.fill, cls.colours)]

    @classmethod
    def initial(cls):
        cards = cls.form_deck()
        random.shuffle(cards)
        table, deck = cards[:cls.table_size], cards[cls.table_size:]
        return cls(deck, table)

    def __init__(self, deck, table):
        self.deck = deck
        self.table = table
        self.selected = []

    def add_cards(self, quantity=3):
        new_table = self.table + self.deck[:quantity]
        new_deck = self.deck[quantity:]
        return Board(new_deck, new_table)
 
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

    def penalty(self, cards):
        return Board(random.shuffle(self.deck + cards), self.table)
 
    def remove_set(self, cards, table_size=12):
        assert(self.is_set(cards))
        to_del = [i for i in xrange(len(self.table)) if self.table[i] in cards]
        
        for i in to_del[::-1]:
            if self.deck and len(self.table) <= table_size:
                self.table[i] = self.deck.pop(0)
            else:
                self.table.pop(i)

        return Board(self.deck, self.table)
 
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
            if self.board.deck:
                self.check()
            
            self.display()
            self.keys_controller()

            cards = self.get_user_turn()
            if cards:
                self.board = self.board.remove_set(cards)

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