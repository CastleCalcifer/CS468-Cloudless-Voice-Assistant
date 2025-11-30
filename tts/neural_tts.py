"""Optional neural TTS integration using Coqui TTS.

This module tries to use the `TTS` package (Coqui) if available. If it's
not installed, the module exposes TTS_AVAILABLE=False and functions will
raise a clear error or return gracefully so the app can fall back.

Usage:
  from tts.neural_tts import NeuralTTS, TTS_AVAILABLE
  if TTS_AVAILABLE:
      tts = NeuralTTS(model_name)
      path = tts.speak_to_file("Hello", "out.wav")
      play_sound(path)
"""

from typing import Optional
import os

try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False


class NeuralTTS:
    def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
        if not TTS_AVAILABLE:
            raise RuntimeError("Coqui TTS (TTS package) is not installed")
        self.model_name = model_name
        # TTS will download the model on first use if missing
        self.tts = TTS(model_name)

    def speak_to_file(self, text: str, out_path: str = "neural_out.wav") -> str:
        """Synthesize text to a WAV file and return the file path."""
        # Ensure output dir exists
        out_dir = os.path.dirname(out_path) or "."
        os.makedirs(out_dir, exist_ok=True)
        self.tts.tts_to_file(text=text, file_path=out_path)
        return out_path
