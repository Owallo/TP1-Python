from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import Book, Author
from typing import Optional

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


@router.get("/")
def get_books(
    page: int = 1, 
    page_size: int = 5,
    sort_by: str = "titre",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des livres avec pagination et tri
    
    Paramètres:
    - page: numéro de page (défaut: 1)
    - page_size: nombre de livres par page (défaut: 5)
    - sort_by: trier par 'titre', 'auteur', 'annee_publication' ou 'popularite' (défaut: titre)
    - order: 'asc' (croissant) ou 'desc' (décroissant) (défaut: asc)
    """
    # Pagination
    offset = (page - 1) * page_size
    query = db.query(Book)
    
    # Tri simple
    if sort_by == "titre":
        if order == "desc":
            query = query.order_by(Book.titre.desc())
        else:
            query = query.order_by(Book.titre)
    elif sort_by == "annee_publication":
        if order == "desc":
            query = query.order_by(Book.annee_publication.desc())
        else:
            query = query.order_by(Book.annee_publication)
    
    total = query.count()
    
    # Appliquer pagination
    livres = query.offset(offset).limit(page_size).all()
    
    # Calculer les pages
    pages = (total + page_size - 1) // page_size
    
    return {
        "livres": [
            {
                "id": livre.id,
                "titre": livre.titre,
                "isbn": livre.isbn,
                "annee_publication": livre.annee_publication,
                "auteur": f"{livre.auteur.prenom} {livre.auteur.nom}" if livre.auteur else "Inconnu",
                "auteur_id": livre.auteur_id,
                "nombre_exemplaires_disponibles": livre.nombre_exemplaires_disponibles,
                "nombre_exemplaires_total": livre.nombre_exemplaires_total,
                "categorie": livre.categorie,
                "langue": livre.langue
            } 
            for livre in livres
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

@router.get("/search")
def search_books(
    page: int = 1,
    page_size: int = 5,
    titre: Optional[str] = None,
    auteur: Optional[str] = None,
    isbn: Optional[str] = None,
    categorie: Optional[str] = None,
    annee: Optional[int] = None,
    annee_min: Optional[int] = None,
    annee_max: Optional[int] = None,
    langue: Optional[str] = None,
    disponible: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Recherche avancée de livres avec filtres multiples (combinaison ET)
    
    Paramètres:
    - titre: recherche partielle insensible à la casse
    - auteur: recherche par nom/prénom (partielle)
    - isbn: recherche exacte
    - categorie: recherche exacte
    - annee: année exacte
    - annee_min/annee_max: plage d'années
    - langue: recherche exacte
    - disponible: True si disponible, False si non disponible
    - page, page_size: pagination
    """
    conditions = []
    
    if titre:
        conditions.append(Book.titre(f"%{titre}%"))
    
    # Recherche par auteur (nom ou prénom)
    if auteur:
        conditions.append(
            Book.auteur.has(
                Author.nom(f"%{auteur}%") | Author.prenom(f"%{auteur}%")
            )
        )
    
    # Recherche par ISBN exact
    if isbn:
        conditions.append(Book.isbn == isbn)
    
    # Recherche par catégorie exacte
    if categorie:
        conditions.append(Book.categorie == categorie)
    
    # Recherche par année exacte
    if annee:
        conditions.append(Book.annee_publication == annee)
    
    # Recherche par plage d'années
    if annee_min:
        conditions.append(Book.annee_publication >= annee_min)
    if annee_max:
        conditions.append(Book.annee_publication <= annee_max)
    
    # Recherche par langue exacte
    if langue:
        conditions.append(Book.langue == langue)
    
    # Filtrage par disponibilité
    if disponible is not None:
        if disponible:
            # Livres disponibles (au moins 1 exemplaire)
            conditions.append(Book.nombre_exemplaires_disponibles > 0)
        else:
            # Livres non disponibles (0 exemplaire)
            conditions.append(Book.nombre_exemplaires_disponibles == 0)
    
    # Combiner toutes les conditions avec ET
    query = db.query(Book)
    if conditions:
        query = query.filter(and_(*conditions))
    
    total = query.count()
    
    offset = (page - 1) * page_size
    livres = query.offset(offset).limit(page_size).all()
    
    pages = (total + page_size - 1) // page_size
    
    return {
        "livres": [
            {
                "id": livre.id,
                "titre": livre.titre,
                "isbn": livre.isbn,
                "annee_publication": livre.annee_publication,
                "auteur": f"{livre.auteur.prenom} {livre.auteur.nom}" if livre.auteur else "Inconnu",
                "auteur_id": livre.auteur_id,
                "nombre_exemplaires_disponibles": livre.nombre_exemplaires_disponibles,
                "nombre_exemplaires_total": livre.nombre_exemplaires_total,
                "categorie": livre.categorie,
                "langue": livre.langue
            } 
            for livre in livres
        ],
        "page_courante": page,
        "taille_page": page_size,
        "total": total,
        "pages_totales": pages
    }

@router.get("/{livre_id}")
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
        "auteur": f"{livre.auteur.prenom} {livre.auteur.nom}" if livre.auteur else "Inconnu",
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
    titre: str,
    isbn: str,
    annee_publication: int,
    auteur_id: int,
    nombre_exemplaires_total: int,
    categorie: str,
    langue: str,
    nombre_pages: int,
    maison_edition: str,
    nombre_exemplaires_disponibles: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Ajouter un nouveau livre"""
    # Vérifier que l'auteur existe
    auteur = db.query(Author).filter(Author.id == auteur_id).first()
    if not auteur:
        raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {auteur_id} non trouvé")
    
    # Vérifier que l'ISBN n'existe pas déjà
    existing_book = db.query(Book).filter(Book.isbn == isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")
    
    
    # Vérifier la contrainte
    if nombre_exemplaires_disponibles > nombre_exemplaires_total:
        raise HTTPException(
            status_code=400, 
            detail="Le nombre d'exemplaires disponibles ne peut pas dépasser le total"
        )
    
    new_livre = Book(
        titre=titre,
        isbn=isbn,
        annee_publication=annee_publication,
        auteur_id=auteur_id,
        nombre_exemplaires_disponibles=nombre_exemplaires_disponibles,
        nombre_exemplaires_total=nombre_exemplaires_total,
        categorie=categorie,
        langue=langue,
        nombre_pages=nombre_pages,
        maison_edition=maison_edition
    )
    
    db.add(new_livre)
    db.commit()
    db.refresh(new_livre)
    
    return {
        "statut": "succès",
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
    titre: Optional[str] = None,
    isbn: Optional[str] = None,
    annee_publication: Optional[int] = None,
    auteur_id: Optional[int] = None,
    nombre_exemplaires_disponibles: Optional[int] = None,
    nombre_exemplaires_total: Optional[int] = None,
    categorie: Optional[str] = None,
    langue: Optional[str] = None,
    nombre_pages: Optional[int] = None,
    maison_edition: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Mettre à jour un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    # Si on change l'auteur, vérifier qu'il existe
    if auteur_id is not None:
        auteur = db.query(Author).filter(Author.id == auteur_id).first()
        if not auteur:
            raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {auteur_id} non trouvé")
        livre.auteur_id = auteur_id
    
    # Mise à jour des champs
    if titre is not None:
        livre.titre = titre
    if isbn is not None:
        # Vérifier que le nouvel ISBN n'existe pas déjà
        existing = db.query(Book).filter(Book.isbn == isbn, Book.id != livre_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Un autre livre avec cet ISBN existe déjà")
        livre.isbn = isbn
    if annee_publication is not None:
        livre.annee_publication = annee_publication
    if categorie is not None:
        livre.categorie = categorie
    if langue is not None:
        livre.langue = langue
    if nombre_pages is not None:
        livre.nombre_pages = nombre_pages
    if maison_edition is not None:
        livre.maison_edition = maison_edition
    
    # Gestion des exemplaires
    if nombre_exemplaires_total is not None:
        livre.nombre_exemplaires_total = nombre_exemplaires_total
    if nombre_exemplaires_disponibles is not None:
        livre.nombre_exemplaires_disponibles = nombre_exemplaires_disponibles
    
    # Vérifier la contrainte
    if livre.nombre_exemplaires_disponibles > livre.nombre_exemplaires_total:
        raise HTTPException(
            status_code=400,
            detail="Le nombre d'exemplaires disponibles ne peut pas dépasser le total"
        )
    
    db.commit()
    db.refresh(livre)
    
    return {
        "statut": "succès",
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
        return {
            "statut": "succès",
            "message": f"Livre {livre_id} supprimé avec succès"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer ce livre (il est peut-être lié à des emprunts)"
        )