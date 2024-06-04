import pygame
import time
import sys
import os

# Add the other folder to sys.path
other_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../moving'))
sys.path.append(other_folder_path)

from esp32_websocket_client import RobotUDPClient

# Initialize the mixer module
pygame.mixer.init()

# Define the paths to the audio files
audio_files = {
    '1': 'whatHappen.mp3',
    '2': 'whyimp.mp3',
    '3': 'safe_demo_mode.mp3',
    '4': 'intro.mp3'
}

def play_audio(file_path):
    sendData("t") #talking
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
        time.sleep(1)
    sendData("s")  # stop

def sendData(data):
    response = robot_client.send_data(data)

    if response:
        print("Response from ESP32:", response)
    else:
        print("Failed to receive response from ESP32. Exiting...")

if __name__ == "__main__":
    ip = input("Enter IP: ")
    robot_client = RobotUDPClient(ip)
    while True:
        question = input("""
Choose the Question You want to say Okay?
[1] What is happening today in Presidency University today
[2] Why this day is Important today
[3] (SAY: I am running in Safe Demo Mode So, my Internal AI is OFF)
[4] INTRO
Enter your choice (1-4): """)

        if question in audio_files:
            play_audio(audio_files[question])
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
