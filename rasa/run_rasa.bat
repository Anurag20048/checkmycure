@echo off
cd /d "%~dp0"
echo Training Rasa eye assistant...
rasa train
echo Starting Rasa on http://127.0.0.1:5005
rasa run --enable-api --cors "*" --port 5005
pause
