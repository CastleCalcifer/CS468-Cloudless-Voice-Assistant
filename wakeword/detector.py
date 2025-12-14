import speech_recognition as sr
from core.recognizer import is_online

def listen_for_wakeword(wakewords_assistant: list[str], wakewords_LLM: list[str]) -> tuple[bool, str]:
    """
    Listen for wakewords (both assistant and LLM types).
    Returns: (detected: bool, wakeword_type: str) where wakeword_type is 'assistant' or 'LLM'
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Combine wakewords for display
        wakewords = wakewords_assistant + wakewords_LLM
        #Constantly listen for wake word
        while True:
            print(f"Listening for wake words... {', '.join(wakewords)}")
            audio = recognizer.listen(source)
            
            if is_online():
                try:
                    # Try online recognition first
                    text = recognizer.recognize_google(audio)
                    # Check for assistant wakewords
                    if any(word in text.lower() for word in wakewords_assistant):
                        print(f"Wake word detected (assistant): {text}")
                        return True, 'assistant'
                    # Check for LLM wakewords
                    elif any(word in text.lower() for word in wakewords_LLM):
                        print(f"Wake word detected (LLM): {text}")
                        return True, 'LLM'
                    else:
                        print(f"Heard: \"{text}\" (no wake word detected)")
                except sr.UnknownValueError:
                    pass
            else:
                try:
                    # If offline...
                    text = recognizer.recognize_sphinx(audio) 
                    # Check for assistant wakewords
                    if any(word in text.lower() for word in wakewords_assistant):
                        print(f"Wake word detected (assistant): {text}")
                        return True, 'assistant'
                    # Check for LLM wakewords
                    elif any(word in text.lower() for word in wakewords_LLM):
                        print(f"Wake word detected (LLM): {text}")
                        return True, 'LLM'
                    else:
                        print(f"Heard: \"{text}\" (no wake word detected)")
                
                except sr.UnknownValueError:
                    continue
