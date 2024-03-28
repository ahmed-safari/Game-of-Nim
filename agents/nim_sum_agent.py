class NimSumAgent:
    """
    An agent that employs the Nim-sum strategy for the Game of Nim. The strategy involves calculating
    the bitwise XOR (Nim-sum) of all pile sizes and making a move that forces the Nim-sum to zero.
    If the Nim-sum is zero at the agent's turn, a random move is simulated by simply taking one from the first non-zero pile.
    """

    def choose_action(self, state):
        """
        Selects an optimal move using the Nim-sum strategy, aiming to reduce the Nim-sum of all piles to zero.

        Parameters:
            state (list[int]): The current state of the game, represented as a list where each element is the size of a pile.

        Returns:
            action (tuple[int, int]): A tuple where the first element is the index of the pile to take from,
                             and the second element is the number of items to remove from that pile.
        """
        nim_sum = 0
        for pile in state:
            nim_sum ^= pile

        if nim_sum == 0:
            # If the Nim-sum is already 0, the strategy is to make a minimal impact move.
            # Here, we simply take one from the first non-empty pile.
            for index, pile in enumerate(state):
                if pile > 0:
                    return (index, 1)  # Take one from the first non-zero pile.

        # If the Nim-sum is not zero, find a move that makes the Nim-sum of all piles zero.
        for index, pile in enumerate(state):
            if pile ^ nim_sum < pile:
                # This means we have a pile that can be reduced to make the Nim-sum zero.
                remove_amount = pile - (pile ^ nim_sum)
                return (index, remove_amount)
