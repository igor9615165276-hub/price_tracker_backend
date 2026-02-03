class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
