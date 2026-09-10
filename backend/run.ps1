$ErrorActionPreference = "Stop"

Write-Host "Check MyCure setup" -ForegroundColor Cyan

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    python -m venv venv
}

& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\python.exe -m pip install -r requirements.txt
& .\venv\Scripts\python.exe manage.py migrate

Write-Host ""
Write-Host "Starting Check MyCure at http://127.0.0.1:8000/" -ForegroundColor Green
& .\venv\Scripts\python.exe manage.py runserver 8000
