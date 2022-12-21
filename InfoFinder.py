import re
import time

from bs4 import BeautifulSoup
import requests
import Wiki
import Dictionary
import pyttsx3
import speech_recognition as sr
import multiprocessing
import Weather

# -  Text to speech  - #

engine = pyttsx3.init()  # Initalises the engine
r = sr.Recognizer()  # Sets up the recogniser


def Speak(words):  # Outputs whatever is passed
    engine.say(words)
    engine.runAndWait()


def Listen():
    with sr.Microphone() as source2:
        print("Speak")
        audio2 = r.listen(source2)  # Listens for input
        text = r.recognize_google(audio2)  # Recognises the words said and stores as text
        return (text)


# - Main Code - #

while True:
    Weather.weatherSearch()
    '''Speak("What would you like to search for?")
    try:
        term = Listen()
    except sr.UnknownValueError:
        Speak("I couldn't understand you, please type what you would like to search for")
        term = input("Search: ") '''
    #command = input("Input: ")  # User writes a command
    #wikiSucces = Wiki.wikiSearch(term)  # Stores whether wiki search was successful or not
    search = input("Dictionary Search: ")
    if not Dictionary.dictionarySearch(search):
        Wiki.wikiSearch(search)
    choice = "h"
    while choice != "y" and choice != "n":
        choice = input("Search for something else? (y/n) ").lower()
    if choice == "n":
        break

# Error made for keyword hit, look into that, something to do with new line removals