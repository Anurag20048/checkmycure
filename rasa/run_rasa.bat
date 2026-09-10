@echo off
cd /d %~dp0
rasa train
rasa run --enable-api --cors "*" --port 5005
