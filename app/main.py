from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import authors, book, loans  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Bibliothèque",
    description="Système de gestion de bibliothèque",
    version="1.0.0"
)

#app.include_router(authors.router) 
app.include_router(book.router)     
app.include_router(loans.router)  

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API Bibliothèque! 📚\n",
        "documentation": {
            "swagger_ui": "http://127.0.0.1:8000/docs",
        },
    }