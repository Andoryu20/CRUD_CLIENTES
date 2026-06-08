from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config import Base

class Client(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name_client = Column(String, unique=True, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    user_created = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    #Check dates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #Foreign keys
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    #Client relation Country/Category
    country = relationship("Country", back_populates="clients")
    category = relationship("Category", back_populates="clients")

    