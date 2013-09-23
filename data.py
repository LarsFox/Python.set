qs = (1, 2, 3)  # or 0, 1, 2?
cs = ('red', 'green', 'purple')
fs = ('empty', 'striped', 'filled')
ss = ('Oval', 'Squiggle', 'Diamond')

class Card():

    def __init__(self, q, c, f, s):
        self.attr = self.q, self.c, self.f, s = q, c, f, s

    def __str__(self):
        s = ''
        if self.q > 1: s = 's'
        return '{} {} {} {}{}'.format(self.q, self.c, self.f, s, s)