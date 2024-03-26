import random
from tqdm import tqdm
from nim_game import NimGame  # Assuming the existence of a NimGame class
from agents import RLAgent
from agents import RandomAgent


def evaluate_agents(n_games=1000):
    """
    Evaluate the performance of RLAgent against RandomAgent in the Nim game.

    Parameters:
    - n_games (int): Number of games to play for the evaluation.

    Returns:
    - None: Prints out the statistical performance of each agent.
    """

    # Initialize agents
    rl_agent = RLAgent()
    random_agent = RandomAgent()
    rl_agent_wins = 0
    random_agent_wins = 0

    game = NimGame()

    rl_agent.train(10000, game)

    for _ in tqdm(range(n_games), desc="Evaluating Agents (1v1)"):

        game.reset()
        current_player = 0  # 0 for RLAgent, 1 for RandomAgent

        while not game.game_over:
            # print(game.piles)
            if current_player == 0:
                # print("RLAgent's Turn")
                action = rl_agent.choose_action(game.piles)
            else:
                # print("RandomAgent's Turn")
                action = random_agent.choose_action(game.piles)

            # print(action)

            game.move(action)
            current_player = 1 - current_player

        # Determine winner
        if current_player == 1:  # Last move was made by RLAgent so RandomAgent won
            # print("RandomAgent wins")
            random_agent_wins += 1
        else:  # Last move was made by RandomAgent so RLAgent won
            # print("RLAgent wins")
            rl_agent_wins += 1

        # Swap starting player for fairness
        current_player = 1 - current_player

    # Analysis
    total_games = rl_agent_wins + random_agent_wins
    print(f"Total games: {total_games}")
    print(f"RLAgent wins: {rl_agent_wins} ({(rl_agent_wins / total_games) * 100:.2f}%)")
    print(
        f"RandomAgent wins: {random_agent_wins} ({(random_agent_wins / total_games) * 100:.2f}%)"
    )


# Example usage
evaluate_agents(n_games=1000)
