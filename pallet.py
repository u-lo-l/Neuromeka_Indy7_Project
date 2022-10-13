from nbformat import current_nbformat
from indy_utils import indydcp_client as client
import time
robot_ip = "192.168.0.8"    # 예시 STEP IP 주소
robot_name = "NRMK-Indy7"   # IndyRP2의 경우 "NRMK-IndyRP2"
indy = client.IndyDCPClient(robot_ip, robot_name) # indy 객체 생성

access_point = [0.19149038537030902, -0.422956615409156, 0.10288759827567309, -90.87633933330643, 156.1061040242262, 90.4357163189986]
back_point = [0.19149038537030902, -0.422956615409156, 0.10288759827567309, -90.87633933330643, 156.1061040242262, 90.4357163189986]
pick_target_point = [0.09153768868657709, -0.42435503802724583, 0.10434673262086618, -90.86795881923283, 156.11225629570933, 90.43699590735689]
mid_point = [0.46806729562333677, -0.28629847885403414, 0.325565500738455, -1.452322719264416, -176.23226985273988, 110.36719764140626]
up = 0.15
down = -0.15

def target_pick(access, target , back) :
    indy.task_move_to(access)
    indy.wait_for_move_finish()
    indy.task_move_to(target)
    indy.wait_for_move_finish()
    indy.set_endtool_do(0, 0)
    time.sleep(1)
    indy.task_move_to(back)
    indy.wait_for_move_finish()

def target_release(access, target , back) :
    indy.task_move_by(access)
    indy.wait_for_move_finish()
    indy.task_move_by(target)
    indy.wait_for_move_finish()
    indy.set_endtool_do(0, 1)
    time.sleep(1)
    indy.task_move_by(back)
    indy.wait_for_move_finish()

def pallet(start_point, end_point):
    while True:
        num = int(input("도미노 개수 :"))
        i = 0
        interval_x = (end_point[0] - start_point[0])/num
        interval_y = (end_point[1] - start_point[1])/num
        while i < num:
            target_pick(access_point, pick_target_point, back_point)
            time.sleep(1)
            indy.task_move_to(start_point)
            indy.wait_for_move_finish()
            target_release([interval_x,interval_y,up,0,0,0], [0,0,down,0,0,0], [0,0,up,0,0,0])
            indy.wait_for_move_finish()
            i += 1