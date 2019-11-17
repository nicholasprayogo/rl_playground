import numpy as np
import itertools
from random import randint

class Blackjack():
    def __init__(self):
        # player_sum = np.array(range(12,22))
        # dealer_card = np.array(range(1,12))
        # player_usable_ace = np.array([0,1])
        # # 0: usable ace 11 without bust
        #
        # # state based on current sum (12-21), dealers's one-showing card (1-10), and whether hold usable ace (0,1)
        # possible_states = list(itertools.product(player_sum,dealer_card,player_usable_ace))

        self.actions = [0,1] # 0: stick, 1: hit
        self.player_policy = np.ones(22, dtype = np.int)
        self.player_policy[20] = self.actions[0]
        self.player_policy[21] = self.actions[0]
        self.dealer_policy = np.ones(22, dtype=np.int)

        for i in range(17,22):
            self.dealer_policy[i] = 0

    def deal_cards(self):
        player_card1 = randint(1,10)
        player_card2 = randint(1,10)
        dealer_count1 = randint(1,10)
        dealer_count2 = randint(1,10)
        return ([player_card1, player_card2], [dealer_count1, dealer_count2])

    def update_usable_ace(self, cards, usable_ace):
        for card_index, card in enumerate(cards):
            if (card == 1) and (sum(cards)+11 - card)<=21:
                cards[card_index] = 11
                usable_ace += 1
        return cards, usable_ace

    def turn(self, bust, stick, policy, cards, agent =None, initial_state=None, dealer_card1 = None):
        usable_ace = 0
        player_trajectory = []

        while bust != True and stick != True:
            print(cards)
            cards, usable_ace = self.update_usable_ace(cards, usable_ace)
            count = sum(cards)
            if count > 21:
                bust = True
                break

            # execute policy
            action = policy[count]

            if agent == "player":
                player_trajectory.append({"state":(sum(cards), dealer_card1, usable_ace), "action":action})

            if action == 0:
                stick = True
            else:
                cards.append(randint(1,10))

        print("Card Count: {}, Bust: {}. Stick: {}, Usable Ace: {}".format(count,bust,stick,usable_ace))

        if agent == "player":
            return (count, bust, stick, usable_ace, player_trajectory)
        else:
            return (count, bust, stick, usable_ace)

    # generate an episode of blackjack
    def play(self, player_cards, dealer_cards):
        player_bust = False
        player_stick = False
        dealer_bust = False
        dealer_stick = False

        player_usable_ace = 0

        player_cards, player_usable_ace = self.update_usable_ace(player_cards, player_usable_ace)

        # player's turn
        print("Player's Turn: ")
        player_count, player_bust, player_stick, player_usable_ace, player_trajectory = self.turn(player_bust, player_stick, self.player_policy, player_cards, agent="player", dealer_card1 = dealer_cards[0])

        if player_bust:
            print("Player busted")
            return -1, player_trajectory

        # dealer's turn
        print("Dealer's Turn: ")
        dealer_count, dealer_bust, dealer_stick, dealer_usable_ace = self.turn(dealer_bust, dealer_stick, self.dealer_policy, dealer_cards)

        if dealer_bust or (player_count > dealer_count):
            print("Player wins")
            return 1, player_trajectory

        elif player_count == dealer_count:
            print("Draw")
            return 0, player_trajectory

        elif player_count < dealer_count:
            print("Dealer wins")
            return -1, player_trajectory
