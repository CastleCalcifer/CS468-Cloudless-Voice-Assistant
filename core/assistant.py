from wakeword.detector import listen_for_wakeword
from tts.tts_engine import speak
from core.recognizer import recognize_speech
from features import timer, clock, weather, traffic
from agent.ollama_agent import query_agent
import yaml

class Assistant:
    def __init__(self):
        # Load configuration, initialize state
        try:
            with open('config/config.yaml') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def run(self):
        # Main event loop
        while True:
            if listen_for_wakeword():
                print("Wake word detected!")
                text = recognize_speech()
                if text:
                    print(f"Heard: {text}")
                    # Add command dispatching logic here
                    # For now, just ask LLM
                    response = query_agent(text)
                    speak(response)
