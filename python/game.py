import chess
import chess.svg
import os
import sys
from bot import predict_move
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy

# Sets the environment, PyQt5 did not work on my machine
os.environ["QT_QPA_PLATFORM"] = "xcb"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Sets up window
        self.setGeometry(80, 80, 880, 900)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Sets up QSvgWidget to display the chessboard
        self.widgetSvg = QSvgWidget(parent=self)
        self.layout.addWidget(self.widgetSvg)
        self.layout.setStretch(0, 1)

        # Set up text input and submit button
        self.bottom_layout = QVBoxLayout()
        self.move_input = QLineEdit(self)
        self.move_input.setPlaceholderText("Enter your move (e.g., e2e4)")
        self.bottom_layout.addWidget(self.move_input)
        
        self.submit_button = QPushButton("Submit Move", self)
        self.submit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.submit_button.setMinimumHeight(50)
        self.submit_button.clicked.connect(self.user_move_button)
        self.bottom_layout.addWidget(self.submit_button)

        self.status_label = QLabel("", self)
        self.bottom_layout.addWidget(self.status_label)

        # Add bottom layout to the main layout
        self.layout.addLayout(self.bottom_layout)
        
        # Add stretch to make sure the bottom layout sticks to the bottom
        self.layout.setStretch(1, 0)

        # Initializes the chessboard
        self.chessboard = chess.Board()
        self.process_bot_move()
        self.update_board()

    def update_board(self):
        '''Renders the chess board'''
        chessboardSvg = chess.svg.board(self.chessboard, flipped=True).encode("UTF-8")
        self.widgetSvg.load(chessboardSvg)

    def apply_move(self, move_uci):
        '''Applies a move to the board'''
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.chessboard.legal_moves:
                self.chessboard.push(move)
                self.update_board()
                return True
            else:
                self.status_label.setText("Invalid move. Try again.")
                return False
        except Exception as e:
            self.status_label.setText(f"Error applying move: {e}")
            return False

    def user_move_button(self):
        '''Handles the move input from the user'''
        if self.chessboard.turn == chess.BLACK and not self.chessboard.is_game_over():
            move_input = self.move_input.text()
            if self.apply_move(move_input):
                print(f"You played: {move_input}")
                self.move_input.clear()
                if self.chessboard.is_game_over():
                    self.status_label.setText("Game Over!")
                self.process_bot_move()

    def process_bot_move(self):
        '''Processes the bot's move if it's the bot's turn'''
        if self.chessboard.turn == chess.WHITE and not self.chessboard.is_game_over():
            move = predict_move(self.chessboard)
            print(f"Kush_Bot played: {move}")
            self.apply_move(move.uci())
            if self.chessboard.is_game_over():
                    self.status_label.setText("Game Over!")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
