from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)  # مثل BTC أو AAPL
    asset_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # علاقة عكسية مع المستخدم
    owner = relationship("User", back_populates="assets")