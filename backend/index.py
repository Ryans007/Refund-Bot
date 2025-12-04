from routes.chat_router import router as chat_router
from fastapi import FastAPI
import uvicorn

from database.database import database_engine, Base

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """Evento de inicialização do aplicativo FastAPI."""
    try:
        print("Criando Banco de Dados")
        Base.metadata.create_all(bind=database_engine)
        print("Banco de Dados criado com sucesso")
    except Exception as e:
        print("Erro ao criar o Banco de Dados:", e)

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

