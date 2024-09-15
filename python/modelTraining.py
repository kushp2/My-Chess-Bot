import numpy as np
import tensorflow as tf
import chess
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Flatten, Conv2D, MaxPooling2D
import pickle

def create_policy_value_model(input_shape, output_size):
    '''Creates a neural network model.'''
    common_layers = [
        Input(shape=input_shape),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Flatten()
    ]

    # Policy Head (predicts next move probabilities)
    policy_input = common_layers[0]
    x = policy_input
    for layer in common_layers[1:]:
        x = layer(x)
    policy_x = Dense(256, activation='relu')(x)
    policy_output = Dense(output_size, activation='softmax')(policy_x)  # Output size is number of possible moves

    # Value Head (predicts evaluation score)
    value_input = common_layers[0]
    x = value_input
    for layer in common_layers[1:]:
        x = layer(x)
    value_x = Dense(256, activation='relu')(x)
    value_output = Dense(1, activation='tanh')(value_x)  # Value represents evaluation score

    # Combine heads into a single model
    model = Model(inputs=policy_input, outputs=[policy_output, value_output])
    model.compile(loss=['categorical_crossentropy', 'mse'], optimizer='adam')
    return model


# Load dataset
data = np.load('../game_data/dataset.npy', allow_pickle=True).item()
X, y = data['X'], data['y']

with open('../game_data/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Define model parameters
input_shape = X.shape[1:]
OUTPUT_SIZE = len(label_encoder.classes_)

# Create and train the model
model = create_policy_value_model(input_shape, OUTPUT_SIZE)
model.fit(X, [tf.keras.utils.to_categorical(y, num_classes=OUTPUT_SIZE), np.zeros_like(y)], epochs=50, validation_split=0.2)

# Save the trained model
model.save('../game_data/chess_bot_model1.keras')
