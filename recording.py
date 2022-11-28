import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import subprocess
from pydub import AudioSegment
import queue
import tempfile
import sys
import soundfile as sf
import os


q = queue.Queue()
filename = None
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

try:
    
    device_info = sd.query_devices(kind='input')
        # soundfile expects an int, sounddevice provides a float:
    samplerate = int(16000)
    
    filename = tempfile.mktemp(prefix='recording_',
                                        suffix='.wav', dir='')

    # Make sure the file is opened before recording anything:
    print("Starting....")
    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                      channels=1) as file:
        with sd.InputStream(samplerate=samplerate,
                            channels=1, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(filename))
    



sd.wait()
#write('output.wav', fs, myrecording)

print("-----Finished Recording-----")

#sounds = AudioSegment.from_wav(filename)
#sounds.export("output.mp3", format="mp3")

print("-----Converting Audio-----")

isCPP = True
if isCPP:
    subprocess.run("cd whisper.cpp && ./main -nt -otxt -f " + filename, shell=True)

else:

    model = whisper.load_model('base')
    result = model.transcribe(filename)
    print(result)

#Write the result to a text file
    with open('result.txt', 'w') as f:
        f.write(result["text"])


#Execute the whisper cpp program

