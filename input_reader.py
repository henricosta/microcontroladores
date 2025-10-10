import os, sys, tarfile, time

package_path = os.path.join('dependencies', 'pyserial-3.5.tar.gz')
extract_dir = os.path.join('dependencies', 'pyserial')

try:
    if not os.path.exists(extract_dir):
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Missing dependency: {package_path}")
        with tarfile.open(package_path, "r:gz") as tar:
            tar.extractall(extract_dir)

    sys.path.insert(0, extract_dir)
    import serial
except Exception as e:
    print(f"Failed to load dependency: {e}")
    sys.exit(1)

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
