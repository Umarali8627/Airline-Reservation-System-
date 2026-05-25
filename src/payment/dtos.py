from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentCreateSchema(BaseModel):
    booking_id: int
    amount: int


class PaymentUpdateSchema(BaseModel):
    payment_status: Optional[str] = None
    amount: Optional[int] = None


class PaymentResponseSchema(BaseModel):
    pay_id: int
    payment_status: str
    amount: int
    booking_id: int
    pay_time: datetime

    class Config:
        from_attributes = True
