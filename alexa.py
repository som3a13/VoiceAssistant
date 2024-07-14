import webbrowser
from time import ctime
import os
import playsound
from gtts import gTTS
import speech_recognition as sr
import pywhatkit
import wikipedia
import pyjokes

def speak(txt):
    tts = gTTS(text=txt, lang='en', slow=False)
    audiofile = os.path.join(os.path.dirname(__file__), 'audio.mp3')
    tts.save(audiofile)
    playsound.playsound(audiofile)
    os.remove(audiofile)

def record(order=False, timeout=None):
    # Initialize the recognizer
    if order:
        speak(order)
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=timeout)  # Record audio with the specified timeout

    print("Recognizing")

    try:
        # Recognize the audio using Google Web Speech API
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Didn't capture any voice. Please try again.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error connecting to the Google Web Speech API: {e}")



def respond():
    while True:
        user_request = record()
        print(user_request)
        if user_request is None:
            continue  # Continue listening until user provides valid input

        if 'alexa' in user_request:
            user_request = user_request.replace('alexa', '')

        elif 'name' in user_request:
            speak("Hello, it's Alexa")
        elif 'time' in user_request:
            speak(ctime())   
        elif 'search' in user_request:
            while True:
                speak('What do you want to Google?')
                search = record(timeout=5)  # Set a timeout for search input (e.g., 10 seconds)
                print(search)
                if search is None:
                    speak("Sorry, I didn't hear what you want to search. Please try again.")
                    continue  # Continue asking for search input
                else:
                    url = 'https://google.com/search?q=' + search
                    webbrowser.get().open(url)
                    break  # Exit the search loop and proceed with other requests
        elif 'joke' in user_request:
            joke = pyjokes.get_joke()
            speak(joke)
        elif 'bye' in user_request:
            speak('Goodbye!')
            exit()

speak('How can I help you?')
while True:
    respond()


