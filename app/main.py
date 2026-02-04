from fastapi import FastAPI
from app.api.v1 import products
from app.api.v1 import search

app = FastAPI()

# Роуты API v1
app.include_router(products.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
