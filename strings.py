# -*- coding: utf-8 -*-
# probably there's need in languages
header = '''Welcome to the Set game!'''

# Common text, data is with no prefixes.
start = '''The goal of this game is to find... sets!

You'll be shown some cards as you press 'New Game'

Each card has four features:
  number (one, two, or three);
  symbol (diamond, squiggle, oval);
  shading (solid, striped, or open);
  colour (red, green, or purple).

A combination of three cards is called set.
To make a set, each cards' feature must be totally
different or totally same with the rest two cards,
e.g. there are two sets here.

To sum up, if three cards form a group of
'Two of ___ and one of ___', then it is not a set.

If there's no set in twelve cards, three more are added.
If there's still no set, the remaining cards reshuffle.

If a player finds set, click his 'Set!' button.
You'll have 8 seconds to click your set.
Failing to find the set when 'Set!' is clicked will take one \
set back to deck.

'Help':          Toggle on/off this screen.
'New Game': Shuffle the deck and start a new round.
'No sets':       Game is over, you have no more sets on the table. \
Start the new one!
'''.split('\n')

current = 'This turn: '
last = 'Last: '
best = 'Best: '
player = 'Player {}: {}'