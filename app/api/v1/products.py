from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.schemas.price_snapshot import PriceSnapshotOut
from app.api.deps import get_current_user  # если у тебя уже есть такой деп

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductOut)
async def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # если делаешь auth
):
    # TODO:
    # 1) определить платформу по URL (wb / ozon)
    # 2) дернуть парсер (wb или ozon) -> title, price, image
    # 3) создать Product + первый PriceSnapshot
    raise NotImplementedError("add_product not implemented yet")


@router.get("/", response_model=List[ProductOut])
async def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: вернуть все товары юзера + last price
    return []


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: вернуть конкретный товар
    raise NotImplementedError("get_product not implemented yet")


@router.get("/{product_id}/history", response_model=List[PriceSnapshotOut])
async def get_price_history(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: вернуть историю цен по товару
    return []


@router.get("/{product_id}/compare")
async def compare_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: найти аналог на другой платформе и отдать {wb_price, ozon_price, diff}
    raise NotImplementedError("compare_product not implemented yet")
