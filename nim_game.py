import random


class NimGame:

    def __init__(self, piles_count=5, max_pile_size=10):
        self.piles = [random.randint(1, max_pile_size) for _ in range(piles_count)]
        self.game_over = False

    # def get_allowed_moves(piles):
    #     actions = set()
    #     for i, pile in enumerate(piles):
    #         for j in range(1, pile + 1):
    #             actions.add(
    #                 (i, j)
    #             )  # This meanns that the player can take j stones from pile i
    #     return actions
    def reset(self):
        """
        Reset the game to its initial state.
        """
        self.__init__()

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.game_over:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.game_over = True

    def display(self):
        """
        Display the current state of the game.
        """
        for i, pile in enumerate(self.piles, start=1):
            print(f"Pile {i}: {'*' * pile} ({pile} items)")
