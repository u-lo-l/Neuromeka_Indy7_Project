import numpy as np
import numpy.linalg as al
import time
import math

from indy_utils import indydcp_client as client

from jenga_constants import *
from make_pos_list import *
import indy_button as button
import indy_led as led

def get_points(indy) :
	point_list = []
	cnt = 0
	while 1:
		status_button = indy.get_di()
		if status_button[0] == 1 :
			print("vertex set");
			temp_position = indy.get_task_pos()
			temp_position[2:6] = [TOOL_PLACE_HEIGHT ,0, 180, 0]
			point_list.append(temp_position)
			led.led_blink(indy, 3)
			cnt = cnt + 1
		if status_button[1] == 1:
			print("vertex set done");
			break
	if cnt < 2 :
		raise ValueError
	return (point_list)

def pick_jenga(indy) :
	print("Pick new jenga up")
	curr_joint_status = indy.get_joint_pos()
	curr_joint_status[5] = 0
	indy.joint_move_to(curr_joint_status)
	indy.wait_for_move_finish()
	indy.set_endtool_do(TOOL, TOOL_RELEASE)
	time.sleep(0.5)
	indy.joint_move_to(PICK_ACCESS_JOINT)
	indy.wait_for_move_finish()
	indy.task_move_to(PICK_TARGET_TASK)
	indy.wait_for_move_finish()
	indy.set_endtool_do(TOOL, TOOL_HOLD)
	time.sleep(1)
	indy.task_move_to(PICK_BACK_TASK)
	indy.wait_for_move_finish()

def get_gradient_dir(prev_pos, curr_pos, next_pos) :
	if (prev_pos is None) :
		grad_dir = np.array(next_pos) - np.array(curr_pos)
	elif (next_pos is None) :
		grad_dir = np.array(curr_pos) - np.array(prev_pos)
	else :
		grad_dir = np.array(next_pos) - np.array(prev_pos)
	return  grad_dir / al.norm(grad_dir)

def update_tool_orientation(indy, dir_vec) :
	curr_joint_status = indy.get_joint_pos();
 
	line_length = al.norm(dir_vec[0:3])
	angle_with_y = np.dot(np.array([0.0,1.0,0.0]), dir_vec[0:3])
	angle_with_y = angle_with_y / line_length
	angle_with_y = math.acos(angle_with_y) * 180 / math.pi
	if (np.cross(np.array([0.0,1.0,0.0]), dir_vec[0:3])[2] < 0) :
		angle_with_y = -angle_with_y
	joint6_angle = curr_joint_status[5] - TOOL_ROT_OFFSET;
	joint6_angle -= angle_with_y - 90
	while (joint6_angle < -215) :
		joint6_angle += 360
	while (joint6_angle > 215) :
		joint6_angle -= 360
	curr_joint_status[5] = joint6_angle
	indy.joint_move_to(curr_joint_status)
	indy.wait_for_move_finish()
	
	return (indy.get_task_pos())

def put_jenga(indy, target_position, dir_vec) :
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

def play_domino(indy, pos_list) :
	start_point = pos_list[-1]
	last_jenga = pos_list[-2]
	start_point[3:6] = last_jenga[3:6]
	start_point[2] += PLACE_OFFSET[2]
	indy.task_move_to(start_point)
	indy.wait_for_move_finish()
	indy.set_endtool_do(TOOL, TOOL_HOLD)
	start_point[2] -= PLACE_OFFSET[2]
	indy.task_move_to(start_point)
	indy.wait_for_move_finish()
	start_point[2] += PLACE_OFFSET[2]
	indy.task_move_to(last_jenga)
	indy.wait_for_move_finish()
	indy.task_move_to(start_point)
	indy.wait_for_move_finish()