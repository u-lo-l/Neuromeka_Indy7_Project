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
    indy.task_move_to(access)
    indy.wait_for_move_finish()
    indy.task_move_to(target)
    indy.wait_for_move_finish()
    indy.set_endtool_do(0, 1)
    time.sleep(1)
    indy.task_move_to(back)
    indy.wait_for_move_finish()