
import pytest
from wakeword.detector import listen_for_wakeword

def test_listen_for_wakeword_returns_true(monkeypatch):
    # Monkeypatch recognizer to simulate wake word detection
    class DummyRecognizer:
        def listen(self, source):
            return None
        def recognize_sphinx(self, audio):
            return "assistant"
    monkeypatch.setattr("speech_recognition.Recognizer", lambda: DummyRecognizer())
    assert listen_for_wakeword(["assistant"]) is True
