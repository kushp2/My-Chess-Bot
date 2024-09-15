import chess
import chess.pgn
import numpy as np
from dotenv import load_dotenv
from sklearn.preprocessing import LabelEncoder
import pickle
import os

load_dotenv()


def parse_pgn(file_path):
    '''parses the games from the file'''
    games = []
    with open(file_path, "r") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            games.append(game)
    return games

def extract_moves(game):
    '''extracts the moves from the games'''
    moves = []
    board = chess.Board()
    for move in game.mainline_moves():
        moves.append((board.fen(), move.uci()))
        board.push(move)
    return moves

def board_to_one_hot(board):
    '''Convert a chess board state to a one-hot encoded numpy array.'''
    piece_map = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5,
    }
    
    board_array = np.zeros((8, 8, 12), dtype=np.float32)  # Shape should be (8, 8, 12)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color_index = 0 if piece.color == chess.WHITE else 6
            piece_index = piece_map.get(piece.piece_type, None)
            if piece_index is None:
                continue
            board_array[chess.square_rank(square), chess.square_file(square), piece_index + color_index] = 1.0  # Remove channel dimension
    
    return board_array


def create_dataset(all_moves):
    '''Creates dataset from extracted  moves'''
    X = []
    y = []
    move_list = []
    for game_moves in all_moves:
        for board_state, move in game_moves:
            board = chess.Board(board_state)
            board_vector = board_to_one_hot(board)
            X.append(board_vector)
            move_list.append(move)

    # Encode moves to integers
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(move_list)
    
    # Save LabelEncoder
    with open('../game_data/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    return np.array(X), np.array(y)




file_path = os.getenv('FILE_PATH')
games = parse_pgn(file_path)
all_moves = [extract_moves(game) for game in games]
X, y = create_dataset(all_moves)
np.save('../game_data/dataset.npy', {'X': X, 'y': y})