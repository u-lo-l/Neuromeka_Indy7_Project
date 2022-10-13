from indy_utils import indydcp_client as client

def wait_for_button_input(indy) :
	old = indy.get_di()[0:3]
	while (True) :
		new = indy.get_di()[0:3]
		if (new is not old) :
			break
		old = new
	if (new[0] == 1):
		return (1)
	if (new[1] == 1):
		return (2)
	if (new[2] == 1):
		return (3)