app = FastAPI()

app.include_router(products_router, prefix="/api/v1")
# app.include_router(auth_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
