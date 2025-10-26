from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()
latest_reading: Optional[str] = None

class Leitura(BaseModel):
    valor: str

@app.post("/salvar-leitura")
def salvar_leitura(leitura: Leitura):
    global latest_reading
    latest_reading = leitura.valor
    return {"status": "ok", "mensagem": "Leitura salva com sucesso"}

@app.get("/obter-leitura")
def obter_leitura():
    if latest_reading is None:
        raise HTTPException(status_code=404, detail="Nenhuma leitura disponível")
    return {"valor": latest_reading}

@app.get("/test-api")
def test_api():
    return {"status": "ok", "mensagem": "API funcionando"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
