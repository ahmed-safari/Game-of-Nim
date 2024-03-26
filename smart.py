import math
import random
import time
from tqdm import tqdm


class Player:

    def __init__(self, name, is_ai=False):
        self.name = name


class NimAI:

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        return self.q[(tuple(state), action)] if (tuple(state), action) in self.q else 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        self.q[(tuple(state), action)] = old_q + self.alpha * (
            future_rewards + reward - old_q
        )

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        best_reward = 0
        actions = list(Nim.get_allowed_moves(state))
        for action in actions:
            best_reward = max(self.get_q_value(state, action), best_reward)
        return best_reward

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        best_action = None
        best_reward = 0
        actions = list(Nim.get_allowed_moves(state))
        for action in actions:
            q_val = self.get_q_value(state, action)
            if best_action is None or q_val > best_reward:
                best_reward = q_val
                best_action = action

        if epsilon:
            total_actions = len(actions)
            weights = [
                (1 - self.epsilon) if action == best_action else self.epsilon
                for action in actions
            ]
            print(weights)
            best_action = random.choices(actions, weights=weights, k=1)[0]

        return best_action


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    agent = NimAI()

    # Play n games

    for i in tqdm(range(n)):
        # print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}}
        player = 0
        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = agent.choose_action(game.piles)

            # Keep track of last state and action
            last[player]["state"] = state
            last[player]["action"] = action

            # Make move
            game.move(action)
            player = 0 if player == 1 else 1
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.game_over:
                agent.update(state, action, new_state, -1)
                agent.update(
                    last[player]["state"],
                    last[player]["action"],
                    new_state,
                    1,
                )
                break

            # If game is continuing, no rewards yet
            elif last[player]["state"] is not None:
                agent.update(
                    last[player]["state"],
                    last[player]["action"],
                    new_state,
                    0,
                )

    print("Done training")

    # Return the trained AI
    return agent


# train(10000)


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()
    player = 0

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.get_allowed_moves(game.piles)
        # time.sleep(1)

        # Let human make a move
        if player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))
        player = 0 if player == 1 else 1

        # Check for winner
        if game.game_over:
            print()
            print("GAME OVER")
            winner = "Human" if player == human_player else "AI"
            print(f"Winner is {winner}")
            return


play(train(10000))
