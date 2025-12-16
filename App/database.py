from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base de données SQLite (fichier local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./bibliotheque.db"

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # obligatoire pour SQLite
)

# Session de base de données
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Classe de base pour les modèles
Base = declarative_base()


# Dépendance FastAPI pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
