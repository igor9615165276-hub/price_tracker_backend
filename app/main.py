from fastapi import FastAPI  # ← ЭТОГО ИМПОРТА НЕ ХВАТАЕТ

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
