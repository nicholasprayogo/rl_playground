from models import Blackjack

n_episodes = 500000
game = Blackjack(n_episodes)
game.monte_carlo_exploring_starts(game.n_episodes)
# value_function = blackjack_monte_carlo_exploring_starts(n_episodes)
print(game.q_values)
