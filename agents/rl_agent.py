import random
from tqdm import tqdm
from utils import get_allowed_moves
from nim_game import NimGame


class RLAgent:
    """
    This agent uses Q-learning to learn the optimal policy for the Nim game.

    Attributes:
        q (dict): A dictionary that maps state-action pairs to Q-values. States are represented as tuples, and actions are specified as required by the environment.
        alpha (float): The learning rate, determining to what extent the newly acquired information will override the old information. Values range from 0 to 1.
        epsilon (float): The exploration rate, determining the probability of choosing a random action instead of the best-known action. Values range from 0 to 1, where higher values encourage more exploration.

    Parameters:
        alpha (float): The learning rate (default 0.5).
        epsilon (float): The exploration rate (default 0.1).
    """

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initializes the RLAgent with specified learning and exploration rates.

        Parameters:
            alpha (float): The learning rate.
            epsilon (float): The exploration rate.
        """

        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Updates the Q-value for a given state-action pair based on the observed transition and reward.

        This method applies the Q-learning update rule to adjust the Q-values towards better estimates of the expected utility of state-action pairs. The update is influenced by the immediate reward received, the estimated value of the subsequent state, and the learning rate.

        Args:
            old_state (tuple): The state from which the action was taken.
            action (tuple): The action taken in the `old_state`. (pile, count)
            new_state (tuple): The state that resulted from taking `action` in `old_state`.
            reward (float): The immediate reward received from the environment after moving to the `new_state`.

        Returns:
            None
        """

        old = self.get_q_value(old_state, action)  # Old Q-value

        best_future = self.best_future_reward(
            new_state
        )  # Estimated best future Q-value

        self.update_q_value(
            old_state, action, old, reward, best_future
        )  # Update Q-value

    def get_q_value(self, state, action):
        """
        This method returns the estimated utility (Q-value) of taking a given action in a given state, according to the agent's current knowledge.
        If the agent has not yet encountered a particular state-action pair, this method returns 0, indicating an uninitialized Q-value.

        Parameters:
            state (tuple): The state for which the Q-value is queried. (pile1, pile2, ..., pileN)
            action (tuple): The action for which the Q-value is queried. (pile, count)

        Returns:
            float: The Q-value for the state-action pair. (zero if not found)
        """
        if (tuple(state), action) in self.q:
            return self.q[(tuple(state), action)]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Updates the Q-value for a given state-action pair based on the observed transition and reward.

        This method applies the Q-learning update rule to adjust the Q-values towards better estimates of the expected utility of state-action pairs.
        The update is influenced by the immediate reward received, the estimated value of the subsequent state, and the learning rate.
        The formula for the update is: Q(s, a) <- Q(s, a) + α * (reward + γ * max_a Q(s', a) - Q(s, a))
        Which is equivilant tooo: Q(s, a) = old_q + alpha * (reward + future_rewards - old_q)

        Parameters:
            state (tuple): The state from which the action was taken.
            action (tuple): The action taken in the `old_state`. (pile, count)
            old_q (float): The previous Q-value for the state-action pair.
            reward (float): The immediate reward received from the environment after moving to the `new_state`.
            future_rewards (float): The estimated best future reward from the resulting state.

        Returns:
            None (updates the Q-value in the agent's Q-table)
        """

        # Calculate the new Q-value based on the Q-learning update rule
        q_value = old_q + self.alpha * (future_rewards + reward - old_q)

        # Update the Q-value in the Q-table
        self.q[(tuple(state), action)] = q_value

    def best_future_reward(self, state):
        """
        Given a state, consider all possible actions (available moves)
        available in that state and return the maximum of all of their Q-values.

        If a state has no available actions, the method should return 0.

        Parameters:
            state (tuple): The state for which the best future reward is queried. (pile1, pile2, ..., pileN)

        Returns:
            best_reward (float): The highest Q-value among all available actions in the state.
        """
        best_reward = 0
        actions = list(get_allowed_moves(state))
        for action in actions:
            best_reward = max(self.get_q_value(state, action), best_reward)
        return best_reward

    def choose_action(self, state, epsilon=True):
        """
        Given a state, choose the best action available in that state based on the current Q-values.
        If multiple actions have the same Q-value, any of those options is acceptable.
        When the `epsilon` parameter is set to `True`, the agent should take a random action with probability `epsilon` instead of taking the best policy action.

        Parameters:
            state (tuple): The current state of the environment. (pile1, pile2, ..., pileN)
            epsilon (bool): Whether to use the agent's exploration parameter.

        Returns:
            best_action (tuple): The optimal action to take in the input state. (pile, count)
        """

        best_action = None  # The best action to take
        best_reward = 0  # The reward of the best action
        actions = list(get_allowed_moves(state))  # Get all possible actions
        for action in actions:  # Loop through all possible actions
            q_val = self.get_q_value(state, action)  # Get the Q-value of the action
            if (
                best_action is None or q_val > best_reward
            ):  # If the Q-value is better than the best reward
                best_reward = q_val  # Update the best reward
                best_action = action  # Update the best action

        if epsilon:  # If epsilon is enabled (exploration)
            weights = []
            for action in actions:  # Loop through all possible actions
                if action == best_action:  # If the action is the best action
                    weights.append(
                        1 - self.epsilon
                    )  # Add the weight of the action (1 - epsilon) using this formula will make the best action more likely to be chosen
                else:  # If the action is not the best action
                    weights.append(
                        self.epsilon
                    )  # Add the weight of the action (epsilon)
            # print(weights)
            best_action = random.choices(actions, weights=weights)[
                0
            ]  # Choose an action based on the weights

        return best_action

    def train(self, n, game=NimGame):

        # agent = self

        # Play n games
        # print(f"Training on {n} games")

        for i in tqdm(range(n), desc="Training RL Agent"):
            # print(f"Playing training game {i + 1}")
            # game = NimGame()
            game.reset()

            # Keep track of last move made by either player
            last = {
                0: {"state": None, "action": None},
                1: {"state": None, "action": None},
            }
            player = 0
            # Game loop
            while True:

                # Keep track of current state and action
                state = game.piles.copy()
                action = self.choose_action(game.piles)

                # Keep track of last state and action
                last[player]["state"] = state
                last[player]["action"] = action

                # Make move
                game.move(action)
                player = 0 if player == 1 else 1
                new_state = game.piles.copy()

                # When game is over, update Q values with rewards
                if game.game_over:
                    self.update(state, action, new_state, 1)
                    self.update(
                        last[player]["state"],
                        last[player]["action"],
                        new_state,
                        -1,
                    )
                    break

                # If game is continuing, no rewards yet
                elif last[player]["state"] is not None:
                    self.update(
                        last[player]["state"],
                        last[player]["action"],
                        new_state,
                        0,
                    )
