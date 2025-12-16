from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Session as SessionLocal, Author
 
router = APIRouter(
    prefix="/authors",
    tags=["/authors"]
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@router.get("/")
def get_auteur(db: Session = Depends(get_db)):
    auteur = db.query(Author).all()
    return {"auteur": [{"id": aut.id, "prenom": aut.prenom, "nom": aut.nom, "livres": aut.livres, "Date de naissance" : aut.date_naissance} for aut in auteur]}
 
@router.get("/{auteur_id}")
def get_auteur(db: Session = Depends(get_db), auteur_id: int = None):
    auteur = db.query(Author).filter(Author.id == auteur_id)
    return {"auteur": [{"id": aut.id, "prenom": aut.prenom, "nom": aut.nom, "livres": aut.livres, "Date de naissance" : aut.date_naissance} for aut in auteur]}
 
 
# @rooter.post("/add")
# def create_auteur(autheur: Author):
#     return {"nom": autheur.id, "message": "Autheur créé avec succès"}