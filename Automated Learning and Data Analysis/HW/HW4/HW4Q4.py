# ANN

import tensorflow as tf
from tensorflow import keras
import os
import numpy as np
import random
import pandas as pd
from matplotlib import pyplot as plt

# A) Check backend
from keras import backend as K
print(K.backend())

# B) Set seeds to 2022
seed = 2002
os.environ['PYTHONHASHSEED'] = '2022'
tf.random.set_seed(seed)
np.random.RandomState(seed)
random.seed(seed)

# C) Neural network code
# Hidden neurons
X = (4, 16, 32, 64)

for n in X:
    # Load in the data
    train = pd.DataFrame(pd.read_csv('ANN/test_data_2022.csv'))
    val = pd.DataFrame(pd.read_csv('ANN/val_data_2022.csv'))
    test = pd.DataFrame(pd.read_csv('ANN/test_data_2022.csv'))

    # Split into x's and y's
    x_train = train.iloc[:, 0:60].to_numpy()
    y_train = train.iloc[:, 60].to_numpy()
    x_val = val.iloc[:, 0:60].to_numpy()
    y_val = val.iloc[:, 60].to_numpy()
    x_test = test.iloc[:, 0:60].to_numpy()
    y_test = test.iloc[:, 60].to_numpy()

    # Define neural network architecture
    # Neurons per layer
    input_neurons = 60
    hidden_neurons = n
    output_neurons = 1

    # set variables
    epochs = 5
    hidden_act = 'relu'
    out_act = 'sigmoid'
    loss = 'binary_crossentropy'
    optim = 'adam'
    metrics = 'accuracy'
    batch_size = 10

    # set up model
    inputs = keras.Input(shape=(input_neurons,), name='data')
    x = keras.layers.Dense(hidden_neurons, activation=hidden_act, name='hidden')(inputs)
    outputs = keras.layers.Dense(output_neurons, activation=out_act, name='predictions')(x)

    model = keras.Model(inputs=inputs, outputs=outputs)

    # Configure model
    model.compile(optimizer=optim, loss=loss, metrics=metrics)

    # fit model to data
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                        validation_data=(x_val, y_val))

    # evaluate on test data
    results = model.evaluate(x_test, y_test)
    print('Results for hidden network with ' + str(hidden_neurons) + ' hidden neurons: \n')
    print('loss, accuracy: ', results)

# D) Get everything to plot, plot
resultsummary = pd.DataFrame()
resultsummary['X'] = pd.DataFrame(X)
resultsummary['Training Acc.'] = pd.DataFrame([0.628, 0.76, 0.828, 0.88])
resultsummary['Validation Acc.'] = pd.DataFrame([0.56, 0.724, 0.804, 0.8080])
resultsummary['Test Acc.'] = pd.DataFrame([0.644, 0.780, 0.844, 0.888])

plt.plot(resultsummary['X'], resultsummary['Training Acc.'], label='Training')
plt.plot(resultsummary['X'], resultsummary['Validation Acc.'], label='Validation')
plt.legend()
plt.ylabel('Accuracy')
plt.xlabel('Number of Hidden Neurons')
plt.title('Model Accuracy vs. Number of Hidden Neurons')
plt.show()

# E) Simple analysis, optimal number of hidden neurons
# The accuracy appears to increase the more hidden neurons are present in our model. This seems reasonable, as more
# neurons would allow for more connections. The accuracy does appear to approach a limit, however, so adding
# more hidden neurons may not help very much. The optimal number of hidden neurons is 64 since it gives the best results.

# F) Test accuracy with 64 hidden neurons is 0.888


