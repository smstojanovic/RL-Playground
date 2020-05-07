import pytest
from games.cards.blackjack.game import BlackJackGame, Action
from games.cards.blackjack.bj_cards import BJCard, CustomBJDeck, StandardBJDeck

def test_dealer_push():
    # dealer push test 2
    bjgame = BlackJackGame(verbose = False)

    cards = [
        BJCard('King','Spade'),
        BJCard('King','Heart'),
        BJCard('Queen','Heart'),
        BJCard('6','Heart'),
        BJCard('6','Spade')
    ]

    cards.reverse()
    cdeck = CustomBJDeck(cards, False)
    bjgame.set_deck(cdeck, False, cards_before_restart = 0)

    done, reward = bjgame.take_action(Action.Stay)

    bjgame.dealer.get_max_value()
    #bjgame.dealer.render()

    assert done and reward == 0 and bjgame.dealer.get_max_value() == 22

def test_dealer_continue():
    bjgame = BlackJackGame(verbose = False)

    cards = [
        BJCard('Ace','Spade'),
        BJCard('King','Spade'),
        BJCard('King','Heart'),
        BJCard('6','Heart'),
        BJCard('5','Spade'),
        BJCard('5','Diamond')
    ]

    cards.reverse()
    cdeck = CustomBJDeck(cards, False)
    bjgame.set_deck(cdeck, False, cards_before_restart = 0)

    done, reward = bjgame.take_action(Action.Stay)

    bjgame.dealer.get_max_value()
    #bjgame.dealer.render()

    assert done and reward == 1 and bjgame.dealer.get_max_value() == 17

def test_dealer_bust():
    # dealer bust test
    bjgame = BlackJackGame(verbose = False)

    cards = [
        BJCard('King','Spade'),
        BJCard('King','Heart'),
        BJCard('Queen','Heart'),
        BJCard('6','Heart'),
        BJCard('7','Spade')
    ]

    cards.reverse()
    cdeck = CustomBJDeck(cards, False)
    bjgame.set_deck(cdeck, False, cards_before_restart = 0)

    done, reward = bjgame.take_action(Action.Stay)

    bjgame.dealer.get_max_value()
    #bjgame.dealer.render()

    assert done and reward == 1 and bjgame.dealer.get_max_value() == 23
