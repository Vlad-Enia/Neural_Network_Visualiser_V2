from keras import Sequential
from keras.layers import Dense, Input
from keras.activations import relu, sigmoid, softmax, tanh
from keras.optimizers import gradient_descent_v2
from keras.models import load_model
import numpy as np


def create_nn(n_hidden_layers, hidden_layers_size_list, output_layer_size, hidden_layers_activation_list,
              output_layer_activation, learning_rate, loss_function):
    model = Sequential()
    model.add(Input(shape=(2,)))
    for i in range(0, n_hidden_layers):
        model.add(Dense(hidden_layers_size_list[i], hidden_layers_activation_list[i]))
    model.add(Dense(output_layer_size, output_layer_activation))
    model.compile(gradient_descent_v2.SGD(learning_rate=learning_rate), loss=loss_function)
    return model


def train_nn(model, dataset_train, labels_train, dataset_test, labels_test, n_labels, epochs, batch_size):
    if n_labels > 2:
        labels_train = convert_to_one_hot(labels_train)
        labels_test = convert_to_one_hot(labels_test)
    history = model.fit(dataset_train, labels_train, validation_data=(dataset_test, labels_test), validation_freq=1, epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)
    return history


def save_model(model, path):
    model.save(path)


def convert_from_one_hot(b):
    a = np.argmax(b, axis=1)
    return np.array(a)


def convert_to_one_hot(a):
    b = np.zeros((a.size, a.max() + 1))
    b[np.arange(a.size), a] = 1
    return b

