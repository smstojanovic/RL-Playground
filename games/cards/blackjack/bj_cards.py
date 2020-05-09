from itertools import product
import numpy as np

_card_values = {
    '2' : {'values' : [2]},
    '3' : {'values' : [3]},
    '4' : {'values' : [4]},
    '5' : {'values' : [5]},
    '6' : {'values' : [6]},
    '7' : {'values' : [7]},
    '8' : {'values' : [8]},
    '9' : {'values' : [9]},
    '10' : {'values' : [10]},
    'Jack' : {'values' : [10]},
    'Queen' : {'values' : [10]},
    'King' : {'values' : [10]},
    'Ace' : {'values' : [1,11]}
}

from games.cards.cards import Card, Deck, _suits, _classes

class BJCard(Card):
    def __init__(self, class_, suit):
        super().__init__(class_, suit)

        self.values = _card_values[self._class]['values']

    def get_num_values(self):
        return len(self.values)

    def get_value(self, index = 0):

        if self.get_num_values() == 1:
            return self.values[0]

        if index > 1 or index < 0:
            raise EnvironmentError('index out of bounds, must be 0 or 1')

        return self.values[index]

class BJDeck(Deck):
    """
        Different BJ Decks can inherit methods from here.
        BJ Decks all use BJ Cards (which have a value assigned to them.)
    """
    def __init__(self, cards):
        super().__init__(cards)

        min_card_val = min([max(v['values']) for k,v in _card_values.items()])
        max_card_val = max([max(v['values']) for k,v in _card_values.items()])

        vec_len = (max_card_val - min_card_val) + 1
        self.card_hist_vec = np.zeros([1,vec_len])
        self._history_index = 0

    def decode_card_history(self):
        """
            This method gets a (relatively fast) vector representation of which cards have been
            drawn (by card value) by remembering which cards in the history have already been counted.
        """
        latest_history = self.get_card_history()[self._history_index:]

        for card in latest_history:
            self._history_index += 1
            card_val = max(card.values)
            self.card_hist_vec[0,card_val-2] += 1

        return self.card_hist_vec



class StandardBJDeck(BJDeck):
    def __init__(self, num_decks = 6, split = None):
        all_cards = []

        for i in range(num_decks):
            cards = [BJCard(cls, suit) for cls, suit in product(_classes, _suits)]
            all_cards += cards

        super().__init__(all_cards)
        self.shuffle()

        if split is not None:
            if split <= 0 or split >= 1:
                raise EnvironmentError("Split needs to be None or a number between 0 and 1")

            num_cards = len(self._cards)
            split_idx = int(split*num_cards)
            self._cards = self._cards[:split_idx]


class CustomBJDeck(BJDeck):
    def __init__(self, cards, shuffle = False):
        super().__init__(cards)

        if shuffle:
            self.shuffle()


# deck = StandardBJDeck(num_decks = 5)
# card = deck.draw()
# self = deck
# card.render()

# t1 = [1,2]
# t2 = ['a','b','c']
#
# list(product(t1,t2))

# card = BJCard('Ace','Spade')
# card.get_value()
#
# card.render()
