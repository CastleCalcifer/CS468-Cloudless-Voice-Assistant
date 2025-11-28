
import sys
import types


class DummyEngine:
    def __init__(self):
        self.props = {}
        self.said = []

    def setProperty(self, k, v):
        self.props[k] = v

    def say(self, text):
        self.said.append(text)

    def runAndWait(self):
        return None


def test_tts_speak_runs_without_error(monkeypatch):
    engine = DummyEngine()
    # Ensure the module import succeeded by injecting a dummy pyttsx3
    sys.modules.setdefault('pyttsx3', types.SimpleNamespace(init=lambda: DummyEngine()))
    from tts import tts_engine

    monkeypatch.setattr(tts_engine, "pyttsx3", types.SimpleNamespace(init=lambda: engine))

    # Call speak; should use our DummyEngine and record the text
    tts_engine.speak("Testing TTS output.")
    assert engine.said == ["Testing TTS output."]
