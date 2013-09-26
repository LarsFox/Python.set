# this thing is commented to prevent pygame from crashing
# move all the inputs one level up

from sys import exit
from random import choice, shuffle

from data import *

class Engine():

    def __init__(self):
        self.deck = [Card(q, c, f, s)
            for q in quantity for c in colours for f in fill for s in shapes]
        self.table, self.gone = [], []

    def is_set(self, ca):
        for i in xrange(4):
            if len(set([card.attr[i] for card in ca])) == 2: return False
        return True

    def launch(self):
        shuffle(self.deck)
        self.table, self.deck = self.deck[:12], self.deck[12:]

    def print_cards(self):
        for i in xrange(0, len(self.table), 3):
            print '{0}. {3}\t| {1}. {4}\t| {2}. {5}'.format(i+1, i+2, i+3,
                self.table[i], self.table[i+1], self.table[i+2])

    def turn(self):
        # TEAR THIS INTO GAME
        while self.deck:
            while not self.has_set(self.table):
                self.table += self.deck[:3]
                self.deck = self.deck[3:]
                if len(self.table) == 15:
                    # print '15 cards and no set!'
                    self.deck += self.table
                    self.table = []
                    shuffle(deck)
                    self.table, self.deck = self.deck[:12], self.deck[12:]

            break
            #self.print_cards()
            self.action()

        #while self.has_set(self.table):
            #self.print_cards()
            #self.action()

        #self.deck, self.table, self.gone, = self.gone + self.table, [], []


    def action(self): # use re and fix any coming errors with wrong format
        s = raw_input('\nChoose set:\n> ')
        s = [int(x)-1 for x in s.split()]
        while not self.is_set([self.table[i] for i in s]):
            s = raw_input('\nNot a set!\n> ')
            s = [int(x)-1 for x in s.split()]

        for i in s[::-1]:
            if len(self.table) <= 12 and self.deck:     # replace card
                self.gone.append(self.table[i])
                self.table[i] = self.deck.pop(0)
            else: self.gone.append(self.table.pop(i))   # no replacements left

    def has_set(self, array):
        for i in xrange(len(array)):
            for j in xrange(i+1, len(array)):
                for k in xrange(j+1, len(array)):
                    if self.is_set([array[i], array[j], array[k]]):
                        #print i+1, j+1, k+1 # cheat to see sets easily
                        return True
        return False

#engine = Engine()
#try: engine.launch()
#except EOFError: print "Bye!"