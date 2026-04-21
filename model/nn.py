"""
Модуль загрузки модели нейронной сети для классификации геометрических фигур.
Классы: circle (0), triangle (1), square (2)
Архитектура: 400 -> 3000 -> 1000 -> 200 -> 10 -> 3
"""
import os
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


def get_model():
    """Строит архитектуру и загружает веса из best.weights.h5."""
    model = Sequential([
        Dense(3000, activation='relu', input_shape=(400,)),
        Dense(1000, activation='relu'),
        Dense(200,  activation='relu'),
        Dense(10,   activation='relu'),
        Dense(3,    activation='softmax'),
    ])

    weights_path = os.path.join(os.path.dirname(__file__), 'best.weights.h5')
    model.load_weights(weights_path)
    return model
