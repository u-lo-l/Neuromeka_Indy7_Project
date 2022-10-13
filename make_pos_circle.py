from indy_utils import indydcp_client as client
from indy_utils.indy_program_maker import JsonProgramComponent
import time
import numpy as np
import matplotlib
import math

robot_ip = "192.168.0.8"
robot_name = "NRMK-Indy7"
indy = client.IndyDCPClient(robot_ip, robot_name)

np_pos1 = [0.4397294470827642, -0.17321585539922313, 0.09314949529313152, 0.0, 180.0, 0.0]
np_pos1 = np.array(np_pos1)

np_pos2 = [0.4729077202233878, 0.09873595446383863, 0.09316427484965083, 0.0, 180.0, 0.0]
np_pos2 = np.array(np_pos2)

def rad(a,b):
    x0=(a[0]+b[0])/2
    y0=(a[1]+b[1])/2
    ans= x0**2 + y0**2
    r=math.sqrt(ans)
    return r

def get_point():
    spot = []
    setspot=indy.get_default()
    spot=spot.append(setspot)



def choose_point(a,b):
    r=rad(a,b)
    print(r)
    c_spot=[]
    for c in range(0,3):
        c_spot.append((a[c]+b[c])/2)
    print(c_spot)
    choose_point=[]
    for n in range(0,8):
        x = c_spot[0] + r*math.cos(n*math.pi/4)
        y = c_spot[1] + r*math.sin(n*math.pi/4)
        p = [x, y, 0.09314949529313152, 0.0, 180.0, 0.0 ]
        choose_point.append(p)
    print(choose_point)
    return choose_point
        

choose_point(np_pos1,np_pos2)