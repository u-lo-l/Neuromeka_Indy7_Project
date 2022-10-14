from indy_utils import indydcp_client as client
import numpy as np
import numpy.linalg as al
import time
import indy_led as led
import jenga_domino as jenga
import gripper as grip

robot_ip = "192.168.0.8" # 예시 STEP IP 주소
robot_name = "NRMK-Indy7" # IndyRP2의 경우 "NRMK-IndyRP2"
indy = client.IndyDCPClient(robot_ip, robot_name) # indy 객체

try :
	indy.connect()
	print("CONNECTED SUCCESSFULLY")
	print("Vairalble Setting")
	led.led_blink(indy, 2)
	led.led_on(indy)
	indy.go_home()
	
	print("Indy ready. Press ENTER to start", end = " ")
	input()
	
	vertices = jenga.get_points(indy)

	start = np.array(vertices[0]);
	end = np.array(vertices[1]);
	print("start : ", start)
	print(" end  : ", end)

	print("Press ENTER to go next step")
	input()
	
	position_list = jenga.make_line_pos_list(start, end)
	
	print("count : ", len(position_list))
	for l in position_list :
		print(l)
	
	print("Press ENTER to go next step")
	input()
	
	jenga.make_dominos(indy, position_list)

	print("Press ENTER to go next step")
	input()

	jenga.play_domino(indy, position_list)
	indy.go_home()

except :
	print("Erro Occurs")

led.led_off(indy)
indy.disconnect()
print("DISCONNECTED")	