
import json
import types
from agent.ollama_agent import query_agent


class DummyResponse:
    def __init__(self, lines):
        self._lines = lines

    def raise_for_status(self):
        return None

    def iter_lines(self):
        for l in self._lines:
            yield l


def test_llm_agent_basic_response(monkeypatch):
    # Simulate a streaming response from Ollama
    lines = [json.dumps({"message": {"content": "Paris is the capital of France."}}).encode()]

    def fake_post(url, json=None, stream=None, timeout=None):
        return DummyResponse(lines)

    monkeypatch.setattr("requests.post", fake_post)

    res = query_agent("What is the capital of France?", host="http://localhost:11434", model="tinyllama:latest")
    assert isinstance(res, str)
    assert "Paris" in res


def test_llm_agent_error(monkeypatch):
    # Simulate an exception during request
    def raise_exc(*a, **k):
        raise Exception("connection refused")

    monkeypatch.setattr("requests.post", raise_exc)
    res = query_agent("Hello", host="http://localhost:11434", model="m")
    assert res.startswith("Error contacting Ollama")
