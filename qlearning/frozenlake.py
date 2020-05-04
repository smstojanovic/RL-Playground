import gym

env = gym.make("FrozenLake8x8-v0").env

env.reset()
env.render()

print("Action Space {}".format(env.action_space))
print("State Space {}".format(env.observation_space))

env.reset()
env.render()


import numpy as np
q_table = np.zeros([env.observation_space.n, env.action_space.n])
q_table.shape

import random
from IPython.display import clear_output

# lets try train it.
# Hyperparameters
alpha = 0.8
gamma = 0.7
epsilon = 0.25

# For plotting metrics
all_epochs = []
all_penalties = []
i = 1

rewards = []

for i in range(1, 100001):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:

        max_action = np.argmax(q_table[state])
        min_action = np.argmin(q_table[state])

        if random.uniform(0, 1) < epsilon or max_action == min_action:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, info = env.step(action)

        if reward <= 0 and done:
            reward = -0.1

        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward != 0:
            rewards.append(reward)

        state = next_state
        epochs += 1

    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")



q_table

def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)



from IPython.display import clear_output
from time import sleep


def play_game():
    frames = []

    state = env.reset()
    epochs, penalties, reward = 0, 0, 0

    done = False

    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)

        frames.append({
            'frame': env.render(mode='ansi'),
            'state': state,
            'action': action,
            'reward': reward
            }
        )

        if reward == -10:
            penalties += 1

        epochs += 1

    print_frames(frames)


play_game()
