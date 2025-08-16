import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import time
import ollama
from gtts import gTTS
import pygame
import os
import json



recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 175)     # speaking speed
engine.setProperty('volume', 1)     # max volume
newsapi = "b0ccfcdd2e214949bc29d1c0534ed1ee"
recognizer.energy_threshold = 1500
recognizer.pause_threshold = 2.0
recognizer.dynamic_energy_threshold = True


def speak(text):
    print(f"Jarvis: {text}")
    
    try:
        tts = gTTS(text, lang='en')
        tts.save('temp.mp3')#Initialize pygame mixer
        
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")    # Load the MP3 file
        pygame.mixer.music.play()   # Play the MP3

        while pygame.mixer.music.get_busy():    # Keep the program running while music is playing
            pygame.time.Clock().tick(10)

        # pygame.mixer.music.stop()
        # pygame.mixer.quit()
        pygame.mixer.music.unload()
        #os.remove("temp.mp3")
    except Exception as e:
        print(f"Error in gtts/Pygame speak function: {e}")
        print('Falling back to pyttsx3')
        engine.say(text)
        engine.runAndWait()

# def talk(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')#Initialize pygame mixer
#     pygame.mixer.init()
#     pygame.mixer.music.load("temp.mp3")    # Load the MP3 file
#     pygame.mixer.music.play()   # Play the MP3

#     while pygame.mixer.music.get_busy():    # Keep the program running while music is playing
#         pygame.time.Clock().tick(10)
#     os.remove("temp.mp3")
def speak_news(articles):
    for idx, article in enumerate(articles, start=1):
        title = article.get('title', 'No title available')
        engine.say(title)
        speak(f"Headline {idx}: {title}")
        engine.runAndWait() # speak each headline immediately
        time.sleep(0.5) # pause between headlines

def ask_ollama(command):
    speak("Let me think about that.")
    try:
        response = ollama.chat(model='llama3', 
        messages=[{'role': 'user', 'content': "you are a virtual assistant named Jarvis skilled in general tasks like alexa and google cloud. Give Short responses please"},
                  {"role": "user", "content": command}])
        reply = (response['message']['content'])
        return reply
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "Sorry, I couldn't get a response from Ollama. Please check if it's running."


        


def get_microphone_index():
# """Checks for Realme Buds and returns their index, otherwise uses default."""
# Get a list of all available microphone names
    mic_list = sr.Microphone.list_microphone_names()    # Search for "realme buds" in the list of microphones
    for i, mic_name in enumerate(mic_list): # Check if the desired keywords are in the microphone name (case-insensitive)
        if "realme buds" in mic_name.lower():
            print(f"✅ Realme Buds connected and selected.")
            return i # Return the index of the found microphone
# This part runs only if the loop finishes without finding the mic
    print("⚠️  Realme Buds not found. Using system default microphone.")
    return None # 'None' tells the library to use the default mic



def processCommand(c):
    print(f"Processing command: '{c}'")
    if "open google" in c.lower():
        print("opening Google")
        webbrowser.open("https://google.com")
    elif "open meta" in c.lower():
        print("opening Facebook")
        webbrowser.open("https://meta.com")
    elif "open youtube" in c.lower():
        print("opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        print("opening linkedin")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        r = requests.get(url)
        if r.status_code==200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                speak_news(articles)
            else:
                speak("no articles found")
    else: 
        output = ask_ollama(c)
        speak(output)

#b0ccfcdd2e214949bc29d1c0534ed1ee

if __name__ == "__main__":
    speak("Initializing Jarvis......")
    mic_index = get_microphone_index()
    try:    # Use the microphone as a context manager
        with sr.Microphone(device_index=mic_index) as source:
     # --- KEY FIX: Calibrate for ambient noise ---

     # This is crucial for the recognizer to distinguish speech from noise
            print("\nCalibrating microphone... Please be quiet for a moment.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"Microphone calibrated. Energy threshold is now {recognizer.energy_threshold:.2f}")
            speak("Ready to assist you.")
        # Main listening loop

            while True:
                print("\nListening for the wake word 'Jarvis'...")
                try:
            # Listen for audio and store it
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Recognize the speech using Google's Web Speech API
                    word = recognizer.recognize_google(audio)
                    print(f"You said: '{word}'")
            # Check for the wake word
                    if "jarvis" in word.lower():
                        engine.say("Ya")
                        print("Wake word detected! Listening for your command...")  # Listen for the actual command after the wake word
                        audio_command = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio_command)
                        if command:processCommand(command)
                        else: speak("Yes? How can I help")


            # Check for the stop command

                    elif "stop" in word.lower() or "exit" in word.lower():
                        speak("Goodbye!")
                        break
                except sr.WaitTimeoutError: # This is normal, just means no speech was detected in the timeout period
                    pass
                except sr.UnknownValueError:    # This is for when the recognizer can't understand the audio
                    print("Sorry, I didn't catch that. Please try again.")
                except sr.RequestError as e:    # This is for when there's an issue with the API (e.g., no internet)
                    speak("Service is unavailable. Please check your internet connection.")
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    break

    except (IOError, AttributeError) as e:
        error_message = "Microphone not found or failed to initialize. Please check your microphone connection, drivers, and permissions."
        print(f"ERROR: {error_message}\nDetails: {e}")
        speak(error_message)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("A critical error has occurred. Shutting down.")
