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
    python simulate_serial.py
) else (
    python read_serial.py
)
taskkill /FI "WINDOWTITLE eq API" /F >nul 2>&1
deactivate
endlocal
