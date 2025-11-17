import speech_recognition as sr
import socket
from tts.tts_engine import speak

def is_online(host="8.8.8.8", port=53, timeout=3) -> bool:
    '''Check internet connectivity by attempting to connect to a known host.'''
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    if is_online():
        try:
            return recognizer.recognize_google(audio)
        except Exception as e:
            print("Google error:", e)
    try:
        return recognizer.recognize_sphinx(audio)
    except Exception as e:
        print("Sphinx error:", e)
    return ""

if __name__ == "__main__":
    print("Online status:", is_online())
    text = recognize_speech()
    print("Recognized text:", text)
    
    if "What's the weather" in text:
        speak("The weather is sunny with a high of 75 degrees.")