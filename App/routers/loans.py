from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models import Session as SessionLocal, Loan, Livre

router = APIRouter(
    prefix="/loans",
    tags=["/loans"]
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@router.get("/")
def get_emprunt(db: Session = Depends(get_db)):
    # Recherche des emprunts dans la base
    emprunt = db.query(Loan).all()
    return {"emprunt": [{"id": em.id, "id_livre": em.id_livre, "id_client": em.id_client, "date_emprunt": em.date_emprunt, "date_retour": em.date_retour} for em in emprunt]}
 
@router.get("/{emprunt_id}")
def get_emprunt(db: Session = Depends(get_db), emprunt_id: int = None):
    emprunt = db.query(Loan).filter(Loan.id == emprunt_id).first()
    
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")
    else:
        return {
            "emprunt": [{
                "id": em.id,
                "id_livre": em.id_livre,
                "id_client": em.id_client,
                "date_emprunt": em.date_emprunt,
                "date_retour": em.date_retour
            } for em in emprunt]
        }
 
@router.put("/{emprunt_id}")
def update_emprunt(
    emprunt_id: int,
    id_livre: Optional[int] = None,
    id_client: Optional[int] = None,
    date_emprunt: Optional[str] = None,
    date_retour: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Recherche de l'emprunt dans la base
    emprunt_base = db.query(Loan).filter(Loan.id == emprunt_id).first()
    
    if emprunt_base is None:
        raise HTTPException(status_code=404, detail=f"Aucun emprunt trouvé avec l'id : {emprunt_id}")

    # Mise à jour de l'emprunt
    if id_livre:
        emprunt_base.id_livre = id_livre
    if id_client:
        emprunt_base.id_client = id_client
    if date_emprunt:
        emprunt_base.date_emprunt = date_emprunt
    if date_retour:
        emprunt_base.date_retour = date_retour

    db.commit()
    db.refresh(emprunt_base)

    return {
        "statut": "succès",
        "message": f"L'ouvrage '{emprunt_base.id}' a été mis à jour",
        "emprunt_modifie": {
            "id": emprunt_base.id,
            "id_livre": emprunt_base.id_livre,
            "id_client": emprunt_base.id_client,
            "date_emprunt": emprunt_base.date_emprunt,
            "date_retour": emprunt_base.date_retour
        }
    }
    
@router.delete("/{emprunt_id}")
def delete_emprunt(emprunt_id: int, db: Session = Depends(get_db)):
    # Localisation de l'emprunt
    emprunt_a_supprimer = db.query(Loan).filter(Loan.id == emprunt_id).first()
    
    if not emprunt_a_supprimer:
        raise HTTPException(
            status_code=404, 
            detail=f"L'emprunt avec l'ID {emprunt_id} est introuvable"
        )
    
    # Conservation du nom pour le message de confirmation
    emprunt = emprunt_a_supprimer.livre
    
    try:
        # Tentative de suppression
        db.delete(emprunt_a_supprimer)
        db.commit()
        
        return {
            "statut": "succès",
            "message": f"L'emprunt de '{emprunt}' (ID: {emprunt_id}) a été supprimé",
            "emprunt_supprime_id": emprunt_id
        }
        
    except Exception as erreur:
        # Annulation en cas d'échec
        db.rollback()
        
        raise HTTPException(
            status_code=400,
            detail=(
                f"Suppression impossible pour '{emprunt}'. "
                "Vérifiez qu'il n'y a pas d'emprunts actifs associés."
            )
        )

@router.post("/")
def create_emprunt(
    id : int,
    id_livre : int,
    id_client : int,
    date_emprunt : str,
    date_retour : str,
    db: Session = Depends(get_db)
):
    """Ajouter un nouvel emprunt"""
    new_emprunt = Loan(
        id = id,
        id_livre = id_livre,
        id_client = id_client,
        date_emprunt = date_emprunt,
        date_retour = date_retour,
    )

    db.add(new_emprunt)
    db.commit()
    db.refresh(new_emprunt)

    return {
        "Retour": "Emprunt ajouté avec succès",
        "Emprunt_id": new_emprunt.id,
        "emprunt": {
            "id": new_emprunt.id,
            "id_livre": new_emprunt.id_livre,
            "id_client": new_emprunt.id_client,
            "date_emprunt": new_emprunt.date_emprunt,
            "date_retour": new_emprunt.date_retour
        }
    }