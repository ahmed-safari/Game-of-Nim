import random
from nim_game import NimGame


class RandomAgent:
    """
    This class represents a random agent that plays the game by choosing a random action from the available actions in the current state.
    It is used to compare the performance of the RLAgent against a simple baseline.
    """

    def choose_action(self, state):
        """
        Given a state, choose a random action from the available ations in that state.
        """

        actions = list(NimGame.get_allowed_moves(state))  # Get all possible actions

        return random.choice(actions)  # Choose a random action
