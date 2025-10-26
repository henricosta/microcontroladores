@echo off
setlocal
cd /d "%~dp0"
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

start "API" cmd /c "python api.py"
timeout /t 2 >nul

if "%1"=="-test" (
    start "Simulator" cmd /c "python simulate_serial.py"
) else (
    start "Reader" cmd /c "python read_serial.py"
)

cd page
start "Frontend" cmd /c "python -m http.server 8080"
echo Running... API=8000, Frontend=8080
pause
