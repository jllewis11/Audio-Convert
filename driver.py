from gpiozero import LED, LEDBarGraph, Button
from time import time, sleep
from signal import pause
import sys
import datetime
import argparse
import os
import random
import numpy

#Recording library
import sounddevice as sd
import subprocess
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
IDEABOX_VERSION = '1.0 Release'

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
	recording_led.on()

	device_info = sd.query_devices(kind='input')
    # soundfile expects an int, sounddevice provides a float:
	#16KHz sampling rate is only accepted in the whisper.cpp program
	samplerate = int(16000)

	filename = tempfile.mktemp(prefix='recording-', suffix='.wav', dir='')

    # Make sure the file is opened before recording anything:
	with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=1) as file:
		with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
			print('Recording...')
			while recording_button.is_pressed:
				file.write(q.get())

	print('\nRecording finished: ' + repr(filename))
	sd.wait(0)

	power_led.off()
	recording_led.blink()
	caution_led.blink()

	subprocess.run("./whisper.cpp/main -m ./whisper.cpp/models/ggml-base.en.bin -nt -otxt -f " + filename, shell=True)
	print('Transcription done.')
	recording_led.off()
	caution_led.off()
	sleep(0.25)
	led_startup_sequence()

	# move recording to subdir
	subprocess.run('mv recording-*.wav ./recordings', shell=True)

	# move transcript to subdir
	subprocess.run('mv recording-*.wav.txt ./transcripts', shell=True)

	update_graph(check_files())
	power_led.on()

	listen()

def led_startup_sequence():
	recording_led.on()
	sleep(0.2)
	caution_led.on()
	sleep(0.2)
	for i in range(100):
		graph_leds.value = i/100
		sleep(0.005)
	sleep(1)
	recording_led.off()
	caution_led.off()
	graph_leds.off()

	return

def check_files():
	count = 0
	dir_path = '/home/pi/cpsc440-project-ideabox/recordings'
	for path in os.scandir(dir_path):
		if path.is_file():
			count += 1

	if args.debug:
		print(f'{count} files in dir {dir_path}')

	return count

def update_graph(count):
	if count > 20:
		graph_leds.value = 20/20
		caution_led.on()
	else:
		caution_led.off()
		graph_leds.value = count/20

	return

def input_init():
	print(f'IdeaBox v{IDEABOX_VERSION} {now}')
	power_led.on()

	led_startup_sequence()
	sleep(0.5)

	update_graph(check_files())

	if args.debug:
		print('Debug information printing')
		print(f'LED PINS: {LED_CONSTANTS}')
		print(f'BUTTON PINS: {BUTTON_CONSTANTS}')

	return

def listen():
	print('Listening...')
	try:
		while True:
			if recording_button.is_pressed:
				start_recording()
	except KeyboardInterrupt:
		led_startup_sequence()
		print('\nQuitting Ideabox.')
		quit()
input_init()
listen()
