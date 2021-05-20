# SpeechChatbot

Credit to https://medium.com/@pemagrg/aiml-tutorial-a8802830f2bf

Chatbot using text to speech and speech synthesizer.

The chatbot listens when 'r' key is pressed until it is released. After that, it will compute and give you an answer.

## Install 

In order to use this you need to pip3 install the following


```
autocorrect
aiml
autocorrect
pyaudio
pyttsx3
SpeechRecognition
```

## Workaround

Due to the fact that `speech_recognition` uses an `AudioData` instance
and that the `pyaudio` stream can't be directly converted to it, the
stream had to be saved to an output file and that filed opened with
`sr.AudioFile("output.wav")`
