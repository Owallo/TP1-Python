import pytest
from app.models import Base
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """"Client de test pour l'application FastAPI."""
    return TestClient(app)

@pytest.fixture
def sample_author():
    """Données d'auteur d'exemple pour les tests."""
    return {
        "nom": "Doe",
        "prenom": "John",
        "nationalite": "FR",
        "date_naissance": "1980-01-01",
    }
    
@pytest.fixture
def db_session():
    """"Session de base de données pour les tests."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    session.close()
    
def test_create_author(client, sample_author):
    """Test de la création d'un auteur."""
    response = client.post("/authors/add", params=sample_author)
    assert response.status_code == 200
    data = response.json()
    assert "auteur_id" in data
    assert data["message"] == "Auteur ajouté avec succès."