#!/bin/bash
set -e

# Go to script directory
cd "$(dirname "$0")"

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pyserial

# Run the Python script
python read_serial.py
