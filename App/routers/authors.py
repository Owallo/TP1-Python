from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
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
    # Recherche des auteurs dans la base
    auteur = db.query(Author).all()
    return {"auteur": [{"id": aut.id, "prenom": aut.prenom, "nom": aut.nom, "livres": aut.livres, "Date de naissance" : aut.date_naissance} for aut in auteur]}
 
@router.get("/{auteur_id}")
def get_auteur(db: Session = Depends(get_db), auteur_id: int = None):
    auteur = db.query(Author).filter(Author.id == auteur_id).first()
    
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    else:
        return {
            "auteur": {
                "id": auteur.id, 
                "prenom": auteur.prenom,
                "nom": auteur.nom, 
                "livres": auteur.livres, 
                "Date de naissance" : auteur.date_naissance
                }
            }
 
@router.put("/{auteur_id}")
def update_auteur(
    auteur_id: int,
    prenom: Optional[str] = None,
    nom: Optional[str] = None,
    livre: Optional[str] = None,
    date_naissance: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Recherche de l'auteur dans la base
    auteur_base= db.query(Author).filter(Author.id == auteur_id).first()
    
    if auteur_base is None:
        raise HTTPException(status_code=404, detail=f"Aucun auteur trouvé avec l'id : {auteur_id}")
    
    # Mise à jour de l'auteur
    if prenom:
        auteur_base.prenom = prenom
    if nom:
        auteur_base.nom = nom
    if livre:
        auteur_base.livres = livre
    if date_naissance:
        auteur_base.date_naissance = date_naissance
        
    db.commit()
    db.refresh(auteur_base)
    
    return {
        "statut": "succès",
        "message": f"L'ouvrage '{auteur_base.prenom}' a été mis à jour",
        "auteur_modifie": {
            "id": auteur_base.id,
            "prenom": auteur_base.prenom,
            "nom": auteur_base.nom,
            "livres": auteur_base.livres,
            "date_naissance": auteur_base.date_naissance
        }
    }


@router.delete("/{auteur_id}")
def delete_auteur(auteur_id: int, db: Session = Depends(get_db)):
    # Localisation de l'auteur
    auteur_a_supprimer = db.query(Author).filter(Author.id == auteur_id).first()
    
    if not auteur_a_supprimer:
        raise HTTPException(
            status_code=404, 
            detail=f"L'auteur avec l'ID {auteur_id} est introuvable"
        )
    
    # Conservation du nom pour le message de confirmation
    nom_auteur = auteur_a_supprimer.nom
    
    try:
        # Tentative de suppression
        db.delete(auteur_a_supprimer)
        db.commit()
        
        return {
            "statut": "succès",
            "message": f"L'auteur''{nom_auteur}' (ID: {auteur_id}) a été retiré du catalogue",
            "auteur_supprime_id": auteur_id
        }
        
    except Exception as erreur:
        # Annulation en cas d'échec
        db.rollback()
        
        raise HTTPException(
            status_code=400,
            detail=(
                f"Suppression impossible pour '{nom_auteur}'. "
                "Vérifiez qu'il n'y a pas d'emprunts actifs associés."
            )
        )

@router.post("/")
def create_auteur(
    prenom:str = Body(...),
    nom:str = Body(...),
    date_naissance:date = Body(...),
    nationalite :str = Body(...),
    db: Session=Depends(get_db)
):
    """Ajouter un nouvel auteur"""
    new_auteur = Author(
        prenom = prenom,
        nom = nom,
        date_naissance = date_naissance,
        nationalite = nationalite,
    )
    
    db.add(new_auteur)
    db.commit()
    db.refresh(new_auteur)
    
    return {
        "Retour": "Auteur ajouté avec succès",
        "Auteur_id": new_auteur.id,
        "auteur": {
            "id": new_auteur.id,
            "prenom": new_auteur.prenom,
            "nom": new_auteur.nom
        }
    }