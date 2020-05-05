import numpy as np

class Env:
    def __init__(self):
        self.action_space = [] # this should be a list of enums

    def reset(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()

    def sample_action(self):
        num_actions = len(self.action_space)
        if num_actions == 0:
            raise EnvironmentError('No actions in this environment')

        i = np.random.randint(0,len(self.action_space))
        return i, self.action_space[i]

    def step(self, action):
        raise NotImplementedError()
