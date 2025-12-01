import requests
from urllib.parse import quote_plus


def get_traffic(location, api_key):
    """Fetch traffic summary for a location using TomTom APIs.

    Steps:
    - Geocode `location` with TomTom Search API to get latitude/longitude.
    - Query TomTom Flow Segment Data at that point to get current speed and travel time.

    Returns a dict on success with fields:
        `location`, `lat`, `lon`, `current_speed_kph`, `free_flow_speed_kph`,
        `current_travel_time_s`, `free_flow_travel_time_s`, `confidence`, `congestion_pct`
    On error returns `{'error': '<message>'}`.
    """
    if not api_key:
        return {"error": "No traffic API key provided"}

    # 1) Geocode the location
    try:
        q = quote_plus(location)
        geocode_url = f"https://api.tomtom.com/search/2/geocode/{q}.json?key={api_key}&limit=1"
        gresp = requests.get(geocode_url, timeout=10)
    except requests.RequestException as exc:
        return {"error": f"Network error during geocoding: {exc}"}

    if gresp.status_code != 200:
        try:
            data = gresp.json()
            msg = data.get("error", {}).get("message") if isinstance(data, dict) else None
        except Exception:
            msg = None
        return {"error": msg or f"Geocoding returned status {gresp.status_code}"}

    try:
        gdata = gresp.json()
        results = gdata.get("results", [])
        if not results:
            return {"error": "No geocoding results for location"}
        pos = results[0].get("position", {})
        lat = pos.get("lat")
        lon = pos.get("lon")
        if lat is None or lon is None:
            return {"error": "Geocoding did not return coordinates"}
    except ValueError:
        return {"error": "Invalid JSON returned from geocoding API"}

    # 2) Query flow segment data for traffic at that point
    try:
        flow_url = (
            f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&unit=KMPH&key={api_key}"
        )
        fresp = requests.get(flow_url, timeout=10)
    except requests.RequestException as exc:
        return {"error": f"Network error when querying traffic service: {exc}"}

    if fresp.status_code != 200:
        try:
            data = fresp.json()
            msg = data.get("error", {}).get("message") if isinstance(data, dict) else None
        except Exception:
            msg = None
        return {"error": msg or f"Traffic API returned status {fresp.status_code}"}

    try:
        fdata = fresp.json()
        fs = fdata.get("flowSegmentData", {})

        current_speed = fs.get("currentSpeed")
        free_flow_speed = fs.get("freeFlowSpeed")
        current_travel_time = fs.get("currentTravelTime")
        free_flow_travel_time = fs.get("freeFlowTravelTime")
        confidence = fs.get("confidence")

        # compute congestion percent if speeds available
        if free_flow_speed and free_flow_speed > 0 and current_speed is not None:
            congestion_pct = max(0.0, (1 - (current_speed / free_flow_speed)) * 100)
        else:
            congestion_pct = None

        return {
            "location": location,
            "lat": lat,
            "lon": lon,
            "current_speed_kph": current_speed,
            "free_flow_speed_kph": free_flow_speed,
            "current_travel_time_s": current_travel_time,
            "free_flow_travel_time_s": free_flow_travel_time,
            "confidence": confidence,
            "congestion_pct": congestion_pct,
        }
    except ValueError:
        return {"error": "Invalid JSON returned from traffic service"}
