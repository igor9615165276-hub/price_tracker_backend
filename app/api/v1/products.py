from typing import List

from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[dict])
async def list_products():
    # Временная заглушка, чтобы сервис стартовал
    return []
