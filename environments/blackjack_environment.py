from environments.env import Env
from games.cards.blackjack.game import BlackJackGame, Action
from enum import Enum
import numpy as np

class PlayerType(Enum):
    Player = 'Player'
    Dealer = 'Dealer'


class BlackJackEnv(Env):
    def __init__(self, num_decks = 6, cards_before_restart = 52):
        self.num_decks = num_decks
        self.cards_before_restart = cards_before_restart

        self.game = BlackJackGame(num_decks, False, cards_before_restart)
        self.action_space = [Action.Hit, Action.Stay]

        self.max_val = 23
        self.s = self.decode()

    def reset(self, reset_deck = True):
        if reset_deck:
            self.game = BlackJackGame(self.num_decks, False, self.cards_before_restart)
        else:
            self.game.new_game()

        state = self.decode()
        self.s = state
        return state

    def render(self):
        self.game.render()

    def decode(self):
        # TODO: add a state for cards in play
        return self.decode_game()

    def decode_game(self):
        dealer_decode = self.player_decode(PlayerType.Dealer)
        player_decode = self.player_decode(PlayerType.Player)

        return dealer_decode + player_decode*self.game.dealer.critical_value

    def encode(self, state_value):
        d = state_value % self.game.dealer.critical_value
        dealer_max = d + self.get_player_min_value(PlayerType.Dealer)

        p = int((state_value - d)/self.game.dealer.critical_value)
        player_max = p + self.get_player_min_value(PlayerType.Player)

        return {
            'player_max_value' : player_max,
            'dealer_max_value' : dealer_max
        }

    def state_bounds(self):
        min = 0
        max = (self.game.dealer.critical_value - self.get_player_min_value(PlayerType.Dealer)) +\
              (self.game.player.critical_value - self.get_player_min_value(PlayerType.Dealer))*(self.game.dealer.critical_value)

        return min, max

    def get_player_min_value(self, player_type):
        if player_type == PlayerType.Player:
            return 4
        return 2

    def player_decode(self, player_type):
        sub = self.get_player_min_value(PlayerType.Dealer)

        if player_type == PlayerType.Player:
            mv = self.game.player.get_max_value()
            sub = self.get_player_min_value(PlayerType.Player)
        else:
            mv = self.game.dealer.get_max_value()

        mv = self.max_val if mv > self.max_val else mv
        return mv - sub

    def sample_action(self):
        i = np.random.randint(0,len(self.action_space))
        return i, self.action_space[i]

    def step(self, action):
        done, reward = self.game.take_action(action)
        state = self.decode()
        info = {'prob' : None}

        self.s = state

        return state, reward, done, info
