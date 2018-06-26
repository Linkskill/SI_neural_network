
from vrep import *
from math import pi
from math import sqrt
from math import atan2
from neural_network import *

def end_connection(clientID):
  print("Encerrando conexão...")

  simxPauseSimulation(clientID, simx_opmode_oneshot)

  # Before closing the connection to V-REP, make sure that the last command
  # sent out had time to arrive. You can guarantee this with (for example):
  simxGetPingTime(clientID)

  simxFinish(clientID)

def euclidean_distance(pointA, pointB):
  return sqrt( (pointB[0]-pointA[0])**2 + (pointB[1]-pointA[1])**2 )

if __name__ == "__main__": 
  simxFinish(-1) # Just in case, close all connections

  print("Objetivo (x y)")
  goal_x = float(input())
  goal_y = float(input())

  print("Conectando-se ao VREP...", end='')
  clientID = simxStart('127.0.0.1', 19999, True, True, 5000, 5)
  scene_name = "CenaKhepheraK3.ttt"

  if clientID != -1:
    print("Sucesso!")

		# Inicialização do robo
    robot_name = "K3_robot"
    print(f"Procurando {robot_name}...", end='')
    return_code, robot_handle = simxGetObjectHandle(clientID, robot_name, simx_opmode_blocking)

    if return_code == simx_return_ok:
      print("Encontrado!")
    else:
      print("Falhou!")
      print(f"Verifique se a cena {scene_name} está aberta e rodando no VREP.")
      end_connection(clientID)
      exit()

    # Inicialização dos sensores
    print("Procurando sensores...")
    NUM_SENSORS = 6
    sensor_names = [ "K3_infraredSensorL", "K3_infraredSensorLM",
                    "K3_infraredSensorML", "K3_infraredSensorMR",
                    "K3_infraredSensorRM", "K3_infraredSensorR" ]
    sensor_handles = []
    distances = [0]*NUM_SENSORS

    for name in sensor_names:
      print(f"  {name}...", end='')
      return_code, handle = simxGetObjectHandle(clientID, name, simx_opmode_blocking)
      if return_code == simx_return_ok:
        print("ok!")
        sensor_handles.append(handle)
      else:
        print("Falhou!")
        end_connection(clientID)

    # Inicialização dos motores
    print("Conectando-se aos motores...", end='')
    return_code_left, left_motor_handle = simxGetObjectHandle(clientID, "K3_leftWheelMotor", simx_opmode_blocking)
    return_code_right, right_motor_handle = simxGetObjectHandle(clientID, "K3_rightWheelMotor", simx_opmode_blocking)
    if return_code_left == simx_return_ok and return_code_right == simx_return_ok:
      print("ok!")
    else:
      print("Falhou!")
      end_connection(clientID)
      exit()
    print()

    # Inicialização e treino da rede neural
    model = create_network()
    multiplier = 5

    #	Loop de Execução
    while (simxGetConnectionId(clientID) != -1):
      # Lê posição e ângulo
      return_code, position = simxGetObjectPosition(clientID, robot_handle, -1, simx_opmode_blocking)
      return_code, euler_angles = simxGetObjectOrientation(clientID, robot_handle, -1, simx_opmode_blocking)
      current_x = position[0]
      current_y = position[1]
      current_angle = euler_angles[2]

      # Calcula a distancia e o angulo com o objetivo
      distance_to_goal = euclidean_distance((current_x, current_y), (goal_x, goal_y))
      if distance_to_goal < 0.1:
        break

      goal_angle = atan2(goal_y-current_y, goal_x-current_x)
      angle_turning_to_one_side = abs(goal_angle - current_angle)
      angle_turning_to_opposite_side = (2*pi) - angle_turning_to_one_side

      smallest_angle_to_turn = min(angle_turning_to_one_side, angle_turning_to_opposite_side)
      if smallest_angle_to_turn == angle_turning_to_one_side:
        angle_to_turn = goal_angle - current_angle
      else:
        angle_to_turn = -angle_turning_to_opposite_side

      if angle_to_turn > pi:
        angle_to_turn -= 2*pi

      print(f"\nPosição do {robot_name}: ({current_x:2f}, {current_y:2f})")
      print(f"  Orientação atual: {current_angle:.2f} radianos")
      print(f"  Distância até o objetivo: {distance_to_goal:2f}")
      print(f"  Angulo para ficar de frente pro objetivo: {angle_to_turn:2f} radianos")

      # Lê os sensores, calcula as distâncias
      for i in range(NUM_SENSORS):
        _, detectionState, detectedPoint, _, _ = simxReadProximitySensor(clientID, sensor_handles[i], simx_opmode_blocking)

        if detectionState:
          distances[i] = (pow(detectedPoint[0], 2) + 
                          pow(detectedPoint[1], 2) + 
                          pow(detectedPoint[2], 2))
          distances[i] = sqrt(distances[i])
        else:
          distances[i] = 1

      # Rede neural (já treinada):
      #   Inputs: distance_to_goal, angle_to_turn, distância dos 6 sensores
      #   Outputs: left_speed, right_speed

      inputs = np.array([[
        distance_to_goal,
        angle_to_turn,
        distances[0],
        distances[1],
        distances[2],
        distances[3],
        distances[4],
        distances[5]
      ]])
      outputs = model.predict(inputs)[0] * multiplier
      # Começa lento e vai aumentando até a velocidade
      # máxima para não sair "empinando"
      if multiplier < 20:
        multiplier += 5

      left_speed, right_speed = outputs[0], outputs[1]

      print(f"  Esq={left_speed:2f}, Dir={right_speed:2f}")
      _ = simxSetJointTargetVelocity(clientID, left_motor_handle, left_speed, simx_opmode_streaming)
      _ = simxSetJointTargetVelocity(clientID, right_motor_handle, right_speed, simx_opmode_streaming)

    print("Conexão fechada!")
    end_connection(clientID)
    exit()
  else:
    print("Falhou!")
    print(f"Verifique se o VREP está rodando com a cena {scene_name}!")