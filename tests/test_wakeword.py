
import sys
import types
import pytest

# Ensure a stub for the external speech_recognition package exists during import
sys.modules.setdefault('speech_recognition', types.SimpleNamespace(Recognizer=lambda: None, Microphone=lambda: None, UnknownValueError=Exception))
sys.modules.setdefault('pyttsx3', types.SimpleNamespace(init=lambda: None))
from wakeword import detector


def test_listen_for_wakeword_offline(monkeypatch):
    # Simulate the offline (Sphinx) recognition path and a detected wakeword
    class DummyRecognizer:
        def listen(self, source):
            return b"audio"

        def recognize_sphinx(self, audio):
            return "assistant"

    class DummyMicrophone:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(detector.sr, "Recognizer", lambda: DummyRecognizer())
    monkeypatch.setattr(detector.sr, "Microphone", lambda: DummyMicrophone())
    # Force offline path
    monkeypatch.setattr("core.recognizer.is_online", lambda: False)

    assert detector.listen_for_wakeword(["assistant"]) is True


def test_listen_for_wakeword_online(monkeypatch):
    # Simulate the online (Google) recognition path
    class DummyRecognizer:
        def listen(self, source):
            return b"audio"

        def recognize_google(self, audio):
            return "Hey Assistant"

    class DummyMicrophone:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(detector.sr, "Recognizer", lambda: DummyRecognizer())
    monkeypatch.setattr(detector.sr, "Microphone", lambda: DummyMicrophone())
    monkeypatch.setattr("core.recognizer.is_online", lambda: True)

    assert detector.listen_for_wakeword(["assistant"]) is True
