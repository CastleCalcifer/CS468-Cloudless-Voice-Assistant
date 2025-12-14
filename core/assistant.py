from wakeword.detector import listen_for_wakeword
from tts.tts_engine import speak
from core.recognizer import recognize_speech
from features import timer, clock, weather, traffic
from features.clock import get_time, get_date
from core.intent import COMMON_PHRASES, matches_any
from features.timer import set_duration_timer, set_time_timer, alarm
from agent.ollama_agent import query_agent
from core.sound import play_sound, WAKE_SOUND, CONFIRM_SOUND, ERROR_SOUND
import yaml
import re
from datetime import datetime, timedelta

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
        # Load wake words and LLM config
        wakewords_assistant = self.config.get('wakewords_assistant', ["assistant"])
        wakewords_LLM = self.config.get('wakewords_LLM', ["computer"])
        llm_config = self.config.get('llm', {})
        llm_host = llm_config.get('host', "http://localhost:11434")
        llm_model = llm_config.get('model', "qwen2.5:1.5b-instruct")
        
        # Main event loop
        while True:
            detected, wakeword_type = listen_for_wakeword(wakewords_assistant, wakewords_LLM)
            if detected:
                print(f"Wake word detected! Type: {wakeword_type}")
                play_sound(WAKE_SOUND)
                text = recognize_speech()
                print("Recognized text:", text)

                 # Route based on wakeword type
                if wakeword_type == 'LLM':
                    # Use LLM for open-ended queries
                    print("Going to LLM for response...")
                    response = query_agent(text, llm_host, llm_model)
                    if response and not response.startswith("Error contacting Ollama"):
                        speak(response)
                        continue
                    else:
                        print(response)  # Or speak a fallback message
                        continue
                
                # An ugly way to handle responses, but it's just for testing.
                if matches_any(text, COMMON_PHRASES["weather"]):
                    weather_api_key = self.config.get('weather_api_key')
                    location = self.config.get('location', 'London')
                    result = weather.get_weather(location, weather_api_key)
                    if "error" in result:
                        speak(f"I couldn't get the weather: {result['error']}")
                    else:
                        msg = f"In {result.get('location')}, it's {result.get('condition')} and {result.get('temp_c')} degrees Celsius. Feels like {result.get('feelslike_c')} degrees."
                        speak(msg)
                    
                elif matches_any(text, COMMON_PHRASES["traffic"]):
                    traffic_api_key = self.config.get('traffic_api_key')
                    location = self.config.get('location', 'London')
                    result = traffic.get_traffic(location, traffic_api_key)
                    if "error" in result:
                        speak(f"I couldn't get traffic info: {result['error']}")
                    else:
                        congestion = result.get('congestion_pct')
                        current_speed = result.get('current_speed_kph')
                        if congestion is not None and current_speed is not None:
                            msg = f"Traffic in {result.get('location')}: currently {current_speed} kilometers per hour, about {congestion:.0f} percent congested."
                        else:
                            msg = f"Traffic in {result.get('location')}: current speed {current_speed} kilometers per hour."
                        speak(msg)
                    
                elif matches_any(text, COMMON_PHRASES["time"]):
                    current_time = get_time()
                    speak(current_time)
                    
                elif matches_any(text, COMMON_PHRASES["date"]):
                    current_date = get_date()
                    speak(current_date)
                
                elif matches_any(text, COMMON_PHRASES["timer"]):
                    # Extract duration from text (e.g., "set a timer for 5 minutes")
                    duration_seconds = self._extract_timer_duration(text)
                    if duration_seconds:
                        def timer_callback():
                            speak("Timer finished!")
                            play_sound(CONFIRM_SOUND)
                        set_duration_timer(duration_seconds, timer_callback)
                        minutes = duration_seconds // 60
                        speak(f"Timer set for {minutes} minutes.")
                    else:
                        speak("I couldn't understand the timer duration. Please say something like 'set a timer for 5 minutes'.")
                
                elif matches_any(text, COMMON_PHRASES["clock"]):
                    # Extract time from text (e.g., "set an alarm for 5:30 PM")
                    target_time = self._extract_alarm_time(text)
                    if target_time:
                        def alarm_callback():
                            speak("Alarm!")
                            play_sound(CONFIRM_SOUND)
                        try:
                            set_time_timer(target_time, alarm_callback)
                            speak(f"Alarm set for {target_time.strftime('%I:%M %p')}.")
                        except ValueError:
                            speak("That time is in the past. Please set an alarm for a future time.")
                    else:
                        speak("I couldn't understand the alarm time. Please say something like 'set an alarm for 5:30 PM'.")
                
                else:
                    # Unrecognized command, suggest LLM usage
                    llm_words = ", ".join(wakewords_LLM)
                    speak(f"I didn't recognize that. You can say {llm_words} to get an AI response.")
    
    def _extract_timer_duration(self, text: str) -> int:
        """Extract timer duration in seconds from user input.
        
        Looks for patterns like "5 minutes", "30 seconds", "2 hours", etc.
        Returns duration in seconds or None if not found.
        """
        text = text.lower()
        
        # Try to find "X minutes/seconds/hours"
        patterns = [
            (r'(\d+)\s*(?:hours?|hrs?)', 3600),
            (r'(\d+)\s*(?:minutes?|mins?)', 60),
            (r'(\d+)\s*(?:seconds?|secs?)', 1),
        ]
        
        for pattern, multiplier in patterns:
            match = re.search(pattern, text)
            if match:
                value = int(match.group(1))
                return value * multiplier
        
        return None
    
    def _extract_alarm_time(self, text: str) -> datetime:
        """Extract alarm time from user input.
        
        Looks for patterns like "5:30 PM", "17:30", "5 PM", etc.
        Returns a datetime object for today at that time, or None if not found.
        """
        text = text.lower()
        now = datetime.now()
        
        # Pattern: "HH:MM AM/PM" or "H:MM AM/PM"
        match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            am_pm = match.group(3)
            
            if am_pm == 'pm' and hour != 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0
            
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Pattern: "H AM/PM" (e.g., "5 PM")
        match = re.search(r'(\d{1,2})\s*(am|pm)', text)
        if match:
            hour = int(match.group(1))
            am_pm = match.group(2)
            
            if am_pm == 'pm' and hour != 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0
            
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
        
        return None
