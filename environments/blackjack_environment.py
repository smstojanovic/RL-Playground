from environments.env import Env
from games.cards.blackjack.game import BlackJackGame, Action
from enum import Enum
import numpy as np

class PlayerType(Enum):
    Player = 'Player'
    Dealer = 'Dealer'


class BlackJackEnv(Env):
    def __init__(self, num_decks = 6):
        self.num_decks = num_decks
        self.game = BlackJackGame(num_decks)
        self.action_space = [Action.Hit, Action.Stay]

        self.max_val = 22
        self.s = self.decode()

    def reset(self):
        self.game = BlackJackGame(self.num_decks)
        state = self.decode()
        self.s = state
        return state

    def render(self):
        self.game.render()

    def decode(self):
        dealer_decode = self.player_decode(PlayerType.Player)
        player_decode = self.player_decode(PlayerType.Dealer)

        return dealer_decode + player_decode*self.dealer.critical_value

    def state_bounds(self):
        min = 0 # TODO: make this programatic
        max = (self.dealer.critical_value - 2) + (self.player.critical_value - 4)*(self.dealer.critical_value) # TODO: make this programatic

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
