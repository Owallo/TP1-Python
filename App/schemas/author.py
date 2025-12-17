from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr, model_validator

class AuteurCreate(BaseModel):
    prenom: str = Field(..., min_length=1, max_length=100)
    nom: str = Field(..., min_length=1, max_length=100)
    livres: Optional[str] = Field(None, max_length=255)
    nationalite: Optional[str] = Field(..., min_length=2, max_length=2)
    date_naissance: Optional[date] = Field(...)
    
    class Config:
        from_attributes = True
    
class AuteurUpdate(BaseModel):
    prenom: Optional[str] = Field(None, min_length=1, max_length=100)
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    livres: Optional[str] = Field(None, max_length=255)
    date_naissance: Optional[date] = None
    
    class Config:
        from_attributes = True

class AuteurDelete(BaseModel):
    pass

class AuteurGet(BaseModel):
    id: int
    prenom: str
    nom: str
    nationalite: Optional[str] = None
    #date_naissance: Optional[date] = None

    class Config:
        from_attributes = True
    

    
    