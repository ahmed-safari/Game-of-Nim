def get_allowed_moves(piles):
    """
    This function returns the set of all allowed moves in the current state.
    Each move is a tuple `(i, j)` where `i` is the index of the pile and `j` is the number of objects to remove from that pile.

    Parameters:
        piles (list): A list of integers representing the number of objects in each pile. For example, [3, 4, 5] means there are 3 piles with 3, 4, and 5 objects, respectively.

    Returns:
        set: A set of all allowed moves. Each move is a tuple `(i, j)` where `i` is a pile index and `j` is a positive integer.

    """
    actions = set()
    for i, pile in enumerate(piles):
        for j in range(1, pile + 1):
            actions.add(
                (i, j)
            )  # This meanns that the player can take j stones from pile i
    return actions
