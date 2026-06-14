from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from src.utils.db import Base

class Seats(Base):
    __tablename__ = 'Seats'

    seat_id = Column(Integer, primary_key=True)

    flight_no = Column(Integer, ForeignKey('Flights.f_id'),index=True)

    seat_no = Column(String)

    seat_class = Column(
        Enum('Economy', 'Business', 'Premium',
              name='seat_class_enum')
    )

    is_book = Column(Boolean, default=False)

    flight = relationship("Flights", back_populates="seats")

    bookings = relationship("Bookings", back_populates="seat")