from indy_utils import indydcp_client as client
from time import sleep

LED_PIN = 10
LED_ON = 1
LED_OFF = 0

def led_on(indy) :
	indy.set_do(LED_PIN, LED_ON)

def led_off(indy):
	indy.set_do(LED_PIN, LED_OFF)

def led_blink(indy, count = 3):
	led_state = indy.get_do()[LED_PIN]
	for i in range(0, count) :
		led_state ^= 1
		indy.set_do(LED_PIN, led_state)
		sleep(0.05)
		led_state ^= 1
		indy.set_do(LED_PIN, led_state)
		sleep(0.05)
