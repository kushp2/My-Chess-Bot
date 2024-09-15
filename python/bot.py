import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import chess
from parseData import board_to_one_hot
import pickle

# Load the trained model and label encoder
model = load_model('../game_data/chess_bot_model1.keras')
with open('../game_data/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

def predict_move(board):
    board_vector = board_to_one_hot(board)
    board_vector = np.expand_dims(board_vector, axis=0)  # Add batch dimension
    
    policy_probs, value = model.predict(board_vector)  # Get policy and value outputs
    
    # Choose a move based on policy
    predicted_move_index = np.argmax(policy_probs[0])
    move = label_encoder.inverse_transform([predicted_move_index])[0]
    predicted_move = chess.Move.from_uci(move)
    
    legal_moves = list(board.legal_moves)
    if predicted_move in legal_moves:
        return predicted_move
    
    # Fallback: choose a random legal move if the predicted one is illegal
    return np.random.choice(legal_moves)
