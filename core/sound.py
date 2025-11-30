"""
sound.py - Sound management for feedback and notifications
"""

import os
from shutil import which

# Prefer a pure-python audio player when available to avoid native deps
try:
    import simpleaudio as _simpleaudio
    SIMPLEAUDIO_AVAILABLE = True
except Exception:
    _simpleaudio = None
    SIMPLEAUDIO_AVAILABLE = False

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False

SOUND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds')

# Example sound file names (place these in the sounds/ folder)
WAKE_SOUND = os.path.join(SOUND_DIR, 'wake.wav')
CONFIRM_SOUND = os.path.join(SOUND_DIR, 'confirm.wav')
ERROR_SOUND = os.path.join(SOUND_DIR, 'error.wav')


def play_sound(sound_path):
    """
    Play a sound file (WAV recommended for Pi).
    """
    # 1) Try simpleaudio (pure-Python) - preferred because it doesn't
    # depend on PyGObject / GStreamer.
    if SIMPLEAUDIO_AVAILABLE and _simpleaudio is not None:
        try:
            wave_obj = _simpleaudio.WaveObject.from_wave_file(sound_path)
            play_obj = wave_obj.play()
            # Non-blocking: return immediately. If you want blocking play,
            # call play_obj.wait_done().
            return
        except Exception as e:
            print(f"simpleaudio playback failed: {e}; falling back to other players.")

    # 2) Try playsound (may raise runtime errors if native deps missing)
    if PLAYSOUND_AVAILABLE:
        try:
            playsound(sound_path)
            return
        except Exception as e:
            print(f"playsound failed: {e}; falling back to system player.")

    # 3) Fallback order: paplay (PulseAudio), aplay (ALSA), ffplay (ffmpeg)
    if which("paplay"):
        os.system(f'paplay "{sound_path}"')
    elif which("aplay"):
        os.system(f'aplay "{sound_path}"')
    elif which("ffplay"):
        # ffplay prints to stderr; suppress it and auto-exit after play
        os.system(f'ffplay -nodisp -autoexit "{sound_path}" >/dev/null 2>&1')
    else:
        # Last resort: try aplay without checking (may still fail) and
        # otherwise print a clear message for the user.
        try:
            os.system(f'aplay "{sound_path}"')
        except Exception:
            print("No audio playback method available. Install 'simpleaudio', 'paplay' (PulseAudio), 'aplay' (ALSA) or PyGObject (python3-gi).")

if __name__ == "__main__":
    # play_sound(WAKE_SOUND)
    # play_sound(CONFIRM_SOUND)
    # play_sound(ERROR_SOUND)
    pass