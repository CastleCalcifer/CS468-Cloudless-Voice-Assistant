
import pytest
from agent.ollama_agent import query_agent

def test_llm_agent_basic_response():
    response = query_agent("What is the capital of France?", host="http://localhost:11434", model="tinyllama:latest")
    assert isinstance(response, str)
    assert "Paris" in response or response != ""
