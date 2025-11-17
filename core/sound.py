"""
sound.py - Sound management for feedback and notifications
"""

import os
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
    if PLAYSOUND_AVAILABLE:
        playsound(sound_path)
    else:
        # Fallback for Raspberry Pi
        os.system(f'aplay "{sound_path}"')

if __name__ == "__main__":
    # play_sound(WAKE_SOUND)
    # play_sound(CONFIRM_SOUND)
    # play_sound(ERROR_SOUND)
    pass