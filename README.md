# Rl-Playground

This is my repo for playing around with either RL or creating games and creating RL-systems around them.

There are some folders are set up here:

- games (for custom game code)
- environments (for environments that provide MDP type framework around these games (states, actions and rewards))
- qlearning (for some preliminary q-learning scripts)

## Environment Setup

Just make sure that the PYTHONPATH env variable is appended to the root of this folder.

Then as per usual

```
  $ python -m venv .venv
  $ source .venv/bin/activate
  $ pip install -r requirements.txt
```
