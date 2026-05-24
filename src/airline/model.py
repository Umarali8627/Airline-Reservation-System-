from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.utils.db import Base

class Airline(Base):
    __tablename__ = 'Airline'

    air_id = Column(Integer, primary_key=True, index=True)
    air_name = Column(String(50))
    model_name = Column(String, unique=True)
    country = Column(String)

    flights = relationship("Flights", back_populates="airline")