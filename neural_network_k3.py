
from vrep import *
from math import sqrt

def end_connection(clientID):
  print("Encerrando conexão...")

  simxPauseSimulation(clientID, simx_opmode_oneshot)

  # Before closing the connection to V-REP, make sure that the last command
  # sent out had time to arrive. You can guarantee this with (for example):
  simxGetPingTime(clientID)

  simxFinish(clientID)

def euclidean_distance(pointA, pointB):
  return (pointB[0]-pointA[0])**2 + (pointB[1]-pointA[1])**2

if __name__ == "__main__": 
  simxFinish(-1) # Just in case, close all connections

  print("Objetivo (x y)")
  goal_x = int(input())
  goal_y = int(input())

  print("Conectando-se ao VREP...", end='')
  clientID = simxStart('127.0.0.1', 19999, True, True, 5000, 5)

  scene_name = "CenaKhepheraK3.ttt"

  if clientID != -1:
    print("Sucesso!")

		# Inicialização do robo
    robot_name = "K3_robot"
    print(f"Procurando {robot_name}...", end='')
    returnCode, robot_handle = simxGetObjectHandle(clientID, robot_name, simx_opmode_blocking)

    if returnCode == simx_return_ok:
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
    sensor_handles = [0]*NUM_SENSORS
    distances = [0]*NUM_SENSORS

    for name in sensor_names:
      print(f"  {name}...", end='')
      returnCode, handle = simxGetObjectHandle(clientID, name, simx_opmode_blocking)
      if returnCode == simx_return_ok:
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

    #
    #
    # Inicialização e treino da rede neural
    #
    #

    #	Loop de Execução
    while (simxGetConnectionId(clientID) != -1):
      # Lê posição e ângulo
      returnCode, position = simxGetObjectPosition(clientID, robot_handle, -1, simx_opmode_blocking)
      returnCode, eulerAngles = simxGetObjectOrientation(clientID, robot_handle, -1, simx_opmode_blocking)
      current_x = position[0]
      current_y = position[1]
      current_angle = eulerAngles[2]
      distance_to_goal = euclidean_distance((current_x, current_y), (goal_x, goal_y))

      print(f"\nPosição do {robot_name}: ({current_x}, {current_y})")
      print(f"  Orientação: {current_angle} radianos")
      print(f"  Distância até o objetivo: {distance_to_goal}")

      # Lê os sensores, calcula as distâncias
      for i in range(NUM_SENSORS):
        _, detectionState, detectedPoint, _, _ = simxReadProximitySensor(clientID, sensor_handles[i], simx_opmode_blocking)

        if detectionState:
          distances[i] = (pow(detectedPoint[0], 2) + 
                          pow(detectedPoint[1], 2) + 
                          pow(detectedPoint[2], 2))
          distances = sqrt(distances[i])
        else:
          distances[i] = 1;

      #
      #
      # Rede neural (já treinada):
      #   Inputs: distance_to_goal, current_angle, distância dos 5 sensores
      #   Outputs: left_speed, right_speed
      #
      #

      left_speed, right_speed = 10, 10

      print(f"  Esq={left_speed}, Dir={right_speed}")
      _ = simxSetJointTargetVelocity(clientID, left_motor_handle, left_speed, simx_opmode_oneshot)
      _ = simxSetJointTargetVelocity(clientID, right_motor_handle, right_speed, simx_opmode_oneshot)

    print("Conexão fechada!")
    end_connection(clientID)
    exit()
  else:
    print("Falhou!")
    print(f"Verifique se o VREP está rodando com a cena {scene_name}!")