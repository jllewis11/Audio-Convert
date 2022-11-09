from gpiozero import LED, Button
from time import time, sleep
from signal import pause
import sys
import datetime
import argparse

# LED PIN CONSTSANTS
LED_CONSTANTS = {
	"POWER_PIN": None,
	"REC_PIN": 17,
	"WARNING_PIN": None,
	"HAT_PIN": None,
	"SLOT1_PIN": None,
	"SLOT2_PIN": None,
	"SLOT3_PIN": None
}
# BUTTON PIN CONSTANTS
BUTTON_CONSTANTS = {
	"POWER_PIN": None,
	"REC_PIN": 4,
	"PAUSE_PIN": None,
	"MODE_PIN": None
}

HOLD_TIME = 3
IDEABOX_VERSION = '0.2 Alpha'

parser = argparse.ArgumentParser(description='Starts the IdeaBox Listener.')
parser.add_argument('-d', '--debug', dest='debug', help='prints debug information', action='store_true')
parser.add_argument('-v', '--version', action='version', version=f'IdeaBox %(prog)s {IDEABOX_VERSION}')
args = parser.parse_args()

power_led = LED(LED_CONSTANTS['POWER_PIN'])
recording_led = LED(LED_CONSTANTS['REC_PIN'])
warning_led = LED(LED_CONSTANTS['WARNING_PIN'])
hat_led = LED(LED_CONSTANTS['HAT_PIN'])
slot1_led = LED(LED_CONSTANTS['SLOT1_PIN'])
slot2_led = LED(LED_CONSTANTS['SLOT2_PIN'])
slot3_led = LED(LED_CONSTANTS['SLOT3_PIN'])

power_button = Button(BUTTON_CONSTANTS['POWER_PIN'])
recording_button = Button(BUTTON_CONSTANTS['REC_PIN'])
pause_button = Button(BUTTON_CONSTANTS['PAUSE_PIN'])
mode_button = Button(BUTTON_CONSTANTS['MODE_PIN'])

now = datetime.datetime.now()

def recording():
	recording_button.when_pressed = None
	recording_button.wait_for_release()

	recording_led.on()

	# TODO Start Recording

	sleep(0.15)

	if args.debug:
		print('Device is recording...')
		start = time()

	recording_button.hold_time = 3
	if recording_button.is_held:
		if args.debug:
			print('Recording paused~')

	recording_button.wait_for_release()

	recording_led.off()

	if args.debug:
		end = time()
		recording_time = end-start
		print(f'Recording complete! {round(recording_time, 2)}s')

	# TODO End recording

	listen()

# TODO Functionality to pause current recording and return to recording context
def pause_recording():
	pass

# TODO Functionality to enter edit mode and enter new context
def edit_mode():
	pass

# TODO Functionality to make driver wait in listen context, waiting for recording or mode switch
def listen():
	recording_button.when_pressed = recording

	pause()

print(f'IdeaBox v{IDEABOX_VERSION} Listening... {now}')
if args.debug:
	print('Debug information printing...')
	print(f'LED PINS: {LED_CONSTANTS}')
	print(f'BUTTON PINS: {BUTTON_CONSTANTS}')

listen()
