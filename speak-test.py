from TTS.api import TTS
import sounddevice as sd

# Initialize TTS with a simple English model
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")

wav = tts.tts(text="Hello world!")

# Play the audio using sounddevice
sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
sd.wait() 