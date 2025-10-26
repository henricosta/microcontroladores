#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python api.py &
API_PID=$!
sleep 2
if [ "$1" == "-test" ]; then
    python simulate_serial.py
else
    python read_serial.py
fi
kill $API_PID 2>/dev/null || true
