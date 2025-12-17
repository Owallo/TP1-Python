from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr, model_validator

class BookBase(BaseModel):
    id: int
    titre: str
    isbn: str
    
    class Config:
        from_attributes = True
        
class BookCreate(BaseModel):
    id: int = Field(..., ge=1)
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

class BookDelete(BaseModel):
    pass

class BookGet(BaseModel):
    id: int
    titre: str
    isbn: str
    annee_publication: int
    auteur_id: int
    nombre_exemplaires_disponibles: int
    nombre_exemplaires_total: int
    categorie: Optional[str] = None
    langue: Optional[str] = None
    nombre_pages: Optional[int] = None
    maison_edition: Optional[str] = None

    class Config:
        from_attributes = True