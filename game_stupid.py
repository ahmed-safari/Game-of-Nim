import random


def initialize_game():
    """Initializes the game with 2 to 5 piles, each with a random number of items."""
    num_piles = random.randint(2, 5)
    piles = [random.randint(1, 10) for _ in range(num_piles)]
    return piles


def print_piles(piles):
    """Prints the current state of the game."""
    for i, pile in enumerate(piles, start=1):
        print(f"Pile {i}: {'*' * pile} ({pile} items)")


def nim_sum(piles):
    """Calculates the Nim-sum of the current piles."""
    n_sum = 0
    for pile in piles:
        n_sum ^= pile
    return n_sum


def make_ai_move(piles):
    """Determines and makes the AI's move based on the Nim-sum strategy."""
    n_sum = nim_sum(piles)
    for i, pile in enumerate(piles):
        target = pile ^ n_sum
        if target < pile:
            take = pile - target
            piles[i] -= take
            print(f"\nAI removed {take} from pile {i+1}\n")
            return piles
    # If no strategic move is found, remove one item from the largest pile
    max_pile_index = piles.index(max(piles))
    piles[max_pile_index] -= 1
    print(f"\nAI removed 1 from pile {max_pile_index+1} (fallback move)\n")
    return piles


def player_move(piles):
    """Allows the player to make a move."""
    valid_move = False
    while not valid_move:
        try:
            pile = int(input("Select a pile: ")) - 1
            remove = int(input("How many to remove from the pile: "))
            if 0 <= pile < len(piles) and 1 <= remove <= piles[pile]:
                piles[pile] -= remove
                valid_move = True
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input, please enter numbers only.")
    return piles


def game_over(piles):
    """Checks if the game is over."""
    return sum(piles) == 0


def play_nim():
    """Main game loop."""
    piles = initialize_game()
    print("\nGame start! Here are the initial piles:")
    print_piles(piles)

    while not game_over(piles):
        # Player's turn
        print("\nYour turn:")
        piles = player_move(piles)
        print_piles(piles)
        if game_over(piles):
            print("All piles are empty. AI wins!")
            break

        # AI's turn
        print("\nAI's turn:")
        piles = make_ai_move(piles)
        print_piles(piles)
        if game_over(piles):
            print("All piles are empty. You win!")
            break


if __name__ == "__main__":
    play_nim()
