# Audio to Text Conversion
CPSC 440 - Computer Systems Architecture <br>
Jerry Liu, Sean Del Castillo


## Introduction
This program listens to a microphone device, writes to wav, then utilizes OpenAI Whisper to convert the audio to text.

OpenAI Whisper is an automated speech recognition (ASR) system that was trained using 680,000 hours of supervised web-based multilingual and multitask data. In using a dataset of size and variety increases resilience against accents, background noise, and technical terminology. Additionally, it permits both translation into English from several languages as well as transcription in those languages. 

## Hardware Prerequisite
The hardware driver depends on the GPIOZero library (https://github.com/gpiozero/gpiozero). Hardware must support this library and have at least 11 GPIO pins. 

## Installation and Setup
To download all Python library modules:
```pip install -r requirements.txt```

The sounddevice library needs PortAudio which isn't bundled in on Linux:
```sudo apt install libportaudio2```

To install libav please see this page for general requrements and platform specific installation instructions:
https://wiki.libav.org/Platform

You might also need to install ffmpeg which is a open-source command-line tool for transcoding multimedia files.
```sudo apt install ffmpeg```

Make sure to create two subdirectories ./recordings, ./transcriptions to store file outputs.

## Getting Started
1. Start driver.py
```python3 driver.py```
2. Press and hold the recording_button to record
3. Release the button to start the transcription process
4. Recording .wavs are stored in /recordings and matching transcriptions are stored in /transcripts
5. Exit the program in listening state by KeyboardInterrupt

## LED Legend
```
[ ] Unlit [*] Blinking [X] Lit
     [ ] <- Recording LED
     [ ] <- Caution LED
     [ ] <- Graph LEDs
     [ ] <-/ /
     [ ] <--/
     [ ] <- Power LED
```

## LED Reporting
1. Listening
```
     [ ] <- Recording LED
     [ ] <- Caution LED
     [ ] <- Graph LEDs
     [ ] <-/ /
     [ ] <--/
     [X] <- Power LED
```

2. Recording
```
     [X] <- Recording LED
     [ ] <- Caution LED
     [ ] <- Graph LEDs
     [ ] <-/ /
     [ ] <--/
     [X] <- Power LED
```

3. Transcribing
```
     [*] <- Recording LED
     [*] <- Caution LED
     [ ] <- Graph LEDs
     [ ] <-/ /
     [ ] <--/
     [ ] <- Power LED
```

4. Graph LED states
```
     [ ] <- Recording LED
     [X] <- Caution LED
     [X] <- Graph LEDs
     [X] <-/ /
     [X] <--/
     [ ] <- Power LED
```
  - The three Graph LEDs are pulse wave modulated to 20 maximum values. They track 
    how many recordings are in /recordings. If all three LEDs are fully lit and 
    Caution is lit then that means the maximum amount of files are being tracked by 
    the graph LEDs. Recording and transcribing are unaffected by this max value.

## References
- https://cdn.openai.com/papers/whisper.pdf
- https://github.com/ggerganov/whisper.cpp
