from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.utils.db import Base

class Airport(Base):
    __tablename__ = 'Airport'

    airp_id = Column(Integer, primary_key=True, index=True)
    airport_name = Column(String, unique=True)
    country = Column(String)
    city = Column(String)

    departures = relationship(
        "Flights",
        foreign_keys="Flights.dep_air_id",
        back_populates="departure_airport"
    )

    arrivals = relationship(
        "Flights",
        foreign_keys="Flights.arr_air_id",
        back_populates="arrival_airport"
    )