from concurrent.futures import ThreadPoolExecutor
import requests, random, time

API_URL = "http://localhost:8000/salvar-leitura"
SENSOR_IDS = [f"P{i}" for i in range(2, 21)]  # Exclude P1

print("Simulador iniciado. Enviando leituras falsas...\n")

def send(sensor, value):
    try:
        requests.post(API_URL, json={"id_sensor": sensor, "valor": value})
    except Exception as e:
        print(f"Falha ao enviar para {sensor}: {e}")

current_values = {sensor: None for sensor in SENSOR_IDS}
executor = ThreadPoolExecutor(max_workers=20)

try:
    while True:
        sensors_to_update = random.sample(SENSOR_IDS, k=random.randint(2, 3))
        for sensor in sensors_to_update:
            new_value = str(round(random.random(), 2))
            if new_value != current_values[sensor]:
                current_values[sensor] = new_value
                print(f"[Simulado] {sensor}: {new_value}")
                executor.submit(send, sensor, new_value)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nSimulação encerrada pelo usuário.")
