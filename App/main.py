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

# # Inclusion des routers
# app.include_router(authors.root, prefix="/authors", tags=["Authors"])
# app.include_router(book.root, prefix="/books", tags=["Books"])
# app.include_router(loans.root, prefix="/loans", tags=["Loans"])

@app.get("/")
def root():
    return {"message": "API Bibliothèque "}
