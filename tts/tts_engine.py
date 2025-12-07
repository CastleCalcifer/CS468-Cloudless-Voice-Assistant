# In tts/tts_engine.py
import os
import sys

if sys.platform == "win32":
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
else:
    # Linux/Mac version using Piper TTS
    try:
        from piper import PiperVoice
        import simpleaudio as sa  # lightweight cross-platform audio player

        # Load the Piper model once at import time
        # Use absolute path relative to this file
        model_dir = os.path.dirname(__file__)
        voice = PiperVoice.load(
            model_path=os.path.join(model_dir, "en_US-amy-medium.onnx"),
            config_path=os.path.join(model_dir, "en_US-amy-medium.onnx.json")
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
                # Add a small silence buffer at the start to prevent audio cutoff
                # This gives the audio device time to initialize (150ms of silence)
                silence_duration_ms = 150
                silence_frames = int(sample_rate * silence_duration_ms / 1000)
                silence_bytes = b'\x00\x00' * silence_frames  # 2 bytes per frame (16-bit audio)
                padded_audio = silence_bytes + audio_data
                
                wave_obj = sa.WaveObject(padded_audio, num_channels=1, bytes_per_sample=2, sample_rate=sample_rate)
                play_obj = wave_obj.play()
                play_obj.wait_done()
    except Exception as e:
        print(f"Error initializing Piper TTS engine: {e}")