import speech_recognition as sr

def listen_for_wakeword(wakewords) -> bool:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_sphinx(audio)
                if any(word in text.lower() for word in wakewords):
                    print(f"Wake word detected: {text}")
                    return True
            except sr.UnknownValueError:
                continue
