
from tts.tts_engine import speak

def test_tts_speak_runs_without_error():
    # This test just checks that speak() does not raise an exception
    try:
        speak("Testing TTS output.")
    except Exception as e:
        assert False, f"TTS raised an exception: {e}"
