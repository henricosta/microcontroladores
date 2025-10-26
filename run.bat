@echo off
setlocal

REM Go to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip and install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pyserial

REM Run the Python script
echo Running script...
python read_serial.py

REM Deactivate and end
deactivate
endlocal
