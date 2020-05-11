
from environments.blackjack_environment import BlackJackEnv, PlayerType, BlackJackEnvCC

bjenv = BlackJackEnv()
self = bjenv
bjenv.render()

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


q_table = np.zeros([bjenv.state_bounds()[1], len(bjenv.action_space) ])

q_table.shape


bjenv.encode(9)


#%%time
"""Training the agent"""

import random
from IPython.display import clear_output

# Hyperparameters
alpha = 0.1
gamma = 0.7
epsilon = 0.25

# blackjack can be thought of as an episodic MDP so we might be able to set gamma to 1.
# however, these episodes are so small and we generally only care about the relativity between
# q-values at each state and rewards are 0 except for at the end of an episode that this shouldn't affect the result.

# For plotting metrics
all_epochs = []
all_penalties = []
i = 1
for i in range(1, 100001):
    state = bjenv.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:
        if random.uniform(0, 1) < epsilon or min(q_table[state,:]) == max(q_table[state, :]):
            action_idx, action = bjenv.sample_action() # Explore action space
        else:
            action_idx = np.argmax(q_table[state]) # Exploit learned values
            action = bjenv.action_space[action_idx]

        next_state, reward, done, info = bjenv.step(action)

        old_value = q_table[state, action_idx]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action_idx] = new_value

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


def play_game():
    state = bjenv.reset()
    epochs, penalties, reward = 0, 0, 0

    done = False

    #bjenv.render()

    while not done:
        action_idx = np.argmax(q_table[state])
        action = bjenv.action_space[action_idx]
        action

        state, reward, done, info = bjenv.step(action)
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
