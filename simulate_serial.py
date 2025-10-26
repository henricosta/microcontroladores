import requests
import random
import time

API_URL = "http://localhost:8000/salvar-leitura"

print("Simulador iniciado. Enviando leituras falsas...\n")

try:
    while True:
        leitura = round(random.uniform(20.0, 30.0), 2)
        print(f"[Simulado] {leitura}")
        try:
            requests.post(API_URL, json={"valor": str(leitura)})
        except Exception as e:
            print(f"Falha ao enviar: {e}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nSimulação encerrada pelo usuário.")
