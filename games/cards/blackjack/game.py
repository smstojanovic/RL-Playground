from enum import Enum
from games.cards.blackjack.player import BJPlayer
from games.cards.blackjack.dealer import BJDealer
from games.cards.blackjack.bj_cards import StandardBJDeck, CustomBJDeck, BJCard
import warnings

class Action(Enum):
    Hit = 'Hit'
    Stay = 'Stay'


class BlackJackGame:
    def __init__(self, num_decks = 6, verbose = False, cards_before_restart = 52):
        self._num_decks = num_decks
        self.deck = StandardBJDeck(num_decks)
        self.new_game(verbose, cards_before_restart)

    def new_game(self, verbose = False, cards_before_restart = 52):
        if cards_before_restart < 20:
            warnings.warn('Warning, number of cards before restart is low to keep playing')

        num_cards = self.num_cards_left()
        if num_cards < cards_before_restart:
            # reshuffle new deck
            self.deck = StandardBJDeck(self._num_decks)

        self.dealer = BJDealer(self.deck)
        self.player = BJPlayer(self.deck)

        # player gets 2 cards
        self.player.hit()
        self.player.hit()
        if verbose:
            self.render()

        self.stop = False

    def num_cards_left(self):
        return self.deck.len_cards()

    def set_deck(self, deck, verbose = False, cards_before_restart = 52):
        self.deck = deck
        self.new_game(verbose, cards_before_restart)

    def get_deck_hist_vec(self):
        """
            Gets a vector representation of the history of the deck in play for this game.
        """
        return self.deck.decode_card_history()

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
