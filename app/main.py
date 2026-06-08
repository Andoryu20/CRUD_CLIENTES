from fastapi import FastAPI
from app.config import Base, engine
from app.countries.models import Country
from app.clients.models import Client
from app.categories.models import Category
from app.clients.router import router as clients_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prueba Técnica AI Turing - FastAPI")

app.include_router(clients_router)

@app.get('/')
def read_root():
    return {"message": "API funcionando y tablas creadas con éxito"}

