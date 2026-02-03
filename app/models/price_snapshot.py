class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Numeric(10, 2))
    currency = Column(String, default="RUB")
    taken_at = Column(DateTime, default=datetime.utcnow, index=True)
