from fastapi import FastAPI
from pydantic import BaseModel

root = FastAPI(
    title="Gestion des Livres et Auteurs",
    description="API TP Python : Bibliothèques",
    version="1.0.0"
)

class Autheur(BaseModel):
    id          : int
    name        : str
    last_name   : str
    birth       : str
    death       : str | None = None
    country     : int
    biography   : str | None = None
    url         : str | None = None
    

@root.get("/authors/{autheur_id}")
def read_item(autheur_id: int, name: str | None = None):
    return {"Autheur_id": autheur_id, "name": name}

@root.post("/authors/")
def create_item(autheur: Autheur):
    return {"item": autheur, "message": "Item créé avec succès"}