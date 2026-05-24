from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.db import Base

class Flights(Base):
    __tablename__ = 'Flights'

    f_id = Column(Integer, primary_key=True, index=True)

    airline_id = Column(Integer, ForeignKey('Airline.air_id'))

    dep_air_id = Column(Integer, ForeignKey('Airport.airp_id'))
    arr_air_id = Column(Integer, ForeignKey('Airport.airp_id'))

    status = Column(String, default='pending')

    arrival_time = Column(DateTime, default=datetime.now)
    departure_time = Column(DateTime, default=datetime.now)

    total_seats = Column(Integer)

    airline = relationship("Airline", back_populates="flights")

    departure_airport = relationship(
        "Airport",
        foreign_keys=[dep_air_id],
        back_populates="departures"
    )

    arrival_airport = relationship(
        "Airport",
        foreign_keys=[arr_air_id],
        back_populates="arrivals"
    )

    seats = relationship("Seats", back_populates="flight")