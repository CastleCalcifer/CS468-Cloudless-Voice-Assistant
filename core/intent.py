# intent.py
"""
Intent and command matching utilities for the voice assistant.
"""

COMMON_PHRASES = {
    "date": [
        "what's the date", "what is the date", "tell me the date", "date today", "today's date", "can you tell me the date"
    ],
    "time": [
        "what's the time", "what is the time", "tell me the time", "current time", "time now", "can you tell me the time"
    ],
    "weather": [
        "what's the weather", "what is the weather", "tell me the weather", "weather today", "current weather", "can you tell me the weather"
    ],
    "timer": [
        "set a timer", "start a timer", "timer for", "remind me in", "countdown for", "can you set a timer"
    ],
    "clock": [
        "set an alarm", "wake me up at", "alarm for", "alarm at", "can you set an alarm"
    ],
    # Add more intents and phrases as needed
}

def matches_any(text:str, phrases:list) -> bool:
    """
    Returns True if any phrase in the list is found in the text (case-insensitive).
    """
    text = text.lower()
    return any(phrase in text for phrase in phrases)

# Example usage:
# if matches_any(user_input, COMMON_PHRASES["date"]):
#     ...
