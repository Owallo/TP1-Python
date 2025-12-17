from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Book, Author
from typing import Optional, List
from app.schemas.book import BookCreate, BookUpdate, BookGet

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[BookGet])
def get_books(page: int = 1, db: Session = Depends(get_db)):
    """Récupérer la liste des livres (pagination conservée, mais la réponse renvoie la liste d'objets)."""
    per_page = 5
    offset = (page - 1) * per_page

    livres = db.query(Book).offset(offset).limit(per_page).all()

    return [
        {
            "id": livre.id,
            "titre": livre.titre,
            "isbn": livre.isbn,
            "annee_publication": livre.annee_publication,
            "auteur_id": livre.auteur_id,
            "nombre_exemplaires_disponibles": livre.nombre_exemplaires_disponibles,
            "nombre_exemplaires_total": livre.nombre_exemplaires_total,
            "categorie": livre.categorie,
            "langue": livre.langue,
            "nombre_pages": livre.nombre_pages,
            "maison_edition": livre.maison_edition,
        }
        for livre in livres
    ]

@router.get("/{livre_id}", response_model=BookGet)
def get_book(livre_id: int, db: Session = Depends(get_db)):
    """Récupérer les détails d'un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return {
        "id": livre.id,
        "titre": livre.titre,
        "isbn": livre.isbn,
        "annee_publication": livre.annee_publication,
        "auteur_id": livre.auteur_id,
        "nombre_exemplaires_disponibles": livre.nombre_exemplaires_disponibles,
        "nombre_exemplaires_total": livre.nombre_exemplaires_total,
        "categorie": livre.categorie,
        "langue": livre.langue,
        "nombre_pages": livre.nombre_pages,
        "maison_edition": livre.maison_edition
    }

@router.post("/")
def create_book(
    book: BookCreate = Body(...),
    db: Session = Depends(get_db)
):
    """Ajouter un nouveau livre (body validé par BookCreate)"""
    # Vérifier que l'auteur existe
    auteur = db.query(Author).filter(Author.id == book.auteur_id).first()
    if not auteur:
        raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {book.auteur_id} non trouvé")

    # Vérifier que l'ISBN n'existe pas déjà
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")

    nombre_exemplaires_disponibles = book.nombre_exemplaires_disponibles
    if nombre_exemplaires_disponibles is None:
        nombre_exemplaires_disponibles = book.nombre_exemplaires_total

    if nombre_exemplaires_disponibles > book.nombre_exemplaires_total:
        raise HTTPException(
            status_code=400,
            detail="Le nombre d'exemplaires disponibles ne peut pas dépasser le total"
        )

    new_livre = Book(
        titre=book.titre,
        isbn=book.isbn,
        annee_publication=book.annee_publication,
        auteur_id=book.auteur_id,
        nombre_exemplaires_disponibles=nombre_exemplaires_disponibles,
        nombre_exemplaires_total=book.nombre_exemplaires_total,
        categorie=book.categorie,
        langue=book.langue,
        nombre_pages=book.nombre_pages,
        maison_edition=book.maison_edition
    )

    db.add(new_livre)
    db.commit()
    db.refresh(new_livre)

    return {
        "message": "Livre ajouté avec succès",
        "livre_id": new_livre.id,
        "livre": {
            "id": new_livre.id,
            "titre": new_livre.titre,
            "isbn": new_livre.isbn
        }
    }

@router.put("/{livre_id}")
def update_book(
    livre_id: int,
    book: BookUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """Mettre à jour un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    # Si on change l'auteur, vérifier qu'il existe
    if book.auteur_id is not None:
        auteur = db.query(Author).filter(Author.id == book.auteur_id).first()
        if not auteur:
            raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {book.auteur_id} non trouvé")
        livre.auteur_id = book.auteur_id

    # Mise à jour des champs
    if book.titre is not None:
        livre.titre = book.titre
    if book.isbn is not None:
        existing = db.query(Book).filter(Book.isbn == book.isbn, Book.id != livre_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Un autre livre avec cet ISBN existe déjà")
        livre.isbn = book.isbn
    if book.annee_publication is not None:
        livre.annee_publication = book.annee_publication
    if book.categorie is not None:
        livre.categorie = book.categorie
    if book.langue is not None:
        livre.langue = book.langue
    if book.nombre_pages is not None:
        livre.nombre_pages = book.nombre_pages
    if book.maison_edition is not None:
        livre.maison_edition = book.maison_edition

    # Gestion des exemplaires
    if book.nombre_exemplaires_total is not None:
        livre.nombre_exemplaires_total = book.nombre_exemplaires_total
    if book.nombre_exemplaires_disponibles is not None:
        livre.nombre_exemplaires_disponibles = book.nombre_exemplaires_disponibles
    
    # Vérifier la contrainte
    if livre.nombre_exemplaires_disponibles > livre.nombre_exemplaires_total:
        raise HTTPException(
            status_code=400,
            detail="Le nombre d'exemplaires disponibles ne peut pas dépasser le total"
        )
    
    db.commit()
    db.refresh(livre)
    
    return {
        "message": f"Livre {livre_id} mis à jour avec succès",
        "livre": {
            "id": livre.id,
            "titre": livre.titre,
            "isbn": livre.isbn
        }
    }

@router.delete("/{livre_id}")
def delete_book(livre_id: int, db: Session = Depends(get_db)):
    """Supprimer un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    try:
        db.delete(livre)
        db.commit()
        return {"message": f"Livre {livre_id} supprimé avec succès"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer ce livre (il est peut-être lié à des emprunts)"
        )