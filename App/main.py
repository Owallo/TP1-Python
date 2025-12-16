from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Mon API",
    description="API de démonstration Python",
    version="1.0.0"
)

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "message": "Item créé avec succès"}