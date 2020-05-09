import pytest
import numpy as np
from games.cards.blackjack.bj_cards import BJCard, CustomBJDeck, StandardBJDeck

def test_vector_history():
    """
    testing that drawing and card history work for the custom deck.
    """
    cards = [
        BJCard('6','Diamond'),
        BJCard('2','Heart'),
        BJCard('Queen','Spade'),
        BJCard('5','Heart'),
        BJCard('8','Spade')
    ]

    cards.reverse()
    cdeck = CustomBJDeck(cards, False)
    cdeck.draw()
    cdeck.draw()

    hist_vec = cdeck.decode_card_history()

    has_two = hist_vec[0,0] == 1
    has_six = hist_vec[0,4] == 1
    no_ten_before = hist_vec[0,8] == 0
    only_two_cards = np.sum(hist_vec, axis=1)[0] == 2.0

    cdeck.draw()
    hist_vec = cdeck.decode_card_history()
    has_ten = hist_vec[0,8] == 1

    assert has_two and has_six and no_ten_before and only_two_cards and has_ten
