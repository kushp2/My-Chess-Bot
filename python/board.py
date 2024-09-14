import chess
import chess.svg
import os

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

#sets the evnironment, PyQt5 did not work on my machine
os.environ["QT_QPA_PLATFORM"] = "xcb"

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        #sets up window with QSvgWidget to display the chessboard
        self.setGeometry(80, 80, 880, 880)
        self.widgetSvg = QSvgWidget(parent = self)
        self.widgetSvg.setGeometry(8,8, 800, 800)

        #initilizes the chess board
        self.chessboard = chess.Board()
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
        except Exception as e:
            print(f"Error applying move: {e}")


    def get_board(self):
        '''Return the current chessboard instance'''
        return self.chessboard


def create_window():
    '''Create and return a MainWindow instance'''
    app = QApplication([])
    window = MainWindow()
    window.show()
    return window, app