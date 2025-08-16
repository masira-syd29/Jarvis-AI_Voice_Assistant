# import webbrowser
# import pyttsx3
# import musicLibrary
# import requests
# import time
# import ollama
# import json


# # pip install pocketsphinx

# recognizer = sr.Recognizer()
# newsapi = "b0ccfcdd2e214949bc29d1c0534ed1ee"
# recognizer.energy_threshold = 1500
# recognizer.pause_threshold = 2.0
# recognizer.dynamic_energy_threshold = True


# def speak(text):
#     print(f"Jarvis: {text}")
#     temp_engine = pyttsx3.init()
#     temp_engine.setProperty('rate', 175)
#     temp_engine.setProperty('volume', 1)
    
#     voices = temp_engine.getProperty('voices')
#     if voices:
#         temp_engine.setProperty('voice', voices[0].id)
#     else:
#         print("No voices found! Text-to-speech may not work.")
#         return # Exit if no voice is available

#     temp_engine.say(text)
#     temp_engine.runAndWait()
#     temp_engine.stop() # Crucial to stop and free up resources

# def speak_news(articles):
#     all_headlines = "Here are the top headlines. "
#     for idx, article in enumerate(articles, start=1):
#         title = article.get('title', 'No title available')
#         all_headlines += f"Headline {idx}: {title}. "
#     speak(all_headlines)
# def aiProcess(command):
#     url = "http://localhost:11434/api/chat"
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "model": "llama3:8b",
#         "messages": [
#             {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. Give short responses please."},
#             {"role": "user", "content": command}
#         ],
#         "stream": False
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         response.raise_for_status()
#         data = response.json()
#         return data["message"]["content"]
#     except requests.exceptions.RequestException as e:
#         print(f"Error connecting to Ollama: {e}")
#         return "I'm sorry, I can't connect to my AI brain right now. Please check if Ollama is running."


# def get_microphone_index():
#     """Checks for Realme Buds and returns their index, otherwise uses default."""
#     mic_list = sr.Microphone.list_microphone_names()    # Get a list of all available microphone names
#     for i, mic_name in enumerate(mic_list): # Search for "realme buds" in the list of microphones
#         if "realme buds" in mic_name.lower():   # Check if the desired keywords are in the microphone name (case-insensitive)
#             print(f"✅ Realme Buds connected and selected.")
#             return i # Return the index of the found microphone
#     print("⚠️  Realme Buds not found. Using system default microphone.")    # This part runs only if the loop finishes without finding the mic
#     return None # 'None' tells the library to use the default mic

# def processCommand(c):
#     print(f"Processing command: '{c}'")
#     if "open google" in c.lower():
#         speak("opening Google")
#         webbrowser.open("https://google.com")
#     elif "open meta" in c.lower():
#         speak("opening Facebook")
#         webbrowser.open("https://meta.com")
#     elif "open youtube" in c.lower():
#         speak("opening Youtube")
#         webbrowser.open("https://youtube.com")
#     elif "open linkedin" in c.lower():
#         speak("opening linkedin")
#         webbrowser.open("https://linkedin.com")
#     elif c.lower().startswith("play"):
#         try:
#             song = c.lower().split(" ", 1)[1]
#             link = musicLibrary.music[song]
#             speak(f"Playing {song}")
#             webbrowser.open(link)
#         except (IndexError, KeyError):
#             speak("Sorry, I couldn't find that song in your music library.")
#     elif "news" in c.lower():
#         speak("Fetching the top headlines.")
#         url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
#         try:
#             r = requests.get(url)
#             r.raise_for_status()
#             data = r.json()
#             articles = data.get('articles', [])
#             if articles:
#                 speak_news(articles)
#             else:
#                 speak("No articles found at this time.")
#         except requests.exceptions.RequestException as e:
#             speak("I am unable to fetch the news right now. Please check your internet connection.")
#             print(f"Error fetching news: {e}")
#     else: 
#         speak("Let me think about that.")
#         output = aiProcess(c)
#         speak(output)
        
  
# #b0ccfcdd2e214949bc29d1c0534ed1ee
# if __name__ == "__main__":
#     speak("Initializing Jarvis......")
#     mic_index = get_microphone_index()


    
#     try:
#         # Use the microphone as a context manager
#         with sr.Microphone(device_index=mic_index) as source:
#             # --- KEY FIX: Calibrate for ambient noise ---
#             # This is crucial for the recognizer to distinguish speech from noise
#             print("\nCalibrating microphone... Please be quiet for a moment.")
#             recognizer.adjust_for_ambient_noise(source, duration=2)
#             print(f"Microphone calibrated. Energy threshold is now {recognizer.energy_threshold:.2f}")
#             speak("Ready to assist you.")

#             # Main listening loop
#             while True:
#                 print("\nListening for the wake word 'Jarvis'...")
#                 try:
#                     # Listen for audio and store it
#                     audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    
#                     # Recognize the speech using Google's Web Speech API
#                     word = recognizer.recognize_google(audio)
#                     print(f"You said: '{word}'")

#                     # Check for the wake word
#                     if "jarvis" in word.lower():
#                         speak("Yes?")
#                         print("Wake word detected! Listening for your command...")
                        
#                         # Listen for the actual command after the wake word
#                         audio_command = recognizer.listen(source, timeout=10, phrase_time_limit=5)
#                         command = recognizer.recognize_google(audio_command) 
#                         if command:processCommand(command)
#                         else: speak("Yes? How cam I help")

#                     # Check for the stop command
#                     elif "stop" in word.lower() or "exit" in word.lower():
#                         speak("Goodbye!")
#                         break

#                 except sr.WaitTimeoutError:
#                     # This is normal, just means no speech was detected in the timeout period
#                     pass
#                 except sr.UnknownValueError:
#                     # This is for when the recognizer can't understand the audio
#                     print("Sorry, I didn't catch that. Please try again.")
#                 except sr.RequestError as e:
#                     # This is for when there's an issue with the API (e.g., no internet)
#                     speak("Service is unavailable. Please check your internet connection.")
#                     print(f"Could not request results from Google Speech Recognition service; {e}")
#                     break
#     except (IOError, AttributeError) as e:
#         error_message = "Microphone not found or failed to initialize. Please check your microphone connection, drivers, and permissions."
#         print(f"ERROR: {error_message}\nDetails: {e}")
#         speak(error_message)
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         speak("A critical error has occurred. Shutting down.")

    
    # #Listen to the wake word Jarvis
    # #obtain audio from the microphone
    # while True:
    #     r = sr.Recognizer()
    #     # recognize speech using google
    #     print("Recognizing...")
    #     mic_index = get_microphone_index()
    #     try:
    #         with sr.Microphone(device_index=mic_index) as source:
    #             print("Listening!......")
    #             audio = r.listen(source, timeout=5, phrase_time_limit=5)
    #         word = r.recognize_google(audio)
            
            
    #         if(word.lower() == "jarvis"):
    #             speak("Ya I am Here")
    #             #listen for command
    #             with sr.Microphone(device_index=mic_index) as source:
    #                 print("Jarvis is Active!......")
    #                 audio = r.listen(source, timeout=5, phrase_time_limit=5)   
    #                 command = r.recognize_google(audio)
    #                 processCommand(command)

    #         elif word.lower() == "stop":
    #             speak("Goodbye!")
    #             break
    #     except AttributeError:
    #         print("Microphone stream failed to initialize. Retrying...")
    #         continue
    #     except sr.UnknownValueError:
    #         print("Sorry, I didn't understand that.")
    #     except sr.RequestError as e:
    #         print(f"Could not request results; {e}")
    #     except Exception as e:
    #         print("error {0}".format(e))

    # Extract only the titles into a list
            # titles = [article['title'] for article in data.get('articles', [])]
            # for title in titles:    
            #     speak(title)

    # elif "news" in c.lower():
    #     url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
    #     r = requests.get(url)
        
    #     if r.status_code==200:
            
    #         data = r.json()

    #         articles = data.get('articles', [])

    #         if articles:
    #             speak("Here are the top headlines")
    #             speak_news(articles)
    #         else:
    #             speak("no articles found")

        # for article in articles:    
            #     speak(article['title'])
        # for article in articles:
                #     title = article.get('title', 'No title available')
                #     speak(title)

    # def speak_news(articles):
#     # This loop will call the 'speak' function for each article title.
#     # The 'speak' function already handles the 'engine.runAndWait()'.
#     for idx, article in enumerate(articles, start=1):
#         title = article.get('title', 'No title available')
#         speak(f"Headline {idx}: {title}")
#         time.sleep(1)

