[![CI](https://github.com/Anurag20048/checkmycure/actions/workflows/ci.yml/badge.svg)](https://github.com/Anurag20048/checkmycure/actions/workflows/ci.yml)

# Check MyCure

Check MyCure is a student-built healthcare assistant web application that combines a Django REST API with a browser-based frontend. It provides symptom checking, a rule-based health chatbot, optional eye-image analysis, eye-health conversational support, emergency profile/SOS logging, and nearby-clinic lookup.

> **Important:** Check MyCure is an educational project. Its symptom and eye-analysis features are not medical diagnoses and should not replace a qualified healthcare professional.

## What is actually implemented

### Symptom Checker
- Browser-based symptom selection and health-information flow.
- Django REST endpoint: `POST /api/predict/`.
- Deterministic rule-based scoring engine in `backend/health/prediction.py`.
- Returns a top condition, a rule-match confidence score, a score distribution, and general safety guidance.
- This is **not a trained machine-learning disease model**.

### Health Chatbot
- Django REST endpoint: `POST /api/chatbot/`.
- Keyword/rule-based responses for common symptoms, emergencies, and general health topics.
- Includes natural-language, spelling-error, and Hinglish-style phrase handling.
- No Rasa service is required for the main chatbot.

### Eye Health and Rasa
- Optional `POST /api/eye-detection/` endpoint for eye-image screening.
- Uses Ultralytics YOLO when a compatible model file is supplied.
- Stores detection history and processed images for authenticated users.
- The project repository does **not** include the YOLO weights. Configure `EYE_MODEL_PATH` or provide `backend/models/eye/best.pt`.
- Optional Rasa project in `rasa/` provides conversational eye-health intents and responses.
- Django endpoint `POST /api/eye-chat/` sends eye-health questions to a local Rasa REST webhook when available and uses a safe local fallback when Rasa is unavailable.
- Rasa is used for conversational NLP, not for image classification.

### Authentication and History
- Django authentication with DRF token authentication.
- User registration stores name and gender in a profile.
- Authenticated users can view symptom-check and eye-detection history.

### Emergency SOS
- Emergency medical profile and emergency contacts.
- SOS events are logged through Django.
- Browser geolocation can capture the user's current location.
- Phone/SMS/WhatsApp actions are opened by the browser/device for the user to complete. The web app does **not** silently place calls or send messages in the background.
- Optional Twilio server-side notifications can be configured for true automatic SMS/WhatsApp delivery.

### Nearby Clinics
- Django server-side location endpoints proxy OpenStreetMap Nominatim and Overpass requests.
- Internet access is required for live location searches.

## Tech Stack

- **Backend:** Python, Django 5, Django REST Framework
- **Database:** SQLite by default
- **Authentication:** Django auth + DRF token authentication
- **Frontend:** HTML, CSS, JavaScript
- **Computer Vision:** OpenCV + Ultralytics YOLO for optional eye-image analysis
- **Conversational NLP:** Rasa for optional eye-health conversational support
- **Maps/Location:** Browser Geolocation API + OpenStreetMap services
- **Notifications:** Optional Twilio integration for server-side emergency alerts

## Project Structure

```text
checkmycure/
├── backend/
│   ├── api/          # General API/admin models
│   ├── health/       # Symptom checker, chatbot and eye detection
│   ├── emergency/    # Medical profile, contacts and SOS logs
│   ├── insights/     # Preventive-health content
│   ├── backend/      # Django settings and URL configuration
│   ├── manage.py
│   ├── requirements.txt
│   ├── requirements-eye.txt
│   └── requirements-rasa.txt
├── frontend/
│   ├── index.html
│   ├── symptom-checker.html
│   ├── chatbot.html
│   ├── eye-health.html
│   ├── emergency-profile.html
│   ├── emergency-sos.html
│   └── app.js
└── rasa/
    ├── config.yml
    ├── domain.yml
    └── data/
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Create the database

```powershell
python manage.py migrate
```

### 4. Optional: create an admin account

```powershell
python manage.py createsuperuser
```

### 5. Start Django

```powershell
python manage.py runserver 8000
```

Open `http://127.0.0.1:8000/`.

The frontend uses relative `/api/` URLs, so run the Django server and open the application through Django rather than opening HTML files directly with `file://`.

## Optional eye-detection setup

Install the computer-vision dependencies:

```powershell
pip install -r requirements-eye.txt
```

Place a compatible YOLO weights file at:

```text
backend/models/eye/best.pt
```

Or configure another path:

```powershell
$env:EYE_MODEL_PATH = "C:\path\to\best.pt"
```

If the model is unavailable, the application does not invent a disease result. Image upload and webcam capture remain usable.

## Optional Rasa setup

From the repository root:

```powershell
cd backend
pip install -r requirements-rasa.txt
cd ..\rasa
rasa train
rasa run --enable-api --cors "*" --port 5005
```

Then start Django separately from `backend`:

```powershell
python manage.py runserver 8000
```

The eye-health page can use Rasa through `/api/eye-chat/`. If Rasa is not running, Django falls back to the built-in safe eye-health responses.

> Rasa has not been validated as an installed production service in this repository. The project includes the Rasa configuration and Django integration, but actual Rasa training/runtime depends on the user's local Rasa-compatible environment.

## Main API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Register user | No |
| POST | `/api/auth/login/` | Login and receive token | No |
| POST | `/api/predict/` | Rule-based symptom scoring | No |
| POST | `/api/chatbot/` | Health chatbot response | No |
| POST | `/api/eye-chat/` | Eye-health conversational support | No |
| GET | `/api/symptom-checks/` | User symptom history | Yes |
| POST | `/api/eye-detection/` | Optional eye-image detection | Optional |
| GET | `/api/eye-detection/history/` | User eye-detection history | Yes |
| GET/PUT | `/api/medical-profile/` | Emergency medical profile | Yes |
| CRUD | `/api/emergency-contacts/` | Emergency contacts | Yes |
| POST | `/api/sos/` | Log an SOS event | No |
| GET | `/api/emergency-logs/` | User SOS history | Yes |
| GET | `/api/locations/geocode/` | Geocode a place | No |
| GET | `/api/locations/nearby/` | Find nearby healthcare facilities | No |

## Testing

The repository includes Django integration/unit tests and a chatbot benchmark covering standard phrases, natural/slang/Hinglish-style phrases, spelling-error variants, and emergency-priority cases.

The chatbot benchmark measures topic/intent recognition, **not medical diagnostic accuracy**. Run the Django tests inside a virtual environment after installing the base requirements:

```powershell
cd backend
python manage.py check
python manage.py test
```

## Security and deployment notes

- `DEBUG` is intended for local development. Set `DJANGO_DEBUG=0` for deployment.
- Set a real `DJANGO_SECRET_KEY` in deployed environments.
- Configure `DJANGO_ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` for deployment.
- Keep Twilio credentials in environment variables, never frontend JavaScript or GitHub.
- The SQLite database, virtual environments, caches, uploaded media, and model weights should not be committed.
- The included `.env.example` documents supported environment variables.

## Current limitations

1. Symptom prediction is rule-based rather than trained ML.
2. The main health chatbot is rule/keyword based rather than generative AI.
3. Rasa is an optional conversational layer for eye-health questions and requires a compatible local Rasa environment.
4. Eye-image classification requires the compatible YOLO weights file.
5. Browser security/user interaction limits background calling and messaging.
6. Automatic Twilio alerts require valid Twilio credentials and supported recipient numbers.
7. Nearby-facility phone alerts depend on public phone data being available from OpenStreetMap.
8. The default SQLite setup is suitable for development, not a production healthcare deployment.
