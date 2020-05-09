import numpy as np

_suits = [
    'Heart',
    'Club',
    'Spade',
    'Diamond'
]

_classes = [
    '2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace'
]

class Card:
    def __init__(self, class_, suit):
        if suit not in _suits:
            raise EnvironmentError('Bad Suit')

        if class_ not in _classes:
            raise EnvironmentError('Bad Class')

        self._class = class_
        self._suit = suit

    def render(self):
        print("({_class},{suit})".format(
            _class = self._class,
            suit = self._suit
        ))

class Deck:
    def __init__(self, cards):
        self._cards = cards
        self._card_history = []

    def shuffle(self):
        np.random.shuffle(self._cards)

    def draw(self, discard = True):
        card = self._cards.pop()
        if not discard:
            self._cards = [card] + self._cards

        self._card_history.append(card)

        return card

    def len_cards(self):
        return len(self._cards)

    def get_card_history(self):
        return self._card_history



# card = Card('5','Spade')
# card.render()
