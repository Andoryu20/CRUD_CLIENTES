from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    clients = relationship("Client", back_populates="country")