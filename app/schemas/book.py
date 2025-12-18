from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr, model_validator, field_validator

class BookCreate(BaseModel):
    titre: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=17)
    annee_publication: int = Field(..., ge=0)
    nombre_exemplaires_disponibles: int = Field(..., ge=0)
    nombre_exemplaires_total: int = Field(..., ge=0)
    categorie: str = Field(..., min_length=1, max_length=50)
    langue: str = Field(..., min_length=1, max_length=50)
    nombre_pages: int = Field(..., ge=1)
    maison_edition: str = Field(..., min_length=1, max_length=255)
    auteur_id: int = Field(..., ge=1)
    
    #===============================
    # Validateurs
    #===============================
    
    @field_validator('titre', 'categorie', 'langue', 'maison_edition')
    @classmethod
    def validate_strings(cls, v: str) -> str:
        """Vérifie que la chaine de caracteres n'est pas vide"""
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        """Vérifie le format ISBN (10 ou 13 chiffres, tirets optionnels)"""
        isbn_cleaned = v.replace('-', '').replace(' ', '')
        if not isbn_cleaned.isdigit():
            raise ValueError('ISBN doit contenir uniquement des chiffres (tirets optionnels)')
        if len(isbn_cleaned) not in [10, 13]:
            raise ValueError('ISBN doit avoir 10 ou 13 chiffres')
        return v.strip()
        
class BookUpdate(BaseModel):
    titre: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    annee_publication: Optional[int] = Field(None, ge=0)
    nombre_exemplaires_disponibles: Optional[int] = Field(None, ge=0)
    nombre_exemplaires_total: Optional[int] = Field(None, ge=0)
    categorie: Optional[str] = Field(None, min_length=1, max_length=50)
    langue: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre_pages: Optional[int] = Field(None, ge=1)
    maison_edition: Optional[str] = Field(None, min_length=1, max_length=255)
    auteur_id: Optional[int] = Field(None, ge=1)
    
    #===============================
    # Validateurs
    #===============================
    
    @field_validator('titre', 'categorie', 'langue', 'maison_edition')
    @classmethod
    def validate_strings(cls, v: Optional[str]) -> Optional[str]:
        """Vérifie que la chaine de caracteres n'est pas vide"""
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        """Vérifie le format ISBN (10 ou 13 chiffres, tirets optionnels)"""
        if v is None:
            return v
        isbn_cleaned = v.replace('-', '').replace(' ', '')
        if not isbn_cleaned.isdigit():
            raise ValueError('ISBN doit contenir uniquement des chiffres (tirets optionnels)')
        if len(isbn_cleaned) not in [10, 13]:
            raise ValueError('ISBN doit avoir 10 ou 13 chiffres')
        return v.strip()

class BookDelete(BaseModel):
    pass

class BookGet(BaseModel):
    titre: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = None#Field(..., min_length=10, max_length=17)
    annee_publication: int = Field(..., ge=0)
    nombre_exemplaires_disponibles: int = Field(None, ge=0)
    nombre_exemplaires_total: int = Field(None, ge=0)
    categorie: str = Field(None, min_length=1, max_length=50)
    langue: str = Field(None, min_length=1, max_length=50)
    nombre_pages: int = Field(None, ge=1)
    maison_edition: str = Field(None, min_length=1, max_length=255)
    auteur_id: int = Field(None, ge=1)

    class Config:
        from_attributes = True

class BookGet_All(BaseModel):
    livres: List[BookGet] = []
    page_courante : int = None
    taille_page: int = None
    total: int = None
    pages_totales: int = None
    
    class Config:
        from_attributes = True