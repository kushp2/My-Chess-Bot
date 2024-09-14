import random

def get_random_move(board):
    """Return a random legal move from the current board state."""
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)