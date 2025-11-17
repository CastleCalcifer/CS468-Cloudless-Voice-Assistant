from wakeword.detector import listen_for_wakeword
from tts.tts_engine import speak
from core.recognizer import recognize_speech
from features import timer, clock, weather, traffic
from features.clock import get_time, get_date
from core.intent import COMMON_PHRASES, matches_any
from features.timer import set_duration_timer, set_time_timer, alarm
from agent.ollama_agent import query_agent
import yaml

class Assistant:
    def __init__(self):
        # Load configuration, initialize state
        try:
            with open('config/config_example.yaml') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def run(self):
        # Load wake words and LLM config
        wakewords = self.config.get('wakewords', ["assistant"])
        llm_config = self.config.get('llm', {})
        llm_host = llm_config.get('host', "http://localhost:11434")
        llm_model = llm_config.get('model', "qwen2.5:1.5b-instruct")
        
        # Main event loop
        while True:
            if listen_for_wakeword(wakewords):
                print("Wake word detected!")
                text = recognize_speech()
                print("Recognized text:", text)
                
                # An ugly way to handle responses, but it's just for testing.
                if matches_any(text, COMMON_PHRASES["weather"]):
                    current_weather = "sunny with a high of 75 degrees." # Placeholder, this will eventually be an API call
                    speak(current_weather)
                    
                elif matches_any(text, COMMON_PHRASES["time"]):
                    current_time = get_time()
                    speak(current_time)
                    
                elif matches_any(text, COMMON_PHRASES["date"]):
                    current_date = get_date()
                    speak(current_date)
                
                else:
                    print("Going to LLM for response...")
                    response = query_agent(text, llm_host, llm_model)
                    if response and not response.startswith("Error contacting Ollama"):
                        speak(response)
                    else:
                        print(response)  # Or speak a fallback message
