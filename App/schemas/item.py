from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr, model_validator

class Auteur(BaseModel):
    id: int = Field(..., ge=1)
    prenom: str = Field(..., min_length=1, max_length=50)
    nom: str = Field(..., min_length=1, max_length=50)
    livres: Optional[str] = Field(None, max_length=255)
    date_naissance: Optional[date] = None