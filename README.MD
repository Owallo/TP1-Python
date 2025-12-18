# API Bibliothèque 📚

Système complet de gestion de bibliothèque REST API construit avec **FastAPI** et **SQLAlchemy**, permettant la gestion des auteurs, livres et emprunts.

## ✨ Fonctionnalités

- ✅ **CRUD complet** pour auteurs, livres et emprunts
- ✅ **Validation des données** avec Pydantic
- ✅ **Recherche avancée** sans schéma
- ✅ **Historique des emprunts**
- ✅ **Base de données** SQLite
- ✅ **Documentation auto-générée** (Swagger & ReDoc)

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip 
- Git

### Étapes d'installation

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

## 🎯 Utilisation

### Démarrer le serveur
```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur: **http://127.0.0.1:8000**

### 📖 Documentation interactive
- **Swagger UI**: http://127.0.0.1:8000/docs (recommandé)
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📁 Structure du projet

```
TP1-Python/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application FastAPI principale
│   ├── models.py            # Modèles SQLAlchemy (ORM)
│   ├── database.py          # Configuration base de données
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── authors.py       # Endpoints gestion auteurs
│   │   ├── book.py          # Endpoints gestion livres
│   │   └── loans.py         # Endpoints gestion emprunts
│   └── schemas/
│       ├── __init__.py
│       ├── author.py        # Schémas Pydantic auteurs
│       ├── book.py          # Schémas Pydantic livres
│       ├── loans.py         # Schémas Pydantic emprunts
│       └── item.py
├── requirement.txt          # Dépendances du projet
├── .gitignore              # Fichiers ignorés par Git
└── README.MD               # Ce fichier
```

## 🔌 Endpoints API

### 👥 Auteurs
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/authors/` | Lister tous les auteurs |
| GET | `/authors/{id}` | Obtenir un auteur par ID |
| POST | `/authors/` | Créer un nouvel auteur |
| PUT | `/authors/{id}` | Mettre à jour un auteur |
| DELETE | `/authors/{id}` | Supprimer un auteur |

### 📚 Livres
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/books/` | Lister tous les livres |
| GET | `/books/{id}` | Obtenir un livre par ID |
| POST | `/books/` | Créer un livre |
| PUT | `/books/{id}` | Mettre à jour un livre |
| DELETE | `/books/{id}` | Supprimer un livre |

### 🔄 Emprunts
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/loans/` | Lister tous les emprunts |
| GET | `/loans/{id}` | Obtenir un emprunt par ID |
| POST | `/loans/` | Créer un emprunt |
| PUT | `/loans/{id}` | Mettre à jour un emprunt |
| DELETE | `/loans/{id}` | Supprimer un emprunt |

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|-------------|-------------|
| **FastAPI** | Framework web moderne pour APIs REST |
| **Uvicorn** | Serveur ASGI haute performance |
| **SQLAlchemy** | ORM Python pour la gestion de base de données |
| **Pydantic** | Validation et sérialisation de données |
| **SQLite** | Base de données légère |
| **Alembic** | Gestion des migrations de schéma |
| **python-dotenv** | Gestion des variables d'environnement |

## 📝 Notes

- La base de données est stockée dans `bibliotheque.db`
- Les fichiers cache Python (`__pycache__/`) sont ignorés par Git
- Utilisez Swagger UI pour tester l'API en développement

## 👨‍💻 Contributeurs

- **Owallo** - Développeur principal
- **AnthonyRSA69** - Développeur principal
