from models import Blackjack
from matplotlib import pyplot as plt

n_episodes = 500000
game = Blackjack(n_episodes)
game.monte_carlo_exploring_starts(game.n_episodes)
# value_function = blackjack_monte_carlo_exploring_starts(n_episodes)
# print(game.q_values)
print(game.player_policy)

print(game.wincount)
plt.plot(game.wincount)
plt.show()
