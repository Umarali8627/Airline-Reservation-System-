from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.db import Base

class Bookings(Base):
    __tablename__ = 'Booking'

    b_id = Column(Integer, primary_key=True)

    b_date = Column(DateTime, default=datetime.now)

    status = Column(String, default='pending')

    seat_id = Column(Integer, ForeignKey('Seats.seat_id'))

    seat = relationship("Seats", back_populates="bookings")

    payments = relationship("Payment", back_populates="booking")

    user_id = Column(Integer, ForeignKey("Users.user_id"))

    user = relationship("User", back_populates="bookings")

    passangers = relationship(
    "Passanger",
    back_populates="booking"
)