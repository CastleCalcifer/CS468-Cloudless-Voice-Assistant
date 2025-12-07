# In tts/tts_engine.py
import os
import sys
import io
import wave

try:
    from piper import PiperVoice

    # Load the Piper model once at import time
    model_dir = os.path.dirname(__file__)
    voice = PiperVoice.load(
        model_path=os.path.join(model_dir, "en_US-amy-medium.onnx"),
        config_path=os.path.join(model_dir, "en_US-amy-medium.onnx.json")
    )

    # Try to import pyaudio first, fall back to simpleaudio
    audio_backend = None
    try:
        import pyaudio
        audio_backend = "pyaudio"
    except ImportError:
        try:
            import simpleaudio as sa
            audio_backend = "simpleaudio"
        except ImportError:
            print("Warning: Neither pyaudio nor simpleaudio could be imported")

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
            if audio_backend == "pyaudio":
                # Use pyaudio for playback
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True
                )
                stream.write(audio_data)
                stream.stop_stream()
                stream.close()
                p.terminate()
            elif audio_backend == "simpleaudio":
                # Use simpleaudio for playback
                wave_obj = sa.WaveObject(audio_data, num_channels=1, bytes_per_sample=2, sample_rate=sample_rate)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            else:
                print("Error: No audio backend available for playback")

except Exception as e:
    print(f"Error initializing Piper TTS engine: {e}")