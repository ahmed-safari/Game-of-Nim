import time
from agents import RLAgent, RandomAgent, NimSumAgent
from nim_game import NimGame


def play_against_human(agent, game):
    """
    Play a game of Nim against the agent.

    Parameters:
    - agent (object): An instance of an agent class with a choose_action method.
    - game (object): An instance of the NimGame class.

    Returns:
    - None: Prints out the game state and result.
    """

    game.reset()
    current_player = 0  # 0 for agent, 1 for human

    while not game.game_over:
        # print("Current game state:")
        print()
        game.display()
        if current_player == 0:
            print("Agent's turn:")
            action = agent.choose_action(game.piles)
            time.sleep(1)
            print(f"Agent chose to take {action[1]} from pile {action[0] + 1}")
        else:
            while True:
                print("Your turn:")
                pile = int(input("Select a pile: ")) - 1
                count = int(input("How many to remove from the pile: "))

                action = (pile, count)
                if action not in NimGame.get_allowed_moves(game.piles):
                    print("Invalid move. Try again.")
                    continue
                break

        game.move(action)
        current_player = 1 - current_player

    # Determine winner
    if current_player == 0:
        print("You win!")
    else:
        print("The agent wins!")


# agents = {
#     "RLAgent": RLAgent(),
#     "RandomAgent": RandomAgent(),
#     "NimSumAgent": NimSumAgent(),
# }

# List of agents
agents = [RLAgent(), RandomAgent(), NimSumAgent()]


# Get user settings
n_piles = int(input("Enter the number of piles: "))
max_items = int(input("Enter the maximum number of items: "))

# Print the list of agents
for i, agent in enumerate(agents, start=1):
    print(f"{i}. {type(agent).__name__}")
# Get user to pick an agent
agent_index = int(input("Enter the number of the agent to play against: ")) - 1
while agent_index < 0 or agent_index >= len(agents):
    print("Invalid choice. Please enter a number corresponding to an agent.")
    agent_index = int(input("Enter the number of the agent to play against: ")) - 1

# Initialize the chosen agent
agent = agents[agent_index]

# Initialize the game with the chosen settings
game = NimGame(piles_count=n_piles, max_pile_size=max_items)

if agent == agents[0]:
    # Train the RL agent
    agent.train(30000, game)

# Play the game

play_against_human(agent, game)
