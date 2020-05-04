from itertools import product

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

class StandardBJDeck(Deck):
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


# deck = StandardBJDeck(num_decks = 5)
# card = deck.draw()
#
# card.render()

# t1 = [1,2]
# t2 = ['a','b','c']
#
# list(product(t1,t2))

# card = BJCard('Ace','Spade')
# card.get_value()
#
# card.render()
