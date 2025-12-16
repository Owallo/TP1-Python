from fastapi import APIRouter
from pydantic import BaseModel

root = APIRouter()

class Livres(BaseModel):
    id                  : int
    titre               : str
    year                : str
    author_id           : int 
    isbn                : int
    nb_livres_dispo     : int
    nb_livres_possedes  : int
    type                : str
    langue              : str
    maison_edit         : str
    nb_pages            : int
    description         : str | None = None

@root.get("/books/{books_id}")
def read_book(id: int, name: str | None = None):
    return {"Autheur_id": id, "name": name}

@root.post("/books/")
def create_book(book: Livres):
    return {"item": book.id, "message": "Item créé avec succès"}