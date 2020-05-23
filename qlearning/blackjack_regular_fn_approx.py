
from environments.blackjack_environment import BlackJackEnv, PlayerType, BlackJackEnvCC
import numpy as np

bjenv = BlackJackEnv()
self = bjenv
bjenv.render()

def get_state_vec(bjenv):
    player = bjenv.player_decode_vec(PlayerType.Player)
    dealer = bjenv.player_decode_vec(PlayerType.Dealer)

    return np.concatenate([player,dealer])




get_state_vec(bjenv)





bjenv.s

bjenv.encode(bjenv.s)

print("Action Space {}".format(bjenv.action_space))


bjenv.reset()
epochs = 0
penalties, reward = 0, 0

frames = [] # for animation

done = False

while not done:
    action_idx, action = bjenv.sample_action()
    state, reward, done, info = bjenv.step(action)

    if reward < 0:
        penalties += 1

    # frames.append({
    #     'frame': bjenv.render(mode='ansi'),
    #     'state': state,
    #     'action': action,
    #     'reward': reward
    #     }
    # )

    epochs += 1

print("Timesteps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))
reward


import numpy as np

# set up the q function as a linear function.
q_weights = np.zeros([len(get_state_vec(bjenv)), len(bjenv.action_space) ])
def q_value(state, action_idx, q_weights):
    return np.dot(state.transpose(),q_weights[:,action_idx])[0]

def nabla_q(state, action_idx):
    grad = np.concatenate([state.transpose(),state.transpose()]).transpose()
    for idx in range(len(bjenv.action_space)):
        if idx != action_idx:
            grad[:,idx] = 0

    return grad

#%%time
"""Training the agent"""

import random
from IPython.display import clear_output

# Hyperparameters
alpha = 0.05
gamma = 0.99
epsilon = 0.25

# blackjack can be thought of as an episodic MDP so we might be able to set gamma to 1.
# however, these episodes are so small and we generally only care about the relativity between
# q-values at each state and rewards are 0 except for at the end of an episode that this shouldn't affect the result.

# For plotting metrics
all_epochs = []
all_penalties = []
i = 1
for i in range(1, 100001):
    bjenv.reset()
    state = get_state_vec(bjenv)

    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:
        q_values = [q_value(state, idx, q_weights) for idx in range(len(bjenv.action_space))]
        if random.uniform(0, 1) < epsilon or min(q_values) == max(q_values):
            action_idx, action = bjenv.sample_action() # Explore action space
        else:
            action_idx = np.argmax(q_values) # Exploit learned values
            action = bjenv.action_space[action_idx]

        _, reward, done, info = bjenv.step(action)
        next_state = get_state_vec(bjenv)

        old_value = q_value(state, action_idx, q_weights)#q_table[state, action_idx]
        next_max = np.max([q_value(next_state, idx, q_weights) for idx in range(len(bjenv.action_space))])

        new_values = q_weights + alpha * (reward + gamma * next_max - q_values[action_idx] ) * nabla_q(state, action_idx)
        q_weights = new_values

        if reward < 0:
            penalties += 1

        state = next_state
        epochs += 1

    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")


100 % 3

bjenv.s % bjenv.game.dealer.critical_value

bjenv.player_decode(PlayerType.Dealer)
bjenv.player_decode(PlayerType.Player)


bjenv.game.dealer.render()
bjenv.game.player.render()

bjenv.decode()
bjenv.render()

def play_game():
    bjenv.reset()
    state = get_state_vec(bjenv)

    epochs, penalties, reward = 0, 0, 0

    done = False

    #bjenv.render()

    while not done:
        q_values = [q_value(state, idx, q_weights) for idx in range(len(bjenv.action_space))]
        action_idx = np.argmax(q_values)
        action = bjenv.action_space[action_idx]
        action

        _, reward, done, info = bjenv.step(action)
        state = get_state_vec(bjenv)
        #bjenv.render()


    return reward

# evaluate performance
losses = 0
draws = 0
wins = 0
blackjacks = 0
cummulative_reward = 0

num_games = 10000

for i in range(num_games):
    reward = play_game()
    cummulative_reward += reward

    if reward < 0:
        losses += 1

    if reward == 0:
        draws += 1

    if reward > 0:
        wins += 1

    if reward > 1:
        blackjacks += 1


cummulative_reward/num_games

losses/num_games
draws/num_games
wins/num_games
blackjacks/num_games
