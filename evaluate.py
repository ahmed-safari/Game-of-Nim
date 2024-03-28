import random
from tqdm import tqdm
from nim_game import NimGame
from agents import RLAgent, RandomAgent, NimSumAgent
import time


def evaluate_agents(agent_dict, n_games=1000, game=NimGame):
    """
    Evaluate the performance of each agent against every other agent in the Nim game.

    Parameters:
    - agent_dict (dict): A dictionary where keys are agent names and values are agent instances.
    - n_games (int): Number of games to play for each evaluation.

    Returns:
    - None: Prints out the statistical performance of each agent.
    """

    results = {}
    for name in agent_dict:
        results[name] = {}
        for opponent_name in agent_dict:
            if opponent_name != name:
                results[name][opponent_name] = 0

    for agent_name, agent in agent_dict.items():
        for opponent_name, opponent in agent_dict.items():
            if agent_name == opponent_name:
                continue  # Skip evaluating against itself

            agent_wins = 0

            for _ in tqdm(
                range(n_games), desc=f"Evaluating {agent_name} vs {opponent_name}"
            ):

                game.reset()
                current_player = 0  # 0 for first agent, 1 for opponent

                while not game.game_over:
                    if current_player == 0:
                        action = agent.choose_action(game.piles)
                    else:
                        action = opponent.choose_action(game.piles)

                    game.move(action)
                    current_player = 1 - current_player

                # Determine winner (if current_player is 1, the agent won, else the opponent won)
                if current_player == 1:
                    agent_wins += 1

                # Swap starting player for fairness in the next game
                current_player = 1 - current_player

            # Record results
            results[agent_name][opponent_name] = agent_wins

    # Print results
    print(f"\nEvaluation results after {n_games} games for configuration:")
    print(f"    - Piles: {game.piles_count}")
    print(f"    - Max pile size: {game.max_pile_size}")
    print()
    for agent_name, opponents in results.items():
        print(f"\nResults for {agent_name}:")
        for opponent_name, wins in opponents.items():
            print(
                f"    Wins against {opponent_name}: {wins} ({(wins / n_games) * 100:.2f}%)"
            )


# game = NimGame(piles_count=5, max_pile_size=10)


agent_dict = {
    "RLAgent": RLAgent(),
    "RandomAgent": RandomAgent(),
    "NimSumAgent": NimSumAgent(),
}

# Evaluate for different combinations of NimGame
for piles_count in [3, 5, 7]:
    for max_pile_size in [5, 10, 15]:
        game = NimGame(piles_count=piles_count, max_pile_size=max_pile_size)
        print(
            f"\nEvaluating for {piles_count} piles with max pile size {max_pile_size}"
        )
        rl_agent = RLAgent()
        rl_agent.train(50000, game)  # Train the RL agent before evaluation
        evaluate_agents(agent_dict, n_games=10000, game=game)
