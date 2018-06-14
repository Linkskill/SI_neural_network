
# Exemplo adaptado de
# https://blog.thoughtram.io/machine-learning/2016/11/02/understanding-XOR-with-keras-and-tensorlow.html
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense

# the four different states of the XOR gate
training_data = np.array([[0,0],[0,1],[1,0],[1,1]], "float32")

# the four expected results in the same order
target_data = np.array([[0],[1],[1],[0]], "float32")

model = Sequential()
# 16 é o número de outputs dessa camada (para usar na próxima camada)
model.add(Dense(16, input_dim=2, activation='sigmoid'))
# Pra camada seguinte, não precisa setar o input, ele já pega o que
# a gente definiu como output da camada anterior (16)
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['binary_accuracy'])

model.fit(training_data, target_data, nb_epoch=5000, verbose=2)

# predict(nosso input)
print(model.predict(training_data).round())