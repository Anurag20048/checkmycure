from pathlib import Path
import re

html = Path(__file__).resolve().parents[1] / "frontend" / "emergency-sos.html"
text = html.read_text(encoding="utf-8")
checks = {
    "user-triggered SOS": 'onclick="activateEmergency()"' in text and 'SOS is intentionally user-triggered' in text,
    "geolocation": 'navigator.geolocation.getCurrentPosition' in text,
    "backend SOS endpoint": "fetch('/api/sos/'" in text,
    "112 call action": "tel:112" in text,
    "WhatsApp action": "https://wa.me/" in text,
    "SMS action": "sms:" in text,
    "last-known-location fallback": "lastKnownLocation" in text,
    "emergency cancellation": 'function cancelEmergency()' in text,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if failed:
    raise SystemExit(1)
print("Frontend emergency static checks passed.")
