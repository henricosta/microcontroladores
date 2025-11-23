import serial
import time
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

# API_URL = "http://209.97.156.234:8000/salvar-leitura"
API_URL = "http://localhost:8000/salvar-leitura"
SENSOR_ID = "P1"

executor = ThreadPoolExecutor(max_workers=20)

def send_to_api(value):
    try:
        requests.post(API_URL, json={"id_sensor": SENSOR_ID, "valor": str(value)})
    except Exception as e:
        print(f"Failed to send data: {e}")

try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
except Exception as e:
    print(f"Failed to connect to serial port: {e}")
    sys.exit(1)

print("Connected. Reading data...\n")

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"[Arduino] {line}")
            executor.submit(send_to_api, line)
except KeyboardInterrupt:
    print("\nStopped by user.")
    ser.close()
except Exception as e:
    print(f"Serial read error: {e}")
    ser.close()
    sys.exit(1)
