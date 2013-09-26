from sys import exit
from random import choice, shuffle

from data import *

class Engine():

    def __init__(self):
        self.deck = [Card(q, c, f, s)
            for q in quantity for c in colours for f in fill for s in shapes]
        self.table, self.gone = [], []

    def is_set(self, array):   # checking for Set with the set HAHAHA
        for i in xrange(4):
            if len(set([card.attr[i] for card in array])) == 2: return False
        return True

    def launch(self):
        shuffle(self.deck)
        self.table, self.deck = self.deck[:12], self.deck[12:]

    def action(self, array): # no more than 12 cards (game rules)
        a = sorted(array, cmp=lambda x, y: y.index-x.index)
        for card in array:
            if len(self.table) <= 12 and self.deck:
                self.gone.append(self.table[card.index])
                self.table[card.index] = self.deck.pop(0)
            else: self.gone.append(self.table.pop(card.index))

    def has_set(self, array):
        for i in xrange(len(array)):
            for j in xrange(i+1, len(array)):
                for k in xrange(j+1, len(array)):
                    if self.is_set([array[i], array[j], array[k]]):
                        return i+1, j+1, k+1 # cheat by pressing Up
                        return True
        return False