# Check MyCure

Check MyCure is a student-built healthcare assistant web application that combines a Django REST API with a browser-based frontend. It provides symptom checking, a rule-based health chatbot, optional YOLO-based eye image analysis, emergency profile/SOS logging, and nearby-clinic lookup.

> **Important:** Check MyCure is an educational project. Its symptom and eye-analysis features are not medical diagnoses and should not replace a qualified healthcare professional.

## What is actually implemented

### Symptom Checker
- Browser-based symptom selection and health information flow.
- Django REST endpoint: `POST /api/predict/`.
- A deterministic rule-based scoring engine in `backend/health/prediction.py`.
- Returns a top condition, a rule-match confidence score, a score distribution, and general safety guidance.

**This is not a trained machine-learning disease model.** The current implementation uses symptom-rule matching, so the project should not claim TensorFlow/Scikit-learn disease prediction unless a separate trained model is added.

### Health Chatbot
- Django REST endpoint: `POST /api/chatbot/`.
- Keyword/rule-based responses for common symptoms, emergencies, and general health topics.
- No Rasa service is required by the current implementation.

### Eye Health
- Optional `POST /api/eye-detection/` endpoint.
- Uses Ultralytics YOLO when a compatible model file is supplied.
- Stores detection history and processed images for authenticated users.
- The project archive does **not** include the YOLO weights, so the eye-detection endpoint requires an external model file configured with `EYE_MODEL_PATH`.

### Authentication and History
- Django authentication with DRF token authentication.
- User registration stores name and gender in a profile.
- Authenticated users can view their symptom-check and eye-detection history.

### Emergency SOS
- Emergency medical profile and emergency contacts.
- SOS events are logged through Django.
- Browser geolocation can capture the user's current location.
- Phone/SMS/WhatsApp actions are opened by the browser/device for the user to complete. The web app does **not** silently place calls or send messages in the background.

### Nearby Clinics
- Uses OpenStreetMap-based services from the frontend for nearby healthcare searches.

## Tech Stack

- **Backend:** Python, Django 5, Django REST Framework
- **Database:** SQLite by default
- **Authentication:** Django auth + DRF token authentication
- **Frontend:** HTML, CSS, JavaScript
- **Computer Vision:** OpenCV/Ultralytics YOLO for the optional eye-detection feature
- **Maps/Location:** Browser Geolocation API + OpenStreetMap services

## Project Structure

```text
checkmycure/
├── backend/
│   ├── api/          # General API/admin models
│   ├── health/       # Symptom checker, chatbot, eye detection
│   ├── emergency/    # Medical profile, contacts and SOS logs
│   ├── insights/     # Preventive-health content
│   ├── backend/      # Django settings and URL configuration
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── symptom-checker.html
    ├── chatbot.html
    ├── eye-health.html
    ├── emergency-profile.html
    ├── emergency-sos.html
    └── app.js
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

### 5. Start the application

```powershell
python manage.py runserver 8000
```

Open the application at `http://127.0.0.1:8000/`.

The frontend uses relative `/api/` URLs, so run the Django server and open the application through Django rather than opening HTML files directly with `file://`.

## Optional eye-detection feature

Install the additional computer-vision dependencies only if you want to use eye detection:

```powershell
pip install -r requirements-eye.txt
```

Then place a compatible YOLO weights file at:

```text
backend/models/eye/best.pt
```

Or set the environment variable:

```powershell
$env:EYE_MODEL_PATH = "C:\path\to\best.pt"
```

The endpoint returns a clear error when the model is not available instead of relying on a developer-specific absolute Windows path.

## Main API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Register user | No |
| POST | `/api/auth/login/` | Login and receive token | No |
| POST | `/api/predict/` | Rule-based symptom prediction | No |
| POST | `/api/chatbot/` | Health chatbot response | No |
| GET | `/api/symptom-checks/` | User symptom history | Yes |
| POST | `/api/eye-detection/` | Optional eye image detection | Optional |
| GET | `/api/eye-detection/history/` | User eye-detection history | Yes |
| GET/PUT | `/api/medical-profile/` | Emergency medical profile | Yes |
| CRUD | `/api/emergency-contacts/` | Emergency contacts | Yes |
| POST | `/api/sos/` | Log an SOS event | No |
| GET | `/api/emergency-logs/` | User SOS history | Yes |

## Testing

The included chatbot benchmark covers standard phrases, natural/slang/Hinglish-style phrases, spelling-error variants, and emergency-priority cases. The benchmark measures topic/intent recognition, not medical diagnostic accuracy. Django integration tests should be run in the project virtual environment after installing the requirements.

## Development Notes

- `DEBUG` is enabled by default for local development. Set `DJANGO_DEBUG=0` for a production deployment.
- Set a real `DJANGO_SECRET_KEY` in any deployed environment.
- Configure `DJANGO_ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` for deployment.
- The SQLite database is intentionally excluded from the project package; run migrations locally.
- Do not commit virtual environments, `__pycache__`, model weights, or user-uploaded media.

## Current limitations

1. Symptom prediction is rule-based rather than trained ML.
2. The chatbot is rule/keyword based rather than a generative AI assistant.
3. Eye detection requires the missing YOLO weights file.
4. Browser security/user interaction limits background calling and messaging.
5. The default SQLite setup is suitable for development, not a production healthcare deployment.
## Important: run through Django

Do **not** open the HTML files directly with `file://`. The application uses Django API endpoints such as `/api/chatbot/`, `/api/predict/`, `/api/sos/`, and `/api/locations/nearby/`.

Start the backend first:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Then open `http://127.0.0.1:8000/`.

## Feature status

- **Symptom Checker:** rule-based symptom scoring, no external ML package required.
- **Chatbot:** Django REST endpoint with rule-based health responses.
- **Nearby Clinics:** Django server proxies OpenStreetMap Nominatim and Overpass requests to avoid browser CORS problems. Internet access is required.
- **Emergency SOS:** obtains browser location, records an SOS event, shows a Google Maps location link, and provides user-controlled 112, phone, WhatsApp and SMS actions. Browsers cannot silently place calls or send messages.
- **Eye Health:** image upload and webcam capture work without the model. Actual eye-disease classification requires the compatible trained `best.pt` model at `backend/models/eye/best.pt` or the `EYE_MODEL_PATH` environment variable. The app does not invent a disease result when the model is missing.

### Eye model setup

Place your trained model here:

```text
backend/models/eye/best.pt
```

or set a Windows environment variable before starting Django:

```powershell
$env:EYE_MODEL_PATH = "C:\path\to\best.pt"
python manage.py runserver 8000
```


## Emergency notification setup

The Emergency SOS page can display the saved emergency contacts, medical profile, current location, and nearby healthcare facilities. The browser can open a phone/SMS/WhatsApp action, but it cannot silently send an SMS or WhatsApp message.

For true automatic server-side alerts after the user presses SOS, configure Twilio on the Django server. Copy `backend/.env.example` to `backend/.env` and fill in the Twilio values. Never expose these credentials in frontend JavaScript or GitHub.

Automatic hospital alerts only work for nearby facilities that publish a phone number in OpenStreetMap. Facilities without a public phone number are shown but cannot be contacted automatically. Calling India's 112 emergency service still requires the user/device phone system unless a separate authorized emergency-services integration is available.
