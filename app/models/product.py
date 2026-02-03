class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String, index=True)
    platform = Column(Enum("wb", "ozon", name="platform_enum"))
    title = Column(String)
    image_url = Column(String, nullable=True)
    sku = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="products")
    price_snapshots = relationship("PriceSnapshot", backref="product")
