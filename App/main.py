from fastapi import FastAPI
from database import engine
from models import Base
from routers import authors, book, loans  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Bibliothèque",
    description="Système de gestion de bibliothèque",
    version="1.0.0"
)

# Inclusion des routers
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])

@app.get("/")
def root():
    return {"message": "API Bibliothèque "}
