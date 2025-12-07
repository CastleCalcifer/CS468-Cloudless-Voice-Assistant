"""
sound.py - Sound management for feedback and notifications
"""

import os

# Try simpleaudio first, then playsound, then fall back to aplay
SIMPLEAUDIO_AVAILABLE = False
PLAYSOUND_AVAILABLE = False

try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    pass

if not SIMPLEAUDIO_AVAILABLE:
    try:
        from playsound import playsound
        PLAYSOUND_AVAILABLE = True
    except ImportError:
        pass

SOUND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds')

# Example sound file names (place these in the sounds/ folder)
WAKE_SOUND = os.path.join(SOUND_DIR, 'wake.wav')
CONFIRM_SOUND = os.path.join(SOUND_DIR, 'confirm.wav')
ERROR_SOUND = os.path.join(SOUND_DIR, 'error.wav')


def play_sound(sound_path):
    """
    Play a sound file (WAV recommended for Pi).
    Tries simpleaudio first, then playsound, then falls back to aplay.
    """
    if SIMPLEAUDIO_AVAILABLE:
        try:
            wave_obj = sa.WaveObject.from_wave_file(sound_path)
            wave_obj.play()
        except Exception as e:
            print(f"Error playing sound with simpleaudio: {e}")
    elif PLAYSOUND_AVAILABLE:
        try:
            playsound(sound_path)
        except Exception as e:
            print(f"Error playing sound with playsound: {e}")
    else:
        # Fallback to system aplay command for Raspberry Pi
        os.system(f'aplay "{sound_path}"')

if __name__ == "__main__":
    # play_sound(WAKE_SOUND)
    # play_sound(CONFIRM_SOUND)
    # play_sound(ERROR_SOUND)
    pass