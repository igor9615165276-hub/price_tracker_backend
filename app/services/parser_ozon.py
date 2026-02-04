import re
from dataclasses import dataclass
from typing import Optional

import httpx
from bs4 import BeautifulSoup


@dataclass
class ParsedProduct:
    title: str
    price: float
    currency: str
    image_url: Optional[str]
    url: str


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
}


async def fetch_ozon_product(url: str) -> ParsedProduct:
    """
    Очень упрощённый парсер карточки Ozon по прямой ссылке на товар.
    Для MVP: вытаскиваем title, price, image_url.
    """
    async with httpx.AsyncClient(
    headers=HEADERS,
    timeout=10,
    follow_redirects=True,  # важно
) as client:
    resp = await client.get(url)
    # без raise_for_status, чтобы не падать на 3xx/4xx, а обработать сами
    if resp.status_code >= 400:
        # можешь залогировать resp.status_code и часть resp.text
        raise RuntimeError(f"Ozon returned HTTP {resp.status_code}")
    html = resp.text


    soup = BeautifulSoup(html, "lxml")

    # Title
    # Ozon часто рендерит название в <h1> или <h1 ... data-widget="webProductHeading">
    title_tag = soup.find("h1")
    if not title_tag:
        # запасной вариант
        title_tag = soup.select_one("h1[data-widget='webProductHeading']")
    title = title_tag.get_text(strip=True) if title_tag else "Без названия"

    # Price (сильно зависит от текущей вёрстки, нужен гибкий селектор)
    price_text = None

    # Попробуем несколько селекторов
    selectors = [
        "span[data-test-id='tile-price']",
        "span[data-widget='webPrice']",
        "div[data-widget='webCurrentPrice'] span",
        "span[class*='price']",  # fallback: любые price-элементы
    ]
    for sel in selectors:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            price_text = el.get_text(strip=True)
            break

    if not price_text:
        # если не нашли цену — считаем, что 0
        price_value = 0.0
    else:
        # вытащить только цифры
        digits = re.sub(r"[^\d]", "", price_text)
        price_value = float(digits) if digits else 0.0

    # Валюта — для РФ это почти всегда RUB
    currency = "RUB"

    # Image URL — часто в og:image
    og_image = soup.find("meta", property="og:image")
    image_url = og_image["content"] if og_image and og_image.get("content") else None

    return ParsedProduct(
        title=title,
        price=price_value,
        currency=currency,
        image_url=image_url,
        url=url,
    )
