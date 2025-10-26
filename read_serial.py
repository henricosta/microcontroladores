import serial
import time
import sys

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
except KeyboardInterrupt:
    print("\nStopped by user.")
    ser.close()
except Exception as e:
    print(f"Serial read error: {e}")
    sys.exit(1)
