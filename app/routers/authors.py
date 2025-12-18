from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import date
from app.models import Session as SessionLocal, Author
from app.schemas.author import AuteurGet, AuteurUpdate, AuteurCreate

router = APIRouter(
    prefix="/authors",
    tags=["Auteurs"]
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@router.get("/", response_model=list[AuteurGet])
def get_auteur(db: Session = Depends(get_db)):
    # Recherche des auteurs dans la base
    auteur = db.query(Author).all()
    return auteur

@router.get("/search")
def search_authors(
    page: int = 1,
    page_size: int = 5,
    nom: Optional[str] = None,
    nationalite: Optional[str] = None,
    sort_by: str = "nom",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Recherche d'auteurs avec filtres et pagination
    
    Paramètres:
    - nom: recherche partielle par prénom ou nom (insensible à la casse)
    - nationalite: recherche exacte par code ISO
    - sort_by: tri par 'nom' ou 'date_naissance' (défaut: nom)
    - order: 'asc' (croissant) ou 'desc' (décroissant) (défaut: asc)
    - page, page_size: pagination
    """
    conditions = []
    
    if nom:
        conditions.append(
            (Author.nom(f"%{nom}%")) | (Author.prenom(f"%{nom}%"))
        )
    
    # Recherche par nationalité 
    if nationalite:
        conditions.append(Author.nationalite == nationalite)
    
    query = db.query(Author)
    
    # Appliquer les filtres
    if conditions:
        query = query.filter(and_(*conditions))
    
    # Tri
    if sort_by == "nom":
        if order == "desc":
            query = query.order_by(Author.nom.desc())
        else:
            query = query.order_by(Author.nom)
    elif sort_by == "date_naissance":
        if order == "desc":
            query = query.order_by(Author.date_naissance.desc())
        else:
            query = query.order_by(Author.date_naissance)
    
    total = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    auteurs = query.offset(offset).limit(page_size).all()
    
    pages = (total + page_size - 1) // page_size
    
    return {
        "auteurs": [
            {
                "id": aut.id,
                "prenom": aut.prenom,
                "nom": aut.nom,
                "date_naissance": aut.date_naissance,
                "nationalite": aut.nationalite,
                "livres": aut.livres
            }
            for aut in auteurs
        ],
        "page_courante": page,
        "taille_page": page_size,
        "total": total,
        "pages_totales": pages,
        "tri": {
            "sort_by": sort_by,
            "order": order
        }
    }
 
@router.get("/{auteur_id}", response_model=AuteurGet)
def get_auteur(db: Session = Depends(get_db), auteur_id: int = None):
    auteur = db.query(Author).filter(Author.id == auteur_id).first()
    
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    else:
        return auteur
 
@router.put("/{auteur_id}")
def update_auteur(
    auteur_id: int,
    auteur : AuteurUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un auteur existant"""
    # Recherche de l'auteur dans la base
    auteur_base = db.query(Author).filter(Author.id == auteur_id).first()
    
    if auteur_base is None:
        raise HTTPException(status_code=404, detail=f"Aucun auteur trouvé avec l'id : {auteur_id}")
    
    # Mise à jour de l'auteur
    if auteur.prenom is not None:
        auteur_base.prenom = auteur.prenom
    if auteur.nom is not None:
        auteur_base.nom = auteur.nom
    if auteur.date_naissance is not None:
        auteur_base.date_naissance = auteur.date_naissance
    if auteur.nationalite is not None:
        auteur_base.nationalite = auteur.nationalite
        
    db.commit()
    db.refresh(auteur_base)
    
    return {
        "statut": "succès",
        "message": f"L'auteur '{auteur_base.prenom} {auteur_base.nom}' a été mis à jour",
        "auteur_modifie": {
            "id": auteur_base.id,
            "prenom": auteur_base.prenom,
            "nom": auteur_base.nom,
            "date_naissance": auteur_base.date_naissance,
            "nationalite": auteur_base.nationalite
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

@router.post("/add")
def create_auteur(
    auteur : AuteurCreate,
    db: Session = Depends(get_db)
):
    """Ajouter un nouvel auteur"""
    new_auteur = Author(
        prenom=auteur.prenom,
        nom=auteur.nom,
        date_naissance=auteur.date_naissance,
        nationalite=auteur.nationalite,
    )
    
    db.add(new_auteur)
    db.commit()
    db.refresh(new_auteur)
    
    return {
        "statut": "succès",
        "message": "Auteur ajouté avec succès",
        "auteur_id": new_auteur.id,
        "auteur": {
            "id": new_auteur.id,
            "prenom": new_auteur.prenom,
            "nom": new_auteur.nom
        }
    }