from asr import record_audio, checkMic, play_audio, speech_to_text, checkOutput
import os

#Check Audio Device

# checkMic()

# checkOutput()

# Record 

def message(text):
    os.system(f'espeak -v en+f2 -p 70 -s 120 "{text}"')

def record_and_play():
    message("Recording...")
    record_audio('test.wav')

    tts_audio = 'test.wav'

    if os.path.exists(tts_audio):
        speech_to_text(tts_audio)
    else:
        print("File does not exist")

record_and_play()