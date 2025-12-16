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

# Inclusion des routers
app.include_router(authors.rooter)
# app.include_router(book.root)
# app.include_router(loans.root)

@app.get("/")
def root():
    return {"message": "API Bibliothèque "}
