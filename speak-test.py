#from TTS.api import TTS
#import sounddevice as sd

## Initialize TTS with a simple English model
#tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")

#wav = tts.tts(text="Hello world!")

## Play the audio using sounddevice
#sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
#sd.wait() 

import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice: {voice.name}, ID: {voice.id}")

engine.setProperty('voice', 'english-us')

engine.say('ee The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
