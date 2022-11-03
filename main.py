import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from pydub import AudioSegment

fs = 44100
seconds = 3

print("Recording...")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write('output.wav', fs, myrecording)

print("-----Finished Recording-----")

sounds = AudioSegment.from_wav("output.wav")
sounds.export("output.mp3", format="mp3")

print("-----Converting Audio-----")

model = whisper.load_model('base')
result = model.transcribe('output.mp3')
print(result)

#Write the result to a text file

with open('result.txt', 'w') as f:
    f.write(result["text"])
