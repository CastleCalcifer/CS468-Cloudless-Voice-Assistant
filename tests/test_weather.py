
from features.weather import get_weather
import requests


class DummyResp:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


def test_get_weather_success(monkeypatch):
    sample = {
        "location": {"name": "Birmingham", "region": "West Midlands"},
        "current": {
            "temp_c": 10,
            "condition": {"text": "Sunny"},
            "humidity": 50,
            "wind_kph": 12,
            "feelslike_c": 9,
            "last_updated": "2025-11-26 10:00",
        },
    }

    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(200, sample))

    res = get_weather("Birmingham", "fakekey")
    assert isinstance(res, dict)
    assert res.get("location")
    assert res.get("temp_c") == 10
    assert res.get("condition") == "Sunny"


def test_get_weather_network_error(monkeypatch):
    def raise_exc(*a, **k):
        raise requests.RequestException("network down")

    monkeypatch.setattr("requests.get", raise_exc)
    res = get_weather("Birmingham", "fakekey")
    assert "error" in res and "Network error" in res["error"]


def test_get_weather_non_200(monkeypatch):
    monkeypatch.setattr(
        "requests.get",
        lambda *a, **k: DummyResp(401, {"error": {"message": "API key invalid"}}),
    )

    res = get_weather("Birmingham", "badkey")
    assert res.get("error") == "API key invalid"


def test_get_weather_no_key():
    res = get_weather("Birmingham", None)
    assert res.get("error") == "No weather API key provided"
