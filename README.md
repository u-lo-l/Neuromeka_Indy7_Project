# Neuromeka_Indy7_Project
2022 Seoul Robot Academy Project with Neuromeka Indy7 (Making Jenga Domino)

# JengaDomino

- ***step0 : 상수 정의***
    
    젠가를 놓기 위한 tool의 높이 : TOOL_PLACE_HEIGHT = 0.1095
    
    젠가 간의 간격 : STRIDE = 0.04
    
    PICK 동작 수행하기 위한 접근지점, 목표지점, 후퇴지점 티칭 후 설정
    
    PICK_ACCESS, PICK_BACK, PICK_TARGET
    
    PLACE 동작 수행하기 위한 오프셋 설정 : PLACE_OFFSET = 0.15
    
- ***step1 : 시작***
    
    indy_client이용하여 indy 객체 생성 후. connect
    
    LED 2회 점멸 후 LED 켬
    
- ***step2 : 경유점 설정***
    - 로봇을 직접 움직여 원하는 지점에 위치시킨 후, 파란 버튼(digital_input_0)을 누른다.
        - get_task_pos()를 통해 얻은 위치정보에서의 z값을 TOOL_PLACE_HEIGHT로 수정한다.
        - get_task_pos()를 통해 얻은 위치정보에서의 [rpy](https://blog.naver.com/milkysc/221754450137)값을 0,180,0으로 수정한다.
            - 0,+-180,0  혹은 +-180,0,0으로 수정해도 된다.
    - 위의 과정을 2회 반복한다.
- ***step3 : 경로 생성***
    - start point와 end_point를 빼면 직선의 길이를 구할 수 있고, STRIDE로 나누면 몇 개의 젠가가 사용될 지 구할 수 있다.
    - [starat_point, end_point] 범위에서 STRIDE간격으로 점들을 새로운 리스트에 저장하여 반환한다.
- ***step4 : pick***
    - step 0에서 설정한 위치 정보를 이용하여 젠가를 잡는다.
- ***step5 : place***
    - place하기 위한 접근위치를 구하고 그 위치로 이동시킨다..
        - 경로 상의 모든  position들은 rpy가 (0, 180, 0) 이기 때문에  end_effector의 z 축은 base의 z 과 방향이 반대고,  end_effector의 y축은 base의 y축과 방향이 같다.
        - tool은 end_effector와 z축은 방향이 같지만, z축방향으로 +22.5(deg) 회전한 좌표계를갖는다.
            - 지금 indy7이 회전을 쿼터니언으로 나타내지 않고 rpy로 나타내고 있는데, 이 때 [ZYX_Euler_angle](https://edward0im.github.io/engineering/2019/11/12/euler-angle/)을 사용한다는 보장이 없으므로, 이 단계에서 tool 좌표계와 end_effector의 좌표계를 일치시켜준다.  joint6를 -22.5(deg)만큼 회전시켜주면 좌표계가 일치하게 된다.
        - tool의 y축을 도미노 경로 진행방향과 일치시켜준다.
            - 도미노 진행 방향을 구한다.
                - 현재 점, 이전 점, 다음 점을 이용하여 진행방향을 구한다.
                    - 이전 점, 혹은 다음점이 없으면 현재점과 다음점 혹은 이전점으로 방향을 구하고
                    - 이전 점과 다음 점이 모두 있으면 다음점 - 이전점으로 방향을 구한다.
            - 도미노의 진행 방향과 (0,1,0)(Base의 y축)이 이루는 각을 내적과 acos을 이용하여 구한다.
            - 위에서 구해진 각 만큼 현재 joint6의 값을 증가시킬 것이다.
                - 갱신되는 joint6의 각이 [-215, 215]의 범위에 존재할 수 있도록 조정해준다.
            - 갱신된 joint_angle로 indy7을 이동시켜준다.
    - 접근 위치가 새롭게 갱신되었다.
        - 현재의 위치를 접근위치로, 목표 위치를 재설정한다.
            - 현재 위치에서 PLACE_OFFSET만큼 뺀 위치가 새 목표 위치이다.
    - 젠가를 내려놓은 후 접근 위치로 다시 올라와서  PLACE 동작을 끝낸다.
    - 위의 과정을 count - 1 만큼 반복한다. (count는 생성된 총 경유점의 개수이다.)
- ***step6 : play***
    - 경로의 마지막에 저장된 점으로 이동한다.
    - 그 상태에서 마지막 젠가의 위치로 툴을 이동시켜 도미노를 넘어뜨린다.
- ***step7 : 끝***
    
    LED 끄고 disconnect()한다.
