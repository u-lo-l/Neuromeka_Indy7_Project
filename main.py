from indy_utils import indydcp_client as client
import numpy as np
import indy_led as led
import jenga_domino as jenga

robot_ip = "192.168.0.8" # 예시 STEP IP 주소
robot_name = "NRMK-Indy7" # IndyRP2의 경우 "NRMK-IndyRP2"
indy = client.IndyDCPClient(robot_ip, robot_name) # indy 객체

try :
	indy.connect()
	print("CONNECTED SUCCESSFULLY")
	print("Vairalble Setting")
	indy.set_task_vel_level(5)
	indy.set_joint_vel_level(5)
	led.led_blink(indy, 2)
	led.led_on(indy)
	indy.go_home()
	
	input("Indy ready. ENTER to go next step")
	vertices = jenga.get_points(indy)

	input("Press ENTER to go next step")
	indy.go_home()
	# position_list = jenga.make_line_pos_list(start, end)
	position_list = jenga.make_multiline_pos_list(vertices)

	print("count : ", len(position_list))
	for l in position_list :
		print(l)
	
	input("Press ENTER to go next step")
	
	jenga.make_dominos(indy, position_list)

	input("Press ENTER to go next step")

	jenga.play_domino(indy, position_list)

except :
	print("Erro Occurs")

indy.set_task_vel_level(3)
indy.set_joint_vel_level(3)
indy.go_home()
led.led_off(indy)
indy.disconnect()
print("DISCONNECTED")	