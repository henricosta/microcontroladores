import requests
import random
import time

API_URL = "http://localhost:8000/salvar-leitura"
SENSOR_ID = "P1"

print("Simulador iniciado. Enviando leituras falsas...\n")

try:
    current_value = None
    while True:
        new_value = str(round(random.random(), 2))  # any float as string
        if new_value != current_value:
            current_value = new_value
            print(f"[Simulado] {current_value}")
            try:
                new_value = str(round(random.random(), 2))
                requests.post(API_URL, json={"id_sensor": SENSOR_ID, "valor": current_value})
            except Exception as e:
                print(f"Falha ao enviar: {e}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nSimulação encerrada pelo usuário.")
