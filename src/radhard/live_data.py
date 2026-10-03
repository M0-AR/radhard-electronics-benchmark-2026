"""Live data fetchers: NOAA SWPC GOES protons, X-ray flares.
No API key. Falls back to bundled quiet snapshot if offline (reproducibility).
"""
import json, os
import urllib.request

GOES_PROTON_URL = "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json"
GOES_XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"

def fetch_json(url: str, timeout: int = 20):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())

def goes_proton_snapshot(save_path: str = None):
    try:
        data = fetch_json(GOES_PROTON_URL)
        last = data[-12:] if len(data) > 12 else data
        out = {"live": True, "n_points": len(data), "tail": last,
               "source": GOES_PROTON_URL}
    except Exception as e:
        out = {"live": False, "error": str(e), "fallback": "quiet-baseline",
               "source": GOES_PROTON_URL}
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(out, f, indent=2)
    return out
