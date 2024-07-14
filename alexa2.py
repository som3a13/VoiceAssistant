import webbrowser
from time import ctime
import os
import playsound
from gtts import gTTS
import speech_recognition as sr
import pywhatkit
import wikipedia
import pyjokes

recognize = sr.Recognizer()

def speak(txt):
    tts = gTTS(text = txt, lang = 'en', slow = True)
    audiofile = 'audio.mp3'
    tts.save(audiofile)
    playsound.playsound(audiofile)
    os.remove(audiofile)
recognize.energy_threshold = 3000 
def record(order = False):
    with sr.Microphone(device_index=11) as source:
        recognize.adjust_for_ambient_noise(source)
        if order:
            speak(order)
        audio = recognize.listen(source)
        request = ''
        try:
            request = recognize.recognize_google(audio, language = 'en')
        except sr.UnknownValueError:
            speak("sorry i did not get that")
        except sr.RequestError:
            speak("sorry Service is Down")
        return request.lower()

def respond():
    user_request = record()
    if 'alexa' in user_request:
        user_request = user_request.replace('alexa', '')
    elif 'name' in user_request:
        speak("Hello, it's alexa")
    elif 'time' in user_request:
        speak(ctime())
    elif 'search' in user_request:
        search = record('What do you want to google?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
    elif 'location' in user_request:
        location = record('What is the location do you want?')
        url = 'https://google.nl/maps/place/' + location + '/&amp'
        webbrowser.get().open(url)
    elif 'bye' in user_request:
        speak('bye')
        exit()
    elif 'music' in user_request:
        song = record('What song do you want to listen?')
        pywhatkit.playonyt(song)
    elif 'wikipedia' in user_request:
        wiki = record('What do you want to search on wikipedia?')
        info = wikipedia.summary(wiki,1)
        speak(info)
    elif 'joke' in user_request:
        speak(pyjokes.get_joke())
    else:
        speak('Please say the request again')

speak('How can I help you?')
while 1:
    respond()
        
