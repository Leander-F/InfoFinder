import speech_recognition as sr
import pyttsx3
import time
import multiprocessing
import keyboard


engine = pyttsx3.init()  # Initalises the engine
r = sr.Recognizer()  # Sets up the recogniser


def sayFunc(words):
    engine.say(words)
    engine.runAndWait()


def Speak(words):  # Outputs whatever is passed
    if __name__ == "__main__":
        p = multiprocessing.Process(target=sayFunc, args=(words,))
        p.start()
        #audio2 = r.listen(source2)
        while p.is_alive():
            if keyboard.is_pressed('q'):
                p.terminate()
            else:
                continue
        p.join()
    #engine.runAndWait()


def Listen():
    with sr.Microphone() as source2:
        print("Speak")
        audio2 = r.listen(source2)  # Listens for input
        text = r.recognize_google(audio2)  # Recognises the words said and stores as text
        return (text)
