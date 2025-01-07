
import pyaudio
import wave
import os

from pydub import AudioSegment
from pydub.playback import play


import speech_recognition as sr
from gtts import gTTS

from model import transcribe_audio


# Check device

pa = pyaudio.PyAudio()
language = "en"

def checkOutput():
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']} - Max Output Channels: {device_info['maxOutputChannels']}")
    pa.terminate()

def checkMic():

    print("Available Devices:")
    for device in range(pa.get_device_count()):

        device_info = pa.get_device_info_by_index(device)

        print(f"Device {device}: {device_info['name']}")
        print(f"Device Info: {device_info['defaultSampleRate']}")

        if device_info['maxInputChannels'] > 0:
            print(f"  --> This device supports input (microphone)")

    pa.terminate()

def record_audio(output_filename):
    device_index = 1
    # chunks = 1024
    chunks = 5120
    duration = 5
    rate = 48000
    channels=1
    format=pyaudio.paInt16

    stream = pa.open(
        rate=rate,
        channels=channels,
        format=format,
        input=True,   
        input_device_index=device_index,
        frames_per_buffer=chunks
    )

    print("recording...")
    frames = []

    for i in range(0, int(rate / chunks * duration)):
                data = stream.read(chunks)
                frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        

    print(f"Recording saved to {output_filename}.")
 
def play_audio(filename):
    audio = AudioSegment.from_file(filename)
    print("Playing Audio")
    play(audio)


def speech_to_text(file_name):   
    try:
        text = transcribe_audio(file_name)
        text = text[0]
        
        print(f"Transcription: {text}")
        os.system(f'espeak -v en+f2 -p 70 -s 120 "{text}"')
      
    except sr.UnknownValueError:
        print("Could not transcript")
    except sr.RequestError as e:
         print(f"Request Error: {e}")
    


