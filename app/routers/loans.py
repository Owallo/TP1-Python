from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import Session as SessionLocal, Loan, Book
from app.schemas.loans import LoansCreate, LoansUpdate, LoansGet

router = APIRouter(
    prefix="/loans",
    tags=["Emprunts"]
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@router.get("/", response_model=List[LoansGet])
def get_emprunt(db: Session = Depends(get_db)):
    # Recherche des emprunts dans la base
    emprunt = db.query(Loan).all()
    return emprunt

@router.get("/{emprunt_id}", response_model=LoansGet)
def get_emprunt(db: Session = Depends(get_db), emprunt_id: int = None):
    emprunt = db.query(Loan).filter(Loan.id == emprunt_id).first()
    
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")
    
    return emprunt
 
@router.put("/{emprunt_id}", response_model=LoansGet)
def update_emprunt(
    emprunt_id: int,
    emprunt : LoansUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un emprunt existant"""
    # Recherche de l'emprunt dans la base
    emprunt_base = db.query(Loan).filter(Loan.id == emprunt_id).first()
    
    if emprunt_base is None:
        raise HTTPException(status_code=404, detail=f"Aucun emprunt trouvé avec l'id : {emprunt_id}")

    # Mise à jour de l'emprunt
    if emprunt.nom_emprunteur is not None:
        emprunt_base.nom_emprunteur = emprunt.nom_emprunteur
    if emprunt.email_emprunteur is not None:
        emprunt_base.email_emprunteur = emprunt.email_emprunteur
    if emprunt.numero_carte_bibliotheque is not None:
        emprunt_base.numero_carte_bibliotheque = emprunt.numero_carte_bibliotheque
    if emprunt.date_emprunt is not None:
        emprunt_base.date_emprunt = emprunt.date_emprunt
    if emprunt.date_limite_retour is not None:
        emprunt_base.date_limite_retour = emprunt.date_limite_retour
    if emprunt.date_retour_effectif is not None:
        emprunt_base.date_retour_effectif = emprunt.date_retour_effectif
    if emprunt.statut is not None:
        emprunt_base.statut = emprunt.statut
    if emprunt.commentaires is not None:
        emprunt_base.commentaires = emprunt.commentaires

    db.commit()
    db.refresh(emprunt_base)

    return emprunt_base
    
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

@router.post("/add", response_model=LoansGet)
def create_emprunt(
    emprunt: LoansCreate,
    db: Session = Depends(get_db)
):
    """Ajouter un nouvel emprunt"""
    new_emprunt = Loan(
        nom_emprunteur=emprunt.nom_emprunteur,
        email_emprunteur=emprunt.email_emprunteur,
        numero_carte_bibliotheque=emprunt.numero_carte_bibliotheque,
        date_emprunt=emprunt.date_emprunt,
        date_limite_retour=emprunt.date_limite_retour,
        date_retour_effectif=emprunt.date_retour_effectif,
        statut=emprunt.statut,
        commentaires=emprunt.commentaires,
        livre_id=emprunt.livre_id,
    )

    db.add(new_emprunt)
    db.commit()
    db.refresh(new_emprunt)

    return new_emprunt