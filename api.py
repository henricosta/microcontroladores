from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from service import (
    save_state,
    get_last_state,
    get_history,
    get_occupation_time,
    get_all_sensors,
)
from fastapi import FastAPI, WebSocket
from ws_manager import manager
import uvicorn
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Leitura(BaseModel):
    valor: str
    id_sensor: str | None = None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)


@app.post("/salvar-leitura")
async def salvar_leitura(payload: dict):
    id_sensor = payload["id_sensor"]
    valor = str(payload["valor"])

    changed = save_state(id_sensor, valor)

    if changed:
        await manager.broadcast(json.dumps({"id_sensor": id_sensor, "valor": valor}))

    return {"ok": True, "changed": changed}


@app.get("/obter-leitura")
def obter_leitura_endpoint(id_sensor: str | None = Query(None)):
    leitura = get_last_state(id_sensor)
    if not leitura:
        raise HTTPException(status_code=404, detail="Nenhuma leitura encontrada")
    return leitura


@app.get("/historico")
def obter_historico_endpoint(id_sensor: str | None = Query(None)):
    return get_history(id_sensor)


@app.get("/tempo-ocupacao")
def tempo_ocupacao_endpoint(id_sensor: str | None = Query(None)):
    return get_occupation_time(id_sensor)


@app.get("/test-api")
def test_api():
    return {"status": "ok", "mensagem": "API funcionando"}


@app.get("/sensores/json")
async def sensores_json():
    return {"sensors": get_all_sensors()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
