
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
training_data = np.loadtxt(open('training_dataset.csv', "rb"), delimiter=', ', usecols=range(8))
target_data = np.loadtxt(open('training_dataset.csv', "rb"), delimiter=', ', usecols=(8,9))

print(training_data)
print(target_data)

model = Sequential()
model.add(Dense(10, input_dim=8, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(2, activation='sigmoid'))

our_optimizer = keras.optimizers.SGD(lr=0.03, momentum=0.0, decay=0.0, nesterov=False)
model.compile(loss='mean_squared_error',
              optimizer=our_optimizer,
              metrics=['accuracy'])

model.fit(training_data, target_data, epochs=1, verbose=2)

# Output da sigmoide varia de 0 a 1, tem que normalizar pro
# limite min e max que a gente quer de velocidade
# (fiz de 0 a 10, até a gente decidir)
print("Results:")
print(model.predict(training_data) * 10)

print("Expected:")
print(target_data)
