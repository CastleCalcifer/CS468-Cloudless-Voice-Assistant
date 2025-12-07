# In tts/tts_engine.py
import os
os.environ['ONNXRUNTIME_GPU_DEVICE_ID'] = ''

from piper import PiperVoice
import simpleaudio as sa  # lightweight cross-platform audio player

# Load the Piper model once at import time
# Use absolute path relative to this file
model_dir = os.path.dirname(__file__)
voice = PiperVoice.load(
    model_path="tts/en_US-amy-medium.onnx",
    config_path="tts/en_US-amy-medium.onnx.json"
)

def speak(text: str) -> None:
    """Converts text to speech using Piper TTS."""

    # Synthesize returns an iterable of AudioChunk objects
    # Collect all audio chunks and concatenate them
    audio_data = b""
    sample_rate = None
    
    for audio_chunk in voice.synthesize(text):
        audio_data += audio_chunk.audio_int16_bytes
        if sample_rate is None:
            sample_rate = audio_chunk.sample_rate
    
    # Play the WAV audio if we have data
    if audio_data:
        wave_obj = sa.WaveObject(audio_data, num_channels=1, bytes_per_sample=2, sample_rate=sample_rate)
        play_obj = wave_obj.play()
        play_obj.wait_done()


''' 
# Windows version of TTS engine using pyttsx3
import pyttsx3

def speak(text: str) -> None:
    """Converts text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()
'''