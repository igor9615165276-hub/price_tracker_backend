from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

from app.services.parser_ozon import fetch_ozon_product, ParsedProduct

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


def detect_platform(url: str) -> Optional[str]:
    if "ozon.ru" in url:
        return "ozon"
    if "wildberries.ru" in url:
        return "wb"
    return None


@router.post("", response_model=SearchResultOut)
async def search_products(payload: SearchRequest):
    if payload.type != "url":
        raise HTTPException(status_code=400, detail="Пока поддерживаем только поиск по ссылке")

    platform = detect_platform(payload.query)
    if platform is None:
        raise HTTPException(status_code=400, detail="Неизвестная платформа, ожидается Ozon или WB")

    offers: list[OfferOut] = []

    if platform == "ozon":
        parsed: ParsedProduct = await fetch_ozon_product(payload.query)

        product = ProductBriefOut(
            id=1,  # временно, потом возьмём из БД
            title=parsed.title,
            image_url=parsed.image_url,
            attributes={},
        )

        offers.append(
            OfferOut(
                platform="ozon",
                url=parsed.url,
                price=parsed.price,
                currency=parsed.currency,
                delivery_price=0.0,   # пока без доставки
                total_price=parsed.price,
                in_stock=True,
            )
        )

    # TODO: когда сделаем parser_wb, сюда добавим второй оффер для WB

    if not offers:
        raise HTTPException(status_code=500, detail="Не удалось получить данные о товаре")

    best_platform = min(offers, key=lambda o: o.total_price).platform

    return SearchResultOut(
        product=product,
        offers=offers,
        best_offer_platform=best_platform,
    )
