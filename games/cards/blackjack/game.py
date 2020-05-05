from enum import Enum
from games.cards.blackjack.player import BJPlayer
from games.cards.blackjack.dealer import BJDealer
from games.cards.blackjack.bj_cards import StandardBJDeck, CustomBJDeck, BJCard

class Action(Enum):
    Hit = 'Hit'
    Stay = 'Stay'


class BlackJackGame:
    def __init__(self, num_decks = 6, verbose = False):
        self.deck = StandardBJDeck(num_decks)
        self._init_game(verbose)

    def _init_game(self, verbose = False):
        self.dealer = BJDealer(self.deck)
        self.player = BJPlayer(self.deck)

        # player gets 2 cards
        self.player.hit()
        self.player.hit()
        if verbose:
            self.render()

        self.stop = False

    def set_deck(self, deck, verbose = False):
        self.deck = deck
        self._init_game(verbose)

    def get_player(self):
        return self.player

    def return_reward(self, reward, verbose):
        if verbose:
            print('Reward: {reward}'.format(reward = str(reward)))

        return self.stop, reward

    def take_action(self, action, verbose = False):
        if action not in Action:
            raise EnvironmentError('Action {action} doesnt exist.'.format(action=action))

        if self.stop:
            raise EnvironmentError('Game has already stopped')

        reward = 0

        if action == Action.Hit:
            self.player.hit()

        if self.player.is_bust():
            self.stop = True
            reward = -1
            return self.return_reward(reward, verbose)

        if self.player.get_max_value() == 21:
            self.stop = True
            reward = 1.5
            return self.return_reward(reward, verbose)

        if action == Action.Stay:
            self.stop = True
            self.dealer.play()

            if self.dealer.is_bust():
                reward = 1
                return self.return_reward(reward, verbose)

            if self.dealer.is_push():
                reward = 0
                return self.return_reward(reward, verbose)

            if self.dealer.get_max_value() > self.player.get_max_value():
                reward = -1
            elif self.dealer.get_max_value() < self.player.get_max_value():
                reward = 1

        return self.return_reward(reward, verbose)

    def render(self):
        print('Dealers card:')
        self.dealer.render()

        print('\nPlayers cards:')
        self.player.render()

#
# # dealer push test 2
# bjgame = BlackJackGame(verbose = False)
#
# cards = [
#     BJCard('King','Spade'),
#     BJCard('King','Heart'),
#     BJCard('Queen','Heart'),
#     BJCard('6','Heart'),
#     BJCard('6','Spade')
# ]
#
# cards.reverse()
# cdeck = CustomBJDeck(cards, False)
# bjgame.set_deck(cdeck, True)
#
# done, reward = bjgame.take_action(Action.Stay)
#
# bjgame.dealer.get_max_value()
# #bjgame.dealer.render()
#
# assert done
# assert reward == 0
# assert bjgame.dealer.get_max_value() == 22
#
#
#
# # dealer push test 2
# bjgame = BlackJackGame(verbose = False)
#
# cards = [
#     BJCard('Ace','Spade'),
#     BJCard('King','Spade'),
#     BJCard('King','Heart'),
#     BJCard('6','Heart'),
#     BJCard('5','Spade'),
#     BJCard('5','Diamond')
# ]
#
# cards.reverse()
# cdeck = CustomBJDeck(cards, False)
# bjgame.set_deck(cdeck, True)
#
# done, reward = bjgame.take_action(Action.Stay)
#
# bjgame.dealer.get_max_value()
# #bjgame.dealer.render()
#
# assert done
# assert reward == 1
# assert bjgame.dealer.get_max_value() == 17
#
#
# # dealer bust test
# bjgame = BlackJackGame(verbose = False)
#
# cards = [
#     BJCard('King','Spade'),
#     BJCard('King','Heart'),
#     BJCard('Queen','Heart'),
#     BJCard('6','Heart'),
#     BJCard('7','Spade')
# ]
#
# cards.reverse()
# cdeck = CustomBJDeck(cards, False)
# bjgame.set_deck(cdeck, True)
#
# done, reward = bjgame.take_action(Action.Stay)
#
# bjgame.dealer.get_max_value()
# #bjgame.dealer.render()
#
# assert done
# assert reward == 1
# assert bjgame.dealer.get_max_value() == 23
#
#
#
#
#
# bjgame.get_player().get_values()
# bjgame.player.get_max_value()
# bjgame.take_action(Action.Hit, True)
#
# bjgame.take_action(Action.Stay)
#
# bjgame.dealer.is_bust()
#
# bjgame.dealer.get_max_value()
# bjgame.dealer.render()




# len(bjgame.deck._cards)
