class ProductCreate(BaseModel):
    url: HttpUrl

class ProductOut(BaseModel):
    id: int
    url: HttpUrl
    platform: str
    title: str
    image_url: str | None
    current_price: Decimal | None

    class Config:
        orm_mode = True
