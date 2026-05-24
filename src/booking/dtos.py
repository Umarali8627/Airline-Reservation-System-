from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingCreateSchema(BaseModel):
    seat_id: int



class BookingUpdateSchema(BaseModel):
    status: Optional[str] = None
    seat_id: Optional[int] = None



class BookingResponseSchema(BaseModel):
    b_id: int
    b_date: datetime
    status: str
    seat_id: int
    user_id: int

