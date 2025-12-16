from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

rooter = APIRouter(
    prefix="/authors",
    tags=["/authors"]
)

@rooter.get("/{autheur_id}")
def read_item(autheur_id: int, name: Optional[str] = None):
    return {"Autheur_id": autheur_id, "name": name}


@rooter.post("/")
def create_item(autheur: A):
    return {"item": autheur, "message": "Item créé avec succès"}