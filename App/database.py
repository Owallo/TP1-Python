from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Créer l'engine SQLite
engine = create_engine(
    "sqlite:///bibliotheque.db",
    connect_args={"check_same_thread": False}
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)