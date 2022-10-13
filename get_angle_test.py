from indy_utils import indydcp_client as client
import time
import numpy as np
import copy

LED_PIN = 10
LED_ON = 1
LED_OFF = 0
robot_ip = "192.168.0.8" # 예시 STEP IP 주소
robot_name = "NRMK-Indy7" # IndyRP2의 경우 "NRMK-IndyRP2"
indy = client.IndyDCPClient(robot_ip, robot_name) # indy 객체 생성


try :
	indy.connect()
	print("CONNECTED SUCCESSFULLY")
	print("Vairalble Setting")
	# indy.go_zero()
	# indy.wait_for_move_finish()
	indy.go_home()
	indy.wait_for_move_finish()
	indy.set_do(LED_PIN, LED_ON)
	np_pos = [0.4397294470827642, -0.17321585539922313, 0.09314949529313152, 0.0, 180.0, 0.0]
	indy.task_move_to(np_pos)
	indy.wait_for_move_finish()
	base_joint_angle = indy.get_joint_pos()[5]
	print(base_joint_angle)
	np_pos2 = [0.4729077202233878, 0.09873595446383863, 0.09316427484965083, 0.0, 180.0, 0.0]
	indy.task_move_to(np_pos2)
	indy.wait_for_move_finish()
	base_joint_angle = indy.get_joint_pos()[5]
	print(base_joint_angle)
	# indy.go_home()
except :
	print("Erro Occurs")
	
indy.set_do(LED_PIN, LED_OFF)
indy.disconnect()
print("DISCONNECTED")