import numpy as np
import numpy.linalg as al
import time
import math

from indy_utils import indydcp_client as client

from jenga_constants import *
from make_pos_list import *
import indy_button as button
import indy_led as led

def get_points(indy, num_of_points = 2) :
	point_list = []
	for i in range(0, num_of_points) :
		while (button.wait_for_button_input(indy) != 1) :
			pass
		temp_position = indy.get_task_pos()
		temp_position[2:4] = [TOOL_PLACE_HEIGHT ,0, 180, 0]
		point_list.append(temp_position)
		led.led_blink(indy, 3)
	print(point_list)
	return (point_list)

def pick_jenga(indy) :
	print("Pick new jenga up")
	indy.set_endtool_do(TOOL, TOOL_RELEASE)
	time.sleep(0.5)
	indy.task_move_to(PICK_ACCESS)
	indy.wait_for_move_finish()
	indy.task_move_to(PICK_TARGET)
	indy.wait_for_move_finish()
	indy.set_endtool_do(TOOL, TOOL_HOLD)
	time.sleep(1)
	indy.task_move_to(PICK_BACK)
	indy.wait_for_move_finish()

def get_gradient_dir(prev_pos, curr_pos, next_pos) :
	if (prev_pos is None) :
		grad_dir = next_pos - curr_pos
	elif (next_pos is None) :
		grad_dir = curr_pos - prev_pos
	else :
		grad_dir = next_pos - prev_pos
	return  grad_dir / al.norm(grad_dir)

def update_tool_orientation(indy, dir_vec) :
	# print("ORIENTATION")
	curr_joint_status = indy.get_joint_pos();
	# print ("curr joint", curr_joint_status)
 
	line_length = al.norm(dir_vec[0:3])
	angle_with_y = np.dot(np.array([0.0,1.0,0.0]), dir_vec[0:3])
	angle_with_y = angle_with_y / line_length
	angle_with_y = math.acos(angle_with_y) * 180 / math.pi
	# print("angle_with_y : ", angle_with_y)

	joint6_angle = curr_joint_status[5];
	joint6_angle -= TOOL_ROT_OFFSET + angle_with_y
	# joint6_angle %= 360
	while (joint6_angle < -215) :
		joint6_angle += 360
	while (joint6_angle > 215) :
		joint6_angle -= 360
	curr_joint_status[5] = joint6_angle
	indy.joint_move_to(curr_joint_status)
	indy.wait_for_move_finish()
	
	return (indy.get_task_pos())

def put_jenga(indy, target_position, dir_vec) :
	# print("Put Jenga")
	above_position = [x + y for x,y in zip(target_position, PLACE_OFFSET)]
	indy.task_move_to(above_position)
	indy.wait_for_move_finish()
	above_position = update_tool_orientation(indy, dir_vec)
	target_position = [x - y for x,y in zip(above_position, PLACE_OFFSET)]
	indy.task_move_to(target_position)
	indy.wait_for_move_finish()
	indy.set_endtool_do(TOOL, TOOL_RELEASE)
	time.sleep(0.5)
	indy.task_move_to(above_position)
	indy.wait_for_move_finish()
 
def play_domino(indy, pos_list) :
	start_point = pos_list[-1]
	last_jenga = pos_list[-2]
	start_point[3:3] = last_jenga[3:3]
	start_point[2] += PLACE_OFFSET
	indy.task_move_to(start_point)
	indy.wait_for_task_finish()
	start_point[2] -= PLACE_OFFSET
	indy.task_move_to(start_point)
	indy.wait_for_task_finish()
	indy.task_move_to(last_jenga)
	indy.wait_for_task_finish()

def make_dominos(indy, pos_list) :
	# print("make_dominos")
	count = len(pos_list)
	for i in range(count - 1) :
		pick_jenga(indy)
		if i is 0 :
			dir_vec3 = get_gradient_dir(None, pos_list[1], pos_list[2])[0:3]
		else :
			dir_vec3 = get_gradient_dir(pos_list[i - 1], pos_list[i], pos_list[i + 1])[0:3]
		put_jenga(indy, pos_list[i], dir_vec3)
