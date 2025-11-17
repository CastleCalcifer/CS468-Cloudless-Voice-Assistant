from core.assistant import Assistant
from core.recognizer import recognize_speech
from tts.tts_engine import speak
from features.clock import get_time, get_date

#Currently using for debugging.
if __name__ == "__main__":
    text = recognize_speech()
    print("Recognized text:", text)
    # An ugly way to handle responses, but it's just for testing.
    if "What's the weather".lower() in text.lower():
        speak("The weather is sunny with a high of 75 degrees.")
    elif "What time is it".lower() in text.lower():
        current_time = get_time()
        speak(current_time)
    elif "What's the date".lower() in text.lower():
        current_date = get_date()
        speak(current_date)
    # assistant = Assistant()
    # assistant.run()  # Main event loop
