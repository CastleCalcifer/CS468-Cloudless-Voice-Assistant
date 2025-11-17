# In tts/tts_engine.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slower speech
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# Use female voice
engine.setProperty('voice', voice_id)

def speak(text: str) -> None:
    """Converts text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()
