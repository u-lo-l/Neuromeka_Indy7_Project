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
	dir_vec_stride = dir_vec / count
	poslst = []
	for i in range(count) :
		np_pos1 += (dir_vec_stride * i)
		poslst.append(np_pos1.tolist())
	return (poslst)

def make_multiline_pos_list(pos_list) :
	count = len(pos_list)
	multiline_pos_list = []
	for i in range(1, count) :
		templist = make_line_pos_list(pos_list[i - 1], pos_list[i])
		if len(multiline_pos_list) != 0 :
			del(templist[0])
		multiline_pos_list.extend(templist)
	return (multiline_pos_list)