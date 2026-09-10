# Check MyCure Eye Health Rasa Assistant

Optional Rasa conversational layer for the eye-health module.

## Run Rasa

From this folder:

```powershell
rasa train
rasa run --enable-api --cors "*" --port 5005
```

The Django `/api/eye-chat/` endpoint uses Rasa when it is available and a safe local fallback when it is not.

The assistant provides general eye-health information and does not diagnose eye disease.
