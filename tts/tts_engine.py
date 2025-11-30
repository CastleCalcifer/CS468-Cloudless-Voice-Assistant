import os
import yaml
import pyttsx3
from typing import Optional


def _init_engine() -> Optional[pyttsx3.Engine]:
    """Attempt to initialize pyttsx3 and choose a reasonable voice.

    This avoids hard-coded Windows voice IDs which will fail on Linux
    (espeak) and other platforms. If initialization fails, return None.
    """
    try:
        engine = pyttsx3.init()
    except Exception as e:
        print(f"pyttsx3.init() failed: {e}")
        return None

    # Load optional audio/tts configuration from config/config.yaml (or example)
    config = {}
    try:
        cfg_path = 'config/config.yaml'
        if not os.path.exists(cfg_path):
            cfg_path = 'config/config_example.yaml'
        with open(cfg_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    except Exception:
        config = {}

    # Set speaking rate from config or reasonable default
    try:
        rate = 150
        rate = int(config.get('audio', {}).get('tts_rate', rate))
        engine.setProperty('rate', rate)
    except Exception:
        pass

    # Try selecting an English voice if available (avoid platform-specific ids)
    try:
        voices = engine.getProperty('voices') or []
        preferred = None

        # If user specified a voice id/name in config, try to match it first
        cfg_voice = config.get('audio', {}).get('tts_voice')
        if cfg_voice:
            for v in voices:
                vid = getattr(v, 'id', '') or ''
                name = getattr(v, 'name', '') or ''
                if cfg_voice.lower() in vid.lower() or cfg_voice.lower() in name.lower():
                    preferred = vid
                    break

        # Otherwise prefer US English if present, then fall back to other English
        if not preferred:
            # first pass: look specifically for en-us markers
            for v in voices:
                vid = getattr(v, 'id', '') or ''
                name = getattr(v, 'name', '') or ''
                if 'en-us' in vid.lower() or 'en_us' in vid.lower() or 'english (america)' in name.lower() or 'america' in name.lower():
                    preferred = vid
                    break
        if not preferred:
            for v in voices:
                vid = getattr(v, 'id', '') or ''
                name = getattr(v, 'name', '') or ''
                if 'english' in name.lower() or vid.lower().startswith('en') or 'en_' in vid.lower() or 'en-' in vid.lower():
                    preferred = vid
                    break

        if preferred:
            try:
                engine.setProperty('voice', preferred)
            except Exception as e:
                print(f"Could not set preferred voice ({preferred}): {e}")
    except Exception as e:
        print(f"Error enumerating voices: {e}")

    # Volume (0.0 to 1.0)
    try:
        vol = float(config.get('audio', {}).get('tts_volume', 1.0))
        vol = max(0.0, min(1.0, vol))
        engine.setProperty('volume', vol)
    except Exception:
        pass

    return engine


# Initialize engine once and reuse it. If initialization fails, _ENGINE will be None
# and speak() will fall back to printing the text.
_ENGINE = _init_engine()


def speak(text: str) -> None:
    """Speak the given text.

    If speech is unavailable we fallback to printing the text so the
    caller still gets feedback (useful for headless/testing environments).
    """
    global _ENGINE

    if _ENGINE is None:
        # Try a late init attempt (in case audio became available)
        _ENGINE = _init_engine()

    if _ENGINE is None:
        print(f"[TTS unavailable] {text}")
        return

    try:
        # Allow config to control blocking behavior; default is blocking
        blocking = True
        try:
            cfg_path = 'config/config.yaml' if os.path.exists('config/config.yaml') else 'config/config_example.yaml'
            with open(cfg_path, 'r') as f:
                cfg = yaml.safe_load(f) or {}
                blocking = bool(cfg.get('audio', {}).get('tts_blocking', True))
        except Exception:
            blocking = True

        _ENGINE.say(text)
        # pyttsx3's runAndWait is blocking; for now we keep blocking behavior
        _ENGINE.runAndWait()
    except Exception as e:
        # Don't let TTS crashes bring down the app; print instead.
        print(f"TTS playback failed: {e}")
        print(text)

