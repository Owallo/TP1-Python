from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, Enum, CheckConstraint, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship
import enum



class CategorieEnum(str, enum.Enum):
    """Énumération des catégories littéraires"""
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTOIRE = "Histoire"
    PHILOSOPHIE = "Philosophie"


class StatutEmpruntEnum(str, enum.Enum):
    """Énumération des statuts d'emprunt"""
    ACTIF = "Actif"
    RETOURNE = "Retourné"
    EN_RETARD = "En retard"


class Author(Base):
    """Modèle Auteur"""
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)
    nationalite = Column(String(2), nullable=False)  # Code ISO
    
    # Relationships
    livres = relationship("Book", back_populates="auteur")
    
    # Contraintes
    __table_args__ = (
        UniqueConstraint('prenom', 'nom', name='uq_author_full_name'),
    )


class Book(Base):
    """Modèle Livre"""
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False, index=True)
    isbn = Column(String(17), unique=True, nullable=False, index=True)  # Format ISBN-13
    annee_publication = Column(Integer, nullable=False)
    nombre_exemplaires_disponibles = Column(Integer, nullable=False)
    nombre_exemplaires_total = Column(Integer, nullable=False)
    categorie = Column(String(50), nullable=False)  # CategorieEnum
    langue = Column(String(50), nullable=False)
    nombre_pages = Column(Integer, nullable=False)
    maison_edition = Column(String(255), nullable=False)
    
    # Foreign Key
    auteur_id = Column(Integer, ForeignKey("author.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # Relationships
    auteur = relationship("Author", back_populates="livres")
    emprunts = relationship("Loan", back_populates="livre", cascade="restrict")
    
    # Contraintes
    __table_args__ = (
        CheckConstraint('nombre_exemplaires_disponibles <= nombre_exemplaires_total', name='ck_exemplaires_dispo_lte_total'),
    )


class Loan(Base):
    """Modèle Emprunt"""
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    nom_emprunteur = Column(String(255), nullable=False)
    email_emprunteur = Column(String(255), nullable=False)
    numero_carte_bibliotheque = Column(String(50), unique=True, nullable=False, index=True)
    date_emprunt = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_limite_retour = Column(DateTime, nullable=False)
    date_retour_effectif = Column(DateTime, nullable=True)
    statut = Column(String(20), nullable=False)  # StatutEmpruntEnum
    commentaires = Column(Text, nullable=True)
    
    # Foreign Key
    livre_id = Column(Integer, ForeignKey("book.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # Relationships
    livre = relationship("Book", back_populates="emprunts")
    
    # Contraintes
    __table_args__ = (
        CheckConstraint('date_retour_effectif IS NULL OR date_retour_effectif >= date_emprunt', name='ck_loan_retour_apres_loan'),
    )


class LoanHistory(Base):
    """Modèle Historique des emprunts"""
    __tablename__ = "loan_history"

    id = Column(Integer, primary_key=True, index=True)
    livre_id = Column(Integer, ForeignKey("book.id"), nullable=False, index=True)
    nombre_emprunts_total = Column(Integer, nullable=False, default=0)
    duree_moyenne_emprunt = Column(Integer, nullable=True)  # en jours
    popularite = Column(Integer, nullable=False, default=0)
