#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python api.py &
API_PID=$!
sleep 2

# Serve frontend folder
cd page
python -m http.server 8080 &
FRONT_PID=$!

echo "Running... API=8000, Frontend=8080"
wait $SIM_PID

kill $API_PID $FRONT_PID 2>/dev/null || true