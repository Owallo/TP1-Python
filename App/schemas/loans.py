from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr, model_validator

class LoansCreate(BaseModel):
    id: int = Field(..., ge=1)
    nom_emprunteur: str = Field(..., min_length=1, max_length=255)
    email_emprunteur: EmailStr = Field(...)
    numero_carte_bibliotheque: str = Field(..., min_length=1, max_length=50)
    date_emprunt: datetime = Field(default_factory=datetime.utcnow)
    date_limite_retour: datetime = Field(...)
    date_retour_effectif: Optional[datetime] = None
    statut: str = Field(..., min_length=1, max_length=20)
    commentaires: Optional[str] = None
    livre_id: int = Field(..., ge=1)

class LoansUpdate(BaseModel):
    nom_emprunteur: Optional[str] = Field(None, min_length=1, max_length=255)
    email_emprunteur: Optional[EmailStr] = None
    numero_carte_bibliotheque: Optional[str] = Field(None, min_length=1, max_length=50)
    date_emprunt: Optional[datetime] = None
    date_limite_retour: Optional[datetime] = None
    date_retour_effectif: Optional[datetime] = None
    statut: Optional[str] = Field(None, min_length=1, max_length=20)
    commentaires: Optional[str] = None
    livre_id: Optional[int] = Field(None, ge=1)

class LoansDelete(BaseModel):
    pass

class LoansGet(BaseModel):
    id: int = Field(..., ge=1)