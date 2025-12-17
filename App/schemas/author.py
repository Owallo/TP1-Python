from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr, model_validator

class AuteurCreate(BaseModel):
    prenom: str = Field(..., min_length=1, max_length=100)
    nom: str = Field(..., min_length=1, max_length=100)
    nationalite: Optional[str] = Field(None, min_length=2, max_length=2)
    date_naissance: Optional[date] = None
    
class AuteurUpdate(BaseModel):
    prenom: Optional[str] = Field(None, min_length=1, max_length=100)
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    date_naissance: Optional[date] = None

class AuteurDelete(BaseModel):
    pass

class AuteurGet(BaseModel):
    id: int
    prenom: str
    nom: str
    nationalite: Optional[str] = None
    date_naissance: Optional[date] = None
    livres: List[LivreGet] = []

    class Config:
        from_attributes = True

class LivreGet(BaseModel):
    id: int
    titre: str
    isbn: str
    categorie: str
    langue: str
    maison_edition: str
    nombre_pages: int
    annee_publication: int
    nombre_exemplaires_total: int
    nombre_exemplaires_disponibles: int
    auteur_id: int

    class Config:
        from_attributes = True