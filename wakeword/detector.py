import speech_recognition as sr

def listen_for_wakeword(wakewords:list[str]) -> bool:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        #Constantly listen for wake word
        while True:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            
            try:
                # Default to sphinx for wake word detection, so it's always offline
                text = recognizer.recognize_sphinx(audio) 
                if any(word in text.lower() for word in wakewords):
                    print(f"Wake word detected: {text}")
                    return True
                
            except sr.UnknownValueError:
                continue
