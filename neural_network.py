
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense

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
    model.add(Dense(18, input_dim=8))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(2, activation='sigmoid'))

    model.compile(loss='mean_squared_error',
        optimizer='adadelta',
        metrics=['accuracy']
    )

    model.fit(training_data, target_data, epochs=500, verbose=2)

    # Separar uma parte do conjunto de treinamento quando tem poucos
    # exemplos é ruim: ele não aprende algumas coisas. Deixa sem
    # separar mesmo.

    # early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', verbose=2)
    # model.fit(training_data, target_data,
    #     epochs=1000,
    #     verbose=2,
    #     validation_split=0.2,
    #     callbacks=[early_stopping]
    # )

    return model

if __name__ == '__main__':
    create_network()