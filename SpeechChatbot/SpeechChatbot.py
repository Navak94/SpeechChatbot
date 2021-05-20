from pynput import keyboard
import speech_recognition as sr
import time
import pyaudio
import wave
import sched
import pyttsx3
from autocorrect import Speller
import aiml
import os
import sys

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

directory = os.path.dirname(os.path.realpath(__file__))
directory = str(directory)
directory = directory.replace("\\", "/")

BRAIN_FILE = directory + "/aiml_pretrained_model.dump"

k = aiml.Kernel()

p = pyaudio.PyAudio()
frames = []


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)


class KeyListener(keyboard.Listener):
    def __init__(self):
        super(KeyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)

    def on_press(self, key):
        if key.char == 'r':
            self.key_pressed = True
        elif key.char == 'q':
            sys.exit()

        return True

    def on_release(self, key):
        if key.char == 'r':
            self.key_pressed = False
        return True


def speech_synth(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speechsynth error")


def InizializeBOT():
    if os.path.exists(BRAIN_FILE):
        # print("Loading from brain file: " + BRAIN_FILE)
        k.loadBrain(BRAIN_FILE)
    else:
        # print("Parsing aiml files")
        k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
        # print("Saving brain file: " + BRAIN_FILE)
        k.saveBrain(BRAIN_FILE)


def chatbot(text):
    query = text
    print(query)
    split = query.split()
    spell = Speller()
    query = [spell(w) for w in split]
    question = " ".join(query)
    response = k.respond(question)
    if response:
        speech_synth(response)
        print(response)
    else:
        print("Chatbot error")


def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        # print("Key is pressed..")
        try:
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=callback)
            # print("Stream active:", stream.is_active())
            started = True
            # print("start Stream")
        except:
            raise

    elif not listener.key_pressed and started:
        # print("Stop recording")
        stream.stop_stream()
        stream.close()
        # p.terminate()

        listener.wf.writeframes(b''.join(frames))
        listener.wf.close()
        # print ("You should have a wav file in the current directory"r
        r = sr.Recognizer()
        file = sr.AudioFile("output.wav")
        with file as source:
            audio = r.record(source)
        try:
            dialogue = r.recognize_google(audio)
            dialogue = str(dialogue)
            chatbot(dialogue)
        except:
            print("Google Speech recognition failed")
        started = False
        clean()
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())


def clean():
    global listener, started, stream, frames
    listener = None
    listener = KeyListener()
    listener.start()
    started = False
    stream = None
    frames = []


if __name__ == "__main__":
    clean()
    InizializeBOT()

    print("Press and hold the 'r' key to begin recording")
    print("Release the 'r' key to end recording")
    task = sched.scheduler(time.time, time.sleep)
    task.enter(0.1, 1, recorder, ())
    task.run()
