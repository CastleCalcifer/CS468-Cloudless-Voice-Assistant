from features.traffic import get_traffic
import requests


class DummyResp:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


def test_get_traffic_success(monkeypatch):
    # Mock geocode response
    geocode = {"results": [{"position": {"lat": 52.4862, "lon": -1.8904}}]}

    # Mock flow response
    flow = {
        "flowSegmentData": {
            "currentSpeed": 40,
            "freeFlowSpeed": 60,
            "currentTravelTime": 120,
            "freeFlowTravelTime": 80,
            "confidence": 0.8,
        }
    }

    calls = {"i": 0}

    def fake_get(url, *a, **k):
        # first call is geocode
        if "search/2/geocode" in url:
            return DummyResp(200, geocode)
        if "flowSegmentData" in url:
            return DummyResp(200, flow)
        return DummyResp(404, {})

    monkeypatch.setattr("requests.get", fake_get)

    res = get_traffic("Birmingham", "fakekey")
    assert isinstance(res, dict)
    assert res.get("lat") == 52.4862
    assert res.get("current_speed_kph") == 40
    assert res.get("free_flow_speed_kph") == 60
    assert res.get("congestion_pct") == (1 - 40 / 60) * 100


def test_get_traffic_geocode_failure(monkeypatch):
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(200, {"results": []}))
    res = get_traffic("Nowhere", "fakekey")
    assert "error" in res and "No geocoding results" in res["error"]


def test_get_traffic_no_key():
    res = get_traffic("Birmingham", None)
    assert res.get("error") == "No traffic API key provided"
