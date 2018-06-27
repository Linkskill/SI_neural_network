
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
import keras.optimizers

# Inputs:
#   distance_to_goal
#   angle_to_turn
#   6 distancias captadas pelos sensores (L, LM, ML, MR, RM , R)
# Outputs:
#   left_speed
#   right_speed

def create_network():
    training_data = np.loadtxt(open('training_dataset.csv', "rb"), delimiter=', ', usecols=range(8))
    target_data = np.loadtxt(open('training_dataset.csv', "rb"), delimiter=', ', usecols=(8,9))

    print(training_data)
    print(target_data)

    model = Sequential()
    model.add(Dense(31, input_dim=8, activation='sigmoid'))
    model.add(Dense(30, activation='sigmoid'))
    model.add(Dense(29, activation='sigmoid'))
    model.add(Dense(2, activation='tanh'))

    our_optimizer = keras.optimizers.SGD(lr=0.03, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss='mean_squared_error',
    #            optimizer=our_optimizer,
                optimizer='adam',
                metrics=['accuracy'])

    model.fit(training_data, target_data, epochs=500, verbose=2)

    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss',
                                min_delta=0,
                                patience=0,
                                verbose=0, mode='auto')
    model.fit(training_data, target_data,
        epochs=500,
        verbose=2,
        validation_split=0.3,
        callbacks=[early_stopping]
    )

    return model

if __name__ == '__main__':
    create_network()