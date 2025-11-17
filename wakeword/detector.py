import speech_recognition as sr
from core.recognizer import is_online

def listen_for_wakeword(wakewords:list[str]) -> bool:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        #Constantly listen for wake word
        while True:
            print(f"Listening for wake words... {', '.join(wakewords)}")
            audio = recognizer.listen(source)
            
            if is_online():
                try:
                    # Try online recognition first
                    text = recognizer.recognize_google(audio)
                    if any(word in text.lower() for word in wakewords):
                        print(f"Wake word detected: {text}")
                        return True
                except sr.UnknownValueError:
                    pass
            else:
                try:
                    # If offline...
                    text = recognizer.recognize_sphinx(audio) 
                    if any(word in text.lower() for word in wakewords):
                        print(f"Wake word detected: {text}")
                        return True
                
                except sr.UnknownValueError:
                    continue
