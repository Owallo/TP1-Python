from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr, model_validator, field_validator
from fastapi import Form

class LoansCreate(BaseModel):
    nom_emprunteur: str = Field(..., min_length=1, max_length=255)
    email_emprunteur: EmailStr = Field(...)
    numero_carte_bibliotheque: str = Field(..., min_length=1, max_length=50)
    date_emprunt: date = Field(None)
    date_limite_retour: date = Field(...)
    date_retour_effectif: Optional[date] = None
    statut: str = Field(..., min_length=1, max_length=20)
    commentaires: Optional[str] = None
    livre_id: int = Field(..., ge=1)
    
    #===============================
    # Validateurs
    #===============================
    
    @field_validator('nom_emprunteur', 'numero_carte_bibliotheque', 'statut')
    @classmethod
    def validate_strings(cls, v: str) -> str:
        """Vérifie que la chaine de caracteres n'est pas vide"""
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('date_limite_retour')
    @classmethod
    def validate_date_limite_retour(cls, v: date) -> date:
        """Vérifie que la date limite est dans le futur"""
        if v < date.today():
            raise ValueError('La date limite de retour doit être dans le futur')
        return v
    
    @field_validator('date_emprunt')
    @classmethod
    def validate_date_emprunt(cls, v: date) -> date:
        """Vérifie que la date d'emprunt est dans le passé ou aujourd'hui"""
        if v > date.today():
            raise ValueError('La date d\'emprunt doit être dans le passé ou aujourd\'hui')
        return v

class LoansUpdate(BaseModel):
    nom_emprunteur: Optional[str] = Field(None, min_length=1, max_length=255)
    email_emprunteur: Optional[EmailStr] = None
    numero_carte_bibliotheque: Optional[str] = Field(None, min_length=1, max_length=50)
    date_emprunt: Optional[date] = None
    date_limite_retour: Optional[date] = None
    date_retour_effectif: Optional[date] = None
    statut: Optional[str] = Field(None, min_length=1, max_length=20)
    commentaires: Optional[str] = None
    
    #===============================
    # Validateurs
    #===============================
    
    @field_validator('nom_emprunteur', 'numero_carte_bibliotheque', 'statut')
    @classmethod
    def validate_strings(cls, v: Optional[str]) -> Optional[str]:
        """Vérifie que la chaine de caracteres n'est pas vide"""
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Ne peut pas être vide')
        return v.strip()
    
    @field_validator('date_limite_retour')
    @classmethod
    def validate_date_limite_retour(cls, v: Optional[date]) -> Optional[date]:
        """Vérifie que la date limite est dans le futur"""
        if v is None:
            return v
        if v < date.today():
            raise ValueError('La date limite de retour doit être dans le futur')
        return v

    @field_validator('date_emprunt')
    @classmethod
    def validate_date_emprunt(cls, v: date) -> date:
        """Vérifie que la date d'emprunt est dans le passé ou aujourd'hui"""
        if v > date.today():
            raise ValueError('La date d\'emprunt doit être dans le passé ou aujourd\'hui')
        return v
    
class LoansDelete(BaseModel):
    pass

class LoansGet(BaseModel):
    id: int = Field(..., ge=1)
    nom_emprunteur: str = Field(..., min_length=1, max_length=255)
    email_emprunteur: EmailStr = Field(...)
    numero_carte_bibliotheque: str = Field(..., min_length=1, max_length=50)
    date_emprunt: date = Field(default_factory=datetime.utcnow)
    date_limite_retour: date = Field(...)
    date_retour_effectif: Optional[date] = None
    statut: str = Field(..., min_length=1, max_length=20)
    commentaires: Optional[str] = None
    livre_id: int = Field(..., ge=1)

    class Config:
        from_attributes = True