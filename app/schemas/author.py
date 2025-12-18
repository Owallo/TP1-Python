from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr, model_validator, field_validator

class AuteurCreate(BaseModel):
    prenom: str = Field(..., min_length=1, max_length=100, description="Prénom de l'auteur")
    nom: str = Field(..., min_length=1, max_length=100, description="Nom de famille de l'auteur")
    nationalite: Optional[str] = Field(None, min_length=2, max_length=2, description="Code pays ISO (FR, EN, ES, etc.)")
    date_naissance: Optional[date] = Field(None, description="Date de naissance (format: YYYY-MM-DD)")
    
    #===============================
    # Validateurs
    #===============================
    
    @field_validator('prenom', 'nom')
    @classmethod
    def validate_nom_prenom(cls, v: str) -> str:
        """Vérifie que le nom/prénom n'est pas vide"""
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('date_naissance')
    @classmethod
    def validate_date_naissance(cls, v: date) -> date:
        """Vérifie que la date n'est pas dans le futur"""
        if v > date.today():
            raise ValueError('Date ne peut pas être dans le futur')
        return v

    @field_validator('nationalite')
    @classmethod
    def validate_nationalite(cls, v: str) -> str:
        """Vérifie le code pays"""
        codes_valides = {
            "FR", "EN", "ES", "DE", "IT", "JP", "CN", "US", "CA", "AU",
            "BR", "MX", "RU", "CH", "NL", "BE", "AT", "SE", "NO", "DK"
        }
        if v.upper() not in codes_valides:
            raise ValueError(f'Code pays invalide: {v}. Valides: {", ".join(sorted(codes_valides))}')
        return v.upper()
    

class AuteurUpdate(BaseModel):
    prenom: Optional[str] = Field(None, min_length=1, max_length=100)
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    nationalite : Optional[str] = Field(None, min_length=2, max_length=2)
    date_naissance: Optional[date] = None
    
    @field_validator('prenom', 'nom')
    @classmethod
    def validate_nom_prenom(cls, v: str) -> str:
        """Vérifie que le nom/prénom n'est pas vide"""
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('date_naissance')
    @classmethod
    def validate_date_naissance(cls, v: date) -> date:
        """Vérifie que la date n'est pas dans le futur"""
        if v > date.today():
            raise ValueError('Date ne peut pas être dans le futur')
        return v

    @field_validator('nationalite')
    @classmethod
    def validate_nationalite(cls, v: str) -> str:
        """Vérifie le code pays"""
        codes_valides = {
            "FR", "EN", "ES", "DE", "IT", "JP", "CN", "US", "CA", "AU",
            "BR", "MX", "RU", "CH", "NL", "BE", "AT", "SE", "NO", "DK"
        }
        if v.upper() not in codes_valides:
            raise ValueError(f'Code pays invalide: {v}. Valides: {", ".join(sorted(codes_valides))}')
        return v.upper()

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