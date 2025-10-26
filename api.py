from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from service import save_state, get_last_state, get_history, get_occupation_time
import uvicorn

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

@app.post("/salvar-leitura")
def salvar_leitura_endpoint(leitura: Leitura):
    changed = save_state(leitura.id_sensor, leitura.valor)
    if changed:
        return {"status": "ok", "mensagem": "Novo estado salvo"}
    return {"status": "ok", "mensagem": "Estado não alterado"}

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
