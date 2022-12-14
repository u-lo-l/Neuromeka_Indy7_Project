import numpy as np
import numpy.linalg as al
import time
import copy
import math

from indy_utils import indydcp_client as client
from jenga_constants import *

def make_line_pos_list(np_pos1, np_pos2) :
	dir_vec = np_pos2 - np_pos1;
	line_length = al.norm(dir_vec[0:3])
	count = int(line_length / STRIDE)
	if (count <= 1) :
		print("path too short. quit program")
		exit()
	dir_vec = dir_vec / count
	poslst = []
	temp = np_pos1
	for i in range(count + 1) :
		temp = np_pos1 + (dir_vec * i)
		poslst.append(temp.tolist())
	return (poslst)

def make_multiline_pos_list(pos_list) :
	print("make multiline")
	count = len(pos_list)
	print("count : ", count)
	multiline_pos_list = []
	for i in range(1, count) :
		print("i : ", i)
		templist = make_line_pos_list(np.array(pos_list[i - 1]), np.array(pos_list[i]))
		print(templist)
		if len(multiline_pos_list) != 0 :
			del(templist[0])
			temp = np.array(multiline_pos_list[-1]) + np.array(templist[1])
			temp /= 2
			templist[0] = temp.tolist()

			temp = np.array(multiline_pos_list[-2]) + np.array(templist[0])
			temp /= 2
			multiline_pos_list[-1] = temp.tolist()

			temp = np.array(templist[0]) + np.array(templist[2])
			temp /= 2
			templist[1] = temp.tolist()

		multiline_pos_list.extend(templist)
	return (multiline_pos_list)