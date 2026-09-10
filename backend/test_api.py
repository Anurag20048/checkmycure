"""Optional live-server smoke test. Run directly, not as a Django test module."""
import json
import urllib.request

BASE = "http://127.0.0.1:8000"

def main():
    print("Check MyCure live API smoke test")
    print("Start Django first: python manage.py runserver 8000")

    with urllib.request.urlopen(BASE + "/", timeout=5) as r:
        print("[OK] Home:", r.status)

    req = urllib.request.Request(
        BASE + "/api/predict/",
        data=json.dumps({"symptoms": ["fever", "cough"]}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        print("[OK] Prediction:", r.status, r.read().decode()[:300])

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[FAIL] Live smoke test:", exc)
        raise SystemExit(1)
