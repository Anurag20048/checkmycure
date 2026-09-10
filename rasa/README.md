# Check MyCure Eye Health Rasa Assistant

This is the optional Rasa conversational layer for the eye-health module.

## Run Rasa

Install the version listed in `backend/requirements-rasa.txt`, then from this folder run:

```bash
rasa train
rasa run --enable-api --cors "*" --port 5005
```

The Django `/api/eye-chat/` endpoint sends messages to Rasa when it is available. If Rasa is not running, Check MyCure uses a safe local fallback so the eye page remains usable.

The conversational assistant provides general health information and does not diagnose eye disease.
