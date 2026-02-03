class PriceSnapshotOut(BaseModel):
    taken_at: datetime
    price: Decimal
