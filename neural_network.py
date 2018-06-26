
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
# fazendo testes no site tensorflow acabei achando um "padrão"legal: 
# para 13 entradas e 2 saidas, fazer 17 (15 + 2) neuronios na primeira camada,
# (como sao 2 saidas) com 2 camadas intermediarias, e a cada camada adicional 
# subtrair 1 neurônio (as vezes ajuda como critério de desempate para conflitos)
    model.add(Dense(25, input_dim=8, activation='sigmoid'))
    model.add(Dense(24, activation='sigmoid'))
    model.add(Dense(23, activation='sigmoid'))
    model.add(Dense(2, activation='tanh'))

    our_optimizer = keras.optimizers.SGD(lr=0.03, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss='mean_squared_error',
    #            optimizer=our_optimizer,
                optimizer='adam',
                metrics=['accuracy'])

    model.fit(training_data, target_data, epochs=1000, verbose=2)

    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss',
                                min_delta=0,
                                patience=0,
                                verbose=0, mode='auto')
    model.fit(training_data, target_data,
        epochs=1000,
        verbose=2,
        validation_split=0.3,
        callbacks=[early_stopping]
    )

    return model

if __name__ == '__main__':
    create_network()