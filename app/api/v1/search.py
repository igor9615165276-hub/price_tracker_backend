from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

router = APIRouter(prefix="/search", tags=["search"])


class OfferOut(BaseModel):
    platform: str
    url: HttpUrl
    price: float
    currency: str
    delivery_price: float
    total_price: float
    in_stock: bool


class ProductBriefOut(BaseModel):
    id: int
    title: str
    image_url: Optional[str] = None
    attributes: Optional[dict] = None


class SearchResultOut(BaseModel):
    product: ProductBriefOut
    offers: List[OfferOut]
    best_offer_platform: str


class SearchRequest(BaseModel):
    query: str
    type: str  # "url" или "text"


@router.post("", response_model=SearchResultOut)
async def search_products(payload: SearchRequest):
    # ВРЕМЕННЫЙ мок, чтобы Flutter уже работал.
    # Потом сюда подставишь реальный парсинг WB/Ozon и сравнение.
    dummy_product = ProductBriefOut(
        id=1,
        title="Тестовый товар",
        image_url=None,
        attributes={"brand": "Test", "volume_ml": 500},
    )

    offers = [
        OfferOut(
            platform="wb",
            url="https://www.wildberries.ru/catalog/...",
            price=1200.0,
            currency="RUB",
            delivery_price=0.0,
            total_price=1200.0,
            in_stock=True,
        ),
        OfferOut(
            platform="ozon",
            url="https://www.ozon.ru/product/...",
            price=1100.0,
            currency="RUB",
            delivery_price=149.0,
            total_price=1249.0,
            in_stock=True,
        ),
    ]

    best_platform = min(offers, key=lambda o: o.total_price).platform

    return SearchResultOut(
        product=dummy_product,
        offers=offers,
        best_offer_platform=best_platform,
    )
