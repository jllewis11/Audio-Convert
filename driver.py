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

recording_led = LED(LED_CONSTANTS['REC_PIN'])
recording_button = Button(BUTTON_CONSTANTS['REC_PIN'])
now = datetime.datetime.now()

def start_recording():
	recording_button.when_pressed = None
	recording_led.on()
	# TODO Start Recording

	sleep(0.15)

	if args.debug:
		print('Device is recording... ')
		start = time()
		while True:
			if recording_button.is_pressed:
				end_recording(start)
				break
	else:
		while True:
			if recording_button.is_pressed:
				end_recording()
				break

def end_recording(start=None):
	recording_led.off()
	# TODO End Recording

	if args.debug:
		end = time()
		recording_length = end-start
		print(f'Recording Stopped!\nLength: {recording_length}s')

	recording_button.when_pressed = start_recording

	return

print(f'IdeaBox v{IDEABOX_VERSION} Listening... {now}')
if args.debug:
	print('Debug information printing...')
	print(f'LED PINS: {LED_CONSTANTS}')
	print(f'BUTTON PINS: {BUTTON_CONSTANTS}')

recording_button.when_pressed = start_recording

pause()
