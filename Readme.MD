# Audio to Text Conversion
CPSC 440 - Computer Systems Architecture <br>
Jerry Liu - Sean Del Castillo


## Introduction
This program listens to a microphone device and converts the file from a WAV to MP3. Then, the program will utilize OpenAI Whisper to convert the audio to text. This program is built specific for Raspberry Pi, but can be converted. 

## Installation
To download all Python library modules:
```pip install -r requirements.txt```

To install libav please see this page for general requrements and platform specific installation instructions:
https://wiki.libav.org/Platform

## Getting Started
1. Run ```python main.py```
2. Wait for recording before speaking
3. The recording will be 3 seconds before it stop and starts to convert. 
4. The results will be printed in a results.txt file
