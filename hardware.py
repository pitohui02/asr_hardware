from gpiozero import Button
from asr import record_audio, checkMic, play_audio, speech_to_text, checkOutput
import os
import time
import subprocess

button = Button(16)

def message(text):
    os.system(f'espeak -v en+f2 -p 70 -s 120 "{text}"')

message("Device Booted")

def button_press():
    last_button_state = False
    try:
        while True:
            if button.is_pressed and not last_button_state:
                message("Device is ready")
                subprocess.run(["python3", "/home/pi/Desktop/asr-model/main.py"], check=True)
                last_button_state = True  
            elif not button.is_pressed and last_button_state:
                last_button_state = False
                message("Device is not ready")
           
            time.sleep(0.5)  

    except KeyboardInterrupt:
        # Cleanup and shutdown
        button.close()
        message("Device shutdown")
        print("Program Interrupted")

button_press()
