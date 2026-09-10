# 🩺 Check MyCure

**Check MyCure** is a student-built healthcare assistant web application that combines a Django REST backend with a browser-based frontend. The project provides symptom-based health information, a conversational health chatbot, optional YOLO eye-image screening, emergency SOS support, and nearby healthcare-facility lookup.

> **Medical disclaimer:** Check MyCure is an educational software project. It does not provide medical diagnoses, prescriptions, or a replacement for professional medical care. Emergency features depend on the user's device, browser permissions, available services, and configuration.

## ✨ Features

### 🩺 Symptom Checker
- Interactive symptom selection through the web UI.
- Django REST endpoint: `POST /api/predict/`.
- Deterministic rule-based symptom matching in `backend/health/prediction.py`.
- Returns health information, rule-match scores, and safety guidance.
- The current implementation is **not a trained disease-prediction ML model**.

### 💬 Health Chatbot
- Django REST endpoint: `POST /api/chatbot/`.
- Recognizes common symptoms, emergency phrases, medication/clinic questions, spelling variations, slang, and selected Hinglish phrases.
- Provides topic-specific health information without diagnosing or prescribing.
- Includes a deterministic local fallback, so the main chatbot remains usable without an external NLP service.

### 👁️ Eye Health
- Eye image upload and camera capture through the frontend.
- Django REST endpoint: `POST /api/eye-detection/`.
- Optional Ultralytics YOLO inference when a compatible trained model is supplied.
- Detection history for authenticated users.
- **The YOLO weights are not included in this repository.** Configure your model with `EYE_MODEL_PATH` or place it at `backend/models/eye/best.pt`.
- If the model is unavailable, the application explicitly reports that detection is unavailable instead of generating a fake medical result.

### 🤖 Rasa Eye-health Conversation
- Optional Rasa service under `rasa/`.
- Rasa handles conversational eye-health intents such as redness, pain, blurred vision, dry/itchy eyes, screening-result questions, prevention, and emergency eye symptoms.
- Django calls the Rasa REST webhook when it is running and falls back to a local eye-health response when Rasa is unavailable.
- Rasa is a conversational NLP component. It does **not** perform image classification.

### 🚨 Emergency SOS
- Emergency medical profile and emergency contacts.
- Browser geolocation support.
- SOS event logging through Django.
- Nearby healthcare facilities can be displayed with location information.
- User-controlled call, SMS, WhatsApp, and emergency-number actions.
- Optional Twilio integration can send configured alerts when valid Twilio credentials are supplied.
- The browser cannot silently place phone calls or send SMS/WhatsApp messages without an appropriate user/device or external-service action.

### 📍 Nearby Clinics
- Django location endpoints for geocoding and nearby healthcare searches.
- Uses OpenStreetMap-based location services.
- Invalid coordinates are validated before external lookup.

### 🔐 Authentication & History
- Django authentication with DRF token authentication.
- User profile data including name and gender.
- Authenticated symptom and eye-detection history.

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| Backend | Python, Django 5, Django REST Framework |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite by default |
| Authentication | Django Auth + DRF Token Authentication |
| Symptom engine | Python rule-based matching |
| Computer Vision | Ultralytics YOLO, OpenCV (optional eye module) |
| Conversational AI | Rasa (optional) |
| Location | Browser Geolocation API + OpenStreetMap services |
| Emergency messaging | Twilio (optional) |

## 🚀 Local Setup

```powershell
git clone https://github.com/Anurag20048/checkmycure.git
cd checkmycure\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver 8000
```

Open `http://127.0.0.1:8000/`.

## 👁️ Enable YOLO Eye Screening

The trained YOLO weights are not included. Install the optional dependencies:

```powershell
cd backend
pip install -r requirements-eye.txt
```

Then place your compatible model at `backend/models/eye/best.pt` or configure `.env`:

```env
EYE_MODEL_PATH=C:\path\to\your\best.pt
```

Restart Django after changing the model path. Only use disease classes/results that your actual trained model supports.

## 🤖 Enable Rasa

Rasa is optional. Django uses a local fallback if Rasa is unavailable.

```powershell
cd rasa
pip install -r ..\backend\requirements-rasa.txt
rasa train
rasa run --enable-api --cors "*" --port 5005
```

Run Django in a second terminal:

```powershell
cd backend
python manage.py runserver 8000
```

## 🚨 Optional Twilio Alerts

Keep credentials server-side and never commit them:

```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
TWILIO_WHATSAPP_FROM=
```

## 🧪 Testing

```powershell
cd backend
python manage.py check
python manage.py test
python test_chatbot_accuracy.py
```

The project contains focused tests for chatbot behavior, eye-chat fallback, location endpoints, prediction rules, and emergency frontend behavior.

## 🔒 Security & Privacy

- Keep `.env` files, API keys, Twilio credentials, and private model weights out of version control.
- Treat user health information as sensitive data.
- The project is intended for education and portfolio demonstration.

## ⚠️ Limitations

- Symptom checking is rule-based, not a validated clinical ML model.
- Eye screening depends on an externally supplied YOLO model and has no claimed clinical validation.
- Rasa is optional and requires its own service process.
- Emergency actions depend on browser/device permissions or configured external services.
- Nearby healthcare results depend on OpenStreetMap services and network availability.

## 📌 Project Status

**Portfolio-ready educational project:** the application, API flows, frontend features, tests, optional YOLO integration, and optional Rasa integration are organized for local development and demonstration.

For production healthcare use, additional clinical validation, security/privacy controls, monitoring, legal/regulatory review, and professionally reviewed medical content would be required.
