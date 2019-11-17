import numpy as np
import itertools
from random import randint
from models import Blackjack

def blackjack_monte_carlo_exploring_starts(n_episodes):
    rewards = []

    state_action_values = np.zeros((10, 10, 2, 2))
    state_action_pair_count = np.ones((10, 10, 2, 2))

    for i in range(n_episodes):
        print("Episode: {}".format(i))

        game = Blackjack()

        # random state initialization
        player_cards, dealer_cards = game.deal_cards()
        reward, player_trajectory = game.play(player_cards, dealer_cards)

        # rewards.append([player_trajectory, reward])
        for state_action_pair in player_trajectory:
            state = state_action_pair["state"]
            action = state_action_pair["action"]
            # player always have sum between 12 to 21

            player_count, dealer_card1, usable_ace = state[0], state[1], state[2]

            state_action_values[player_count-12, dealer_card1-1, usable_ace, action] += reward
            state_action_pair_count[player_count-12, dealer_card1-1, usable_ace, action] +=1

    return state_action_values/state_action_pair_count

n_episodes = 500000
value_function = blackjack_monte_carlo_exploring_starts(n_episodes)
print(value_function)
