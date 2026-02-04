from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import products
from app.api.v1 import search

app = FastAPI()

# Разрешаем запросы с клиента (Flutter на эмуляторе/устройстве/вебе)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на время разработки можно *; позже сузим
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
