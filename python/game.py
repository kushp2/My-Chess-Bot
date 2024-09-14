import chess
import sys
from PyQt5.QtWidgets import QApplication 
from board import create_window
from bot import get_random_move

def game_loop(window):
    '''Game loop function'''
    board = window.get_board()

    while not board.is_game_over():
        # If it's white's turn (the bot)
        if board.turn == chess.WHITE:
            move = get_random_move(board)
            print(f"Kush Bot plays: {move}")
        else:
            move = None
            while move not in board.legal_moves:
                try:
                    move_input = input("Enter your move: ")
                    move = chess.Move.from_uci(move_input)
                except:
                    print("Invalid move format. Use UCI format (e.g., e2e4)")
            print(f"You play: {move}")

        # Apply the move to the board
        window.apply_move(move.uci())

    print("Game Over!")
    print("Result: ", board.result())



if __name__ == "__main__":
    window, app = create_window()
    game_loop(window)
    sys.exit(app.exec_())
    quit()