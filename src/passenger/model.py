from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.utils.db import Base


class Passanger(Base):

    __tablename__ = 'Passanger'

    p_id = Column(Integer, primary_key=True, index=True)

    p_name = Column(String(50))

    email = Column(String, unique=True)

    contact = Column(String)

    passport_num = Column(String, unique=True)

    nationality = Column(String)

    DOB = Column(Date)

    booking_id = Column(Integer, ForeignKey('Booking.b_id'))

    booking = relationship(
        "Bookings",
        back_populates="passangers"
    )