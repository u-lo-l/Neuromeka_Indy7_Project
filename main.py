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


# step1 : 직접 이동하여 점 두개 받는다. 직접 교시도 좋고, 화살표로 움직여도 좋다.
#       : 하지만 되도록 테이블과 툴이 수직이여야 한다.

# step2 : 점을 입력 받으면 

# step3 : 버튼 눌리면 직선 경로 생성 및 경로 내 젠가가 놓일 위치들을 생성(좌표만)
#       : 생성된 직선 경로의 기울기 파악. -> y축과 이루는 각, x축과 이루는 각 확인
# step4 : place 할 접근 위치로 이동
#       : 현재 joint1의 각도 받아옴

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