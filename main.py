import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import aiml
import os
import requests
import json
import pyttsx3

import presidencyRelatedAi as pai
from offline_ai import TextToResponseChatbot

from moving.esp32_websocket_client import RobotUDPClient
import asyncio

#esp32_ip = "192.168.137.111" # it may change

def update_expression_ai(new_expression):
    try:
        with open('expression.txt', 'w') as file:
            file.write(new_expression)
        print("Expression updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def sendData(data):
    response = robot_client.send_data(data)

    if response:
        print("Response from ESP32:", response)
    else:
        print("Failed to receive response from ESP32. Exiting...")

# Initialize recognizer
recognizer = sr.Recognizer()

# Chatbot class
class Chatbot:
    def __init__(self):
        print("""Hi! This is Sukarna Jana, the creator of this code.
Its a offline Mode which was trained long back.
Thank you!
================= Happy Chatting =================""")
        
        self.kernel = aiml.Kernel()
        self.kernel.learn("std-startup.xml")
        self.kernel.respond("LOAD AIML B")

    def get_response(self, input_text):
        """
        Get response based on the input text.
        
        Parameters:
        - input_text (str): The input text.
        
        Returns:
        - str: The response from the chatbot.
        """
        return self.kernel.respond(input_text)

''' # This Runs using Internet
# Function to convert text to speech and play it with the specified gender
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("response.mp3")
    
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    # Stop the mixer and clean up
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    os.remove("response.mp3")
'''
def speak(text):
    engine = pyttsx3.init()
    
    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 1)  # Volume 0-1

    # Get available voices
    voices = engine.getProperty('voices')
    
    # Set the voice to male
    for voice in voices:
        if 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
# Function to listen for the hotword "Candy"
def listen_for_hotword():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for hotword 'prism'...")
        update_expression_ai("Listening")
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {text}")
            if "prism" in text:
                return True
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return False

def ask_question(question):
    url = "http://localhost:5000/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"input_text": question}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            # Concatenate the response chunks into a single paragraph
            concatenated_response = ' '.join(data.get('response', []))
            return concatenated_response
    except requests.exceptions.ConnectionError:
        return "Sorry, can't connect to the internet. Please check your connection."
    return None

# Function to get user input and respond using the AI chatbot
def ai_conversation(chatbot):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("You can speak now...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            #update_expression_ai("Saying")
            #await sendData("t") #talking
            # Try to get response from Gemini chatbot
            gemini_response = ask_question(user_input)
            if gemini_response is not None:
                if(gemini_response=="Sorry, can't connect to the internet. Please check your connection."):
                    #print(f"Gemini: {gemini_response}")
                    offline_response = chatbot2.get_response_from_text(user_input)
                    print(f"Offline Robot: {offline_response}")
                    update_expression_ai("Saying")
                    sendData("t") #talking
                    speak(offline_response)
                    pass
                else:
                    print(f"Gemini: {gemini_response}")
                    update_expression_ai("Saying")
                    sendData("t") #talking
                    speak(gemini_response)
            else:
                # If Gemini fails, fallback to offline robot
                offline_response = chatbot2.get_response_from_text(user_input)
                print(f"Offline Robot: {offline_response}")
                update_expression_ai("Saying")
                sendData("t") #talking
                speak(offline_response)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was an error with the speech recognition service.")

# Main loop to listen for hotword and trigger AI conversation
def main():
    
    while True:
        if listen_for_hotword():
            ai_conversation(chatbot)
            sendData("s")  # stop
            print("Returning to hotword listening mode...")
            time.sleep(2)  # Pause briefly before listening again

if __name__ == "__main__":
    esp32_ip = input("Enter the IP address of your ESP32: ")
    print(f"IP Address of Robot Locomotion Controller : {esp32_ip}")
    robot_client = RobotUDPClient(esp32_ip)
    update_expression_ai("starting")
    chatbot = Chatbot()
    chatbot2 = TextToResponseChatbot()
    main()
