from environments.env import Env
from games.cards.blackjack.game import BlackJackGame, Action
import numpy as np

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
        dealer_decode = self.player_decode('dealer')
        player_decode = self.player_decode('player')

        return dealer_decode - 1 + player_decode*(self.max_val + 1)

    def state_bounds(self):
        min = 0 # TODO: make this programatic
        max = (22 - 1 - 1) + (22 - 4)*(self.max_val + 1) # TODO: make this programatic

        return min, max

    def player_decode(self, player_type):
        sub = 1
        if player_type == 'player':
            mv = self.game.player.get_max_value()
            sub = 4
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
