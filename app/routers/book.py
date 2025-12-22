from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import Book, Author
from app.schemas.book import BookCreate, BookUpdate, BookGet, BookGet_All
from typing import Optional

router = APIRouter(
    prefix="/books",
    tags=["Livres"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=BookGet_All)
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
        "livres": livres,
        "page_courante": page,
        "taille_page": page_size,
        "total": total,
        "pages_totales": pages,
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
        "livres": livres,
        "page_courante": page,
        "taille_page": page_size,
        "total": total,
        "pages_totales": pages
    }

@router.get("/{livre_id}", response_model=BookGet)
def get_book(livre_id: int, db: Session = Depends(get_db)):
    """Récupérer les détails d'un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    return livre

@router.post("/add", response_model=BookGet)
def create_book(
    livre: BookCreate,
    db: Session = Depends(get_db)
):
    """Ajouter un nouveau livre"""
    # Vérifier que l'auteur existe
    auteur = db.query(Author).filter(Author.id == livre.auteur_id).first()
    if not auteur:
        raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {livre.auteur_id} non trouvé")
    
    # Vérifier que l'ISBN n'existe pas déjà
    existing_book = db.query(Book).filter(Book.isbn == livre.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")
    
    
    # Vérifier la contrainte
    if livre.nombre_exemplaires_disponibles > livre.nombre_exemplaires_total:
        raise HTTPException(
            status_code=400, 
            detail="Le nombre d'exemplaires disponibles ne peut pas dépasser le total"
        )
    
    new_livre = Book(
        titre=livre.titre,
        isbn=livre.isbn,
        annee_publication=livre.annee_publication,
        auteur_id=livre.auteur_id,
        nombre_exemplaires_disponibles=livre.nombre_exemplaires_disponibles,
        nombre_exemplaires_total=livre.nombre_exemplaires_total,
        categorie=livre.categorie,
        langue=livre.langue,
        nombre_pages=livre.nombre_pages,
        maison_edition=livre.maison_edition
    )
    
    db.add(new_livre)
    db.commit()
    db.refresh(new_livre)
    
    return new_livre

@router.put("/{livre_id}", response_model=BookGet)
def update_book(
    livre_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un livre"""
    livre = db.query(Book).filter(Book.id == livre_id).first()
    
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    # Si on change l'auteur, vérifier qu'il existe
    if livre_id is not None:
        auteur = db.query(Author).filter(Author.id == livre.auteur_id).first()
        if not auteur:
            raise HTTPException(status_code=404, detail=f"Auteur avec l'ID {livre.auteur_id} non trouvé")
        livre.auteur_id = livre.auteur_id
    
    # Mise à jour des champs
    if book.titre is not None:
        livre.titre = book.titre
    if book.isbn is not None:
        # Vérifier que le nouvel ISBN n'existe pas déjà
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
    
    return livre

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