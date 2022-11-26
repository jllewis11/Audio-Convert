from gpiozero import LED, LEDBarGraph, Button
from time import time, sleep
from signal import pause
import sys
import datetime
import argparse
import os
import random

#Recording library
import sounddevice as sd
import whisper
import queue
import tempfile
import soundfile as sf

# LED PIN CONSTSANTS
LED_CONSTANTS = {
	"POWER_PIN": 10,
	"REC_PIN": 9,
	"CAUTION_PIN": 11,
	"HAT_PIN": None,
	"LED1_PIN": 17,
	"LED2_PIN": 27,
	"LED3_PIN": 22
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
power_led = LED(LED_CONSTANTS['POWER_PIN'])
caution_led = LED(LED_CONSTANTS['CAUTION_PIN'])
recording_button = Button(BUTTON_CONSTANTS['REC_PIN'])
graph_leds = LEDBarGraph(LED_CONSTANTS['LED1_PIN'], LED_CONSTANTS['LED2_PIN'], LED_CONSTANTS['LED3_PIN'], pwm = True)
now = datetime.datetime.now()

q = queue.Queue()
filename = None

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def start_recording():
	recording_button.when_pressed = None
	recording_led.on()

	device_info = sd.query_devices(kind='input')
    # soundfile expects an int, sounddevice provides a float:
	samplerate = int(device_info['default_samplerate'])
    
	filename = tempfile.mktemp(prefix='recording-',
                                        suffix='.wav', dir='')

    # Make sure the file is opened before recording anything:
	print("Starting....")

	with sf.SoundFile(filename, mode='x', samplerate=samplerate,
						channels=1) as file:
		with sd.InputStream(samplerate=samplerate,
								channels=1, callback=callback):
			print('#' * 80)
			print('Recording...')
			print('#' * 80)
			while recording_button.is_pressed:
				file.write(q.get())
	
	print('\nRecording finished: ' + repr(filename))
	print("-----Finished Recording-----")
	sd.wait(0)
	# Need to sleep to let user unpress button or else will fall into end_recording instantly
	sleep(0.25)

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

	return

def end_recording(start=None):
	recording_led.off()

	model = whisper.load_model('base')
	result = model.transcribe(filename)
	print(result)

	#Write the result to a text file
	######TODO change file name if needed
	with open('result.txt', 'w') as f:
		f.write(result["text"])

	if args.debug:
		end = time()
		recording_length = end-start
		print(f'Recording Stopped!\nLength: {round(recording_length, 2)}s')

	recording_button.when_pressed = start_recording

	# Debug functionality to make a file in /recordings to test update_graph()
	randnum = random.random()
	fp = open(f'/home/pi/Documents/CPSC-440-Project/recordings/recording-{randnum}', 'w')
	fp.close()
	# End Debug

	update_graph(check_files())

	return

def led_startup_sequence():
	recording_led.on()
	sleep(0.2)
	caution_led.on()
	sleep(0.2)
	for i in range(100):
		graph_leds.value = i/100
		sleep(0.005)
	sleep(0.5)
	recording_led.off()
	caution_led.off()
	graph_leds.off()

	return

def check_files():
	count = 0
	dir_path = '/home/pi/Documents/CPSC-440-Project/recordings'
	for path in os.scandir(dir_path):
		if path.is_file():
			count += 1

	if args.debug:
		print(f'{count} files in dir {dir_path}')

	return count

def update_graph(count):
	graph_leds.value = count/20

	return

print(f'IdeaBox v{IDEABOX_VERSION} Listening {now}')
power_led.on()

led_startup_sequence()
sleep(1)

update_graph(check_files())

if args.debug:
	print('Debug information printing')
	print(f'LED PINS: {LED_CONSTANTS}')
	print(f'BUTTON PINS: {BUTTON_CONSTANTS}')

recording_button.when_pressed = start_recording

pause()
