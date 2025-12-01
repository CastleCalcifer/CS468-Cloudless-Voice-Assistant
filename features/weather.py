import requests

# How `requests` is used in this module:
# - We call `requests.get(base_url, params=params, timeout=10)` to perform an HTTP
#   GET against WeatherAPI's current weather endpoint. The `params` dictionary
#   includes the API `key` and the location query (`q`). The `timeout` ensures
#   the request fails fast if the remote service does not respond.
# - Network-level problems (connection errors, DNS failures, timeouts) raise
#   `requests.RequestException`; we catch that and return an error dict so the
#   rest of the assistant can handle it gracefully.
# - After a response is received we check `resp.status_code` for 200 (OK). For
#   non-200 responses we attempt to parse the JSON error message (if provided)
#   and return it; otherwise we return a generic message including the status
#   code.
# - `resp.json()` is used to decode the response body into Python objects and
#   we use `.get()` when accessing fields so missing keys are handled safely.
# - Important: avoid logging or printing the API key. If you need diagnostic
#   information, log only the URL without the `key` parameter or redact the key.


def get_weather(location, api_key):
    """Fetch current weather for `location` from weatherapi.com.

    Args:
        location (str): City name or query supported by WeatherAPI (e.g., "London" or "94103").
        api_key (str): API key for weatherapi.com from the config.

    Returns:
        dict: On success a dictionary with keys: `location`, `temp_c`, `condition`,
              `humidity`, `wind_kph`, `feelslike_c`, `last_updated`.
              On failure returns `{'error': '<message>'}`.
    """
    if not api_key:
        return {"error": "No weather API key provided"}

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": location, "aqi": "no"}

    try:
        resp = requests.get(base_url, params=params, timeout=10)
    except requests.RequestException as exc:
        return {"error": f"Network error when contacting weather service: {exc}"}

    if resp.status_code != 200:
        # Try to parse error message from provider if present
        try:
            data = resp.json()
            msg = data.get("error", {}).get("message") if isinstance(data, dict) else None
        except Exception:
            msg = None
        return {"error": msg or f"Weather API returned status {resp.status_code}"}

    try:
        data = resp.json()
        loc = data.get("location", {})
        cur = data.get("current", {})

        result = {
            "location": f"{loc.get('name', '')}, {loc.get('region', '')}".strip(', '),
            "temp_c": cur.get("temp_c"),
            "condition": cur.get("condition", {}).get("text"),
            "humidity": cur.get("humidity"),
            "wind_kph": cur.get("wind_kph"),
            "feelslike_c": cur.get("feelslike_c"),
            "last_updated": cur.get("last_updated"),
        }
        return result
    except ValueError:
        return {"error": "Invalid JSON returned from weather service"}
