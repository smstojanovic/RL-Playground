from environments.blackjack_environment import BlackJackEnv, PlayerType, BlackJackEnvCC
import sys
import numpy as np

bjenv = BlackJackEnvCC()
self = bjenv
bjenv.render()

num_decks = bjenv.num_decks

bjenv.s


def create_projection(low_value_limit = 6, med_value_limit = 9):
    """
        This helps define how 'warm' the deck is.
    """
    proj = np.zeros((1,10))

    for i in range(10):
        if i <= low_value_limit - 2:
            proj[0,i] = -1
        elif i > med_value_limit - 2:
            proj[0,i] = 1

    return proj

proj = create_projection()

def get_cc_component(state, proj):
    res = np.dot(
        state[1],
        proj.transpose()
    )
    return res[0,0]

get_cc_component(bjenv.s, proj)

cc_res = 150

q_tensor = np.zeros([len(bjenv.action_space), bjenv.state_bounds()[1], cc_res])

# if we have a q_table from regular blackjack, try to init the
# q_tensor with values from here.

try:
    # initialise the agent with knowledge on how to play regular blackjack.
    q_t = q_table.transpose()
except:
    # no prior knowledge, just play and learn as you go.
    q_t = None

for i in range(cc_res):
    q_tensor[:,:,i] = q_t


def decompose_state(state, proj, cc_res):
    s = state[0]
    c = int(get_cc_component(state, proj) + cc_res/2)
    return s,c

import random
from IPython.display import clear_output

# Hyperparameters
alpha = 0.07
gamma = 0.7
epsilon = 0.25

# For plotting metrics
all_epochs = []
all_penalties = []
i = 1

max_rounds = int(1e6 + 1)
hard_reset=True

for i in range(1, max_rounds):
    if i > 1:
        hard_reset = False

    state = bjenv.reset(hard_reset)
    s,c = decompose_state(state, proj, cc_res)

    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:
        if random.uniform(0, 1) < epsilon or min(q_tensor[:,s,c]) == max(q_tensor[:, s,c]):
            action_idx, action = bjenv.sample_action() # Explore action space
        else:
            action_idx = np.argmax(q_tensor[:,s,c]) # Exploit learned values
            action = bjenv.action_space[action_idx]

        next_state, reward, done, info = bjenv.step(action)
        ns, nc = decompose_state(next_state, proj, cc_res)

        #old_value = q_table[state, action_idx]
        old_value = q_tensor[action_idx,s,c]
        next_max = np.max(q_tensor[:,ns,nc])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_tensor[action_idx,s,c] = new_value

        if reward < 0:
            penalties += 1

        state = next_state
        s,c = ns, nc
        epochs += 1

    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")



def play_game():
    state = bjenv.reset()
    epochs, penalties, reward = 0, 0, 0

    done = False

    #bjenv.render()
    s,c = decompose_state(state, proj, cc_res)

    #c - (cc_res*0.5)

    while not done:
        #q_tensor[:,s,c]
        action_idx = np.argmax(q_tensor[:,s,c])
        action = bjenv.action_space[action_idx]
        action

        state, reward, done, info = bjenv.step(action)
        s,c = decompose_state(state, proj, cc_res)
        #bjenv.render()


    return reward



# evaluate performance
losses = 0
draws = 0
wins = 0
blackjacks = 0
cummulative_reward = 0

num_games = int(1e4)

bjenv.reset(True)
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





# evaluate performance if we choose to play with a biased deck.


def play_game_biased(deck_idx_min = 15, deck_idx_max = 15):
    """
        Allow the ability to choose when to play based on the
        heat of the deck
    """
    state = bjenv.reset()
    s,c = decompose_state(state, proj, cc_res)
    epochs, penalties, reward = 0, 0, 0

    done = False

    #bjenv.render()
    c_value = c - (cc_res*0.5)
    if not (deck_idx_min <= c_value <= deck_idx_max):
        played = False
        return 0, played

    played = True

    #c - (cc_res*0.5)

    while not done:
        #q_tensor[:,s,c]
        action_idx = np.argmax(q_tensor[:,s,c])
        action = bjenv.action_space[action_idx]
        action

        state, reward, done, info = bjenv.step(action)
        s,c = decompose_state(state, proj, cc_res)
        #bjenv.render()


    return reward, played


losses = 0
draws = 0
wins = 0
blackjacks = 0
cummulative_reward = 0

num_games = int(1e6)
num_games_played = 0

for i in range(num_games):
    reward, played = play_game_biased(15,100)
    if played:
        cummulative_reward += reward
        num_games_played += 1

        if reward < 0:
            losses += 1

        if reward == 0:
            draws += 1

        if reward > 0:
            wins += 1

        if reward > 1:
            blackjacks += 1

num_games_played
cummulative_reward/num_games_played

losses/num_games_played
draws/num_games_played
wins/num_games_played
blackjacks/num_games_played
