from fastapi import FastAPI
from pydantic import BaseModel

root = FastAPI(
    title="Gestion des Livres et Auteurs",
    description="API TP Python : Bibliothèques",
    version="1.0.0"
)

class Loan(BaseModel):
    id                  : int
    reference           : str
    nom_emprunteur      : str
    email_emprunteur    : str 
    numero_carte        : str
    date_emprunt        : str
    date_limite_retour  : str
    date_retour         : str
    statut              : str
    commentaire         : str

@root.get("/loans/{books_id}")
def read_book(id: int, name: str | None = None):
    return {"Autheur_id": id, "name": name}

@root.post("/loans/")
def create_book(emprunt: Loan):
    return {"item": emprunt.id, "message": "Item créé avec succès"}