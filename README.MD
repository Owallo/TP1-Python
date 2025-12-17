# API Bibliothèque 📚

Système de gestion de bibliothèque REST API construit avec FastAPI et SQLAlchemy.

## Fonctionnalités

- ✅ Gestion des auteurs (CRUD)
- ✅ Gestion des livres 
- ✅ Gestion des emprunts
- ✅ Historique des emprunts
- ✅ Base de données SQLite

## Installation

### Prérequis
- Python 3.8+
- pip

### Important ⚠️
Renommer le dossier `App` en `app` (minuscules) pour éviter les problèmes

### Étapes

1. **Cloner le projet**
```bash
git clone https://github.com/Owallo/TP1-Python.git
cd TP1-Python
```

2. **Créer un environnement virtuel**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
```

3. **Installer les dépendances**
```bash
pip install -r requirement.txt
```

## Utilisation

### Démarrer le serveur
```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur: `http://127.0.0.1:8000`

### Documentation interactive
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Structure du projet

```
TP1-Python/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── models.py            # Modèles SQLAlchemy
│   ├── database.py          # Configuration BD
│   ├── routers/
│   │   ├── authors.py       # Endpoints auteurs
│   │   ├── book.py          # Endpoints livres
│   │   └── loans.py         # Endpoints emprunts
│   └── schemas/
│       └── item.py          # Schémas Pydantic
├── requirement.txt          # Dépendances
└── README.MD                # Ce fichier
```

## Endpoints

### Auteurs
- `GET /authors/` - Lister tous les auteurs
- `GET /authors/{id}` - Obtenir un auteur par ID
- `POST /authors/` - Créer un nouvel auteur
- `PUT /authors/{id}` - Mettre à jour un auteur
- `DELETE /authors/{id}` - Supprimer un auteur

### Livres
- `GET /books/` - Lister tous les livres
- `GET /books/{id}` - Obtenir un livre par ID
- `POST /books/` - Créer un livre
- `PUT /books/{id}` - Mettre à jour un livre
- `DELETE /books/{id}` - Supprimer un livre

### Emprunts
- `GET /loans/` - Lister tous les emprunts
- `POST /loans/` - Créer un emprunt
- `PUT /loans/{id}` - Mettre à jour un emprunt

## Technologies utilisées

- **FastAPI** - Framework web moderne pour APIs REST
- **Uvicorn** - Serveur ASGI
- **SQLAlchemy** - ORM Python
- **Pydantic** - Validation de données
- **SQLite** - Base de données
- **Alembic** - Gestion des migrations BD
- **python-dotenv** - Gestion des variables d'environnement

## Développement

### Variables d'environnement
Créer un fichier `.env` à la racine:
```
DATABASE_URL=sqlite:///bibliotheque.db
```

## Licence

MIT
