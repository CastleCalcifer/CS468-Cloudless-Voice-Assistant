from core.assistant import Assistant
from core.recognizer import recognize_speech
from tts.tts_engine import speak
from features.clock import get_time, get_date
from core.intent import COMMON_PHRASES, matches_any
from features.timer import set_duration_timer, set_time_timer, alarm
from agent.ollama_agent import query_agent
#Currently using for debugging
if __name__ == "__main__":
    
    
    text = recognize_speech()
    print("Recognized text:", text)
    
    # An ugly way to handle responses, but it's just for testing.
    if matches_any(text, COMMON_PHRASES["weather"]):
        current_weather = "sunny with a high of 75 degrees." # Placeholder, this will eventually be an API call
        speak("The weather is sunny with a high of 75 degrees.")
        
    elif matches_any(text, COMMON_PHRASES["time"]):
        current_time = get_time()
        speak(current_time)
        
    elif matches_any(text, COMMON_PHRASES["date"]):
        current_date = get_date()
        speak(current_date)
    
    else:
        speak(query_agent(text))
    # assistant = Assistant()
    # assistant.run()  # Main event loop
