@echo off
setlocal
cd /d "%~dp0"

if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

start "API" cmd /k "python api.py"
timeout /t 10 >nul

if "%1"=="-test" (
    start "Simulator" cmd /k "python simulate_serial.py"
) else (
    start "Reader" cmd /k "python read_serial.py"
)

cd page
start "Frontend" cmd /k "python -m http.server 8080"
cd ..

pause