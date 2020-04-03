import numpy as np
import threading
import speech_recognition as sr
import pyttsx3
import os
import aiml
from autocorrect import spell

directory = os.path.dirname(os.path.realpath(__file__))
directory = str(directory)
directory = directory.replace("\\","/")

BRAIN_FILE= directory + "/aiml_pretrained_model.dump"

k = aiml.Kernel()
def InizializeBOT():

    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        k.loadBrain(BRAIN_FILE)
    else:
        print("Parsing aiml files")
        k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
        print("Saving brain file: " + BRAIN_FILE)
        k.saveBrain(BRAIN_FILE)

def voiceREC():
    r = sr.Recognizer()
    mic = sr.Microphone()
    while(True):

        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:   
            dialogue = r.recognize_google(audio)
            dialogue = str(dialogue)
            Chatbot(dialogue)
        except:
          print("Google Speech recognition failed")
         

def Chatbot(text):
    query = text
    print(query)
    query = [spell(w) for w in (query.split())]
    question = " ".join(query)
    response = k.respond(question)
    if response:
        SpeechSynth(response)
        print(response)
    else:
        print("Chatbot error")

def SpeechSynth(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
      print("Speechsynth error")
      
if __name__ == "__main__":
    InizializeBOT()
    voiceREC = threading.Thread(target=voiceREC) 
    voiceREC.start() 
