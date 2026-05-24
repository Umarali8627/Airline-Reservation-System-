from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.db import Base

class Payment(Base):
    __tablename__ = 'Payment'

    pay_id = Column(Integer, primary_key=True)

    payment_status = Column(String, default='pending')

    amount = Column(Integer)

    booking_id = Column(Integer, ForeignKey('Booking.b_id'))

    pay_time = Column(DateTime, default=datetime.now)

    booking = relationship("Bookings", back_populates="payments")