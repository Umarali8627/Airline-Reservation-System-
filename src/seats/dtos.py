from pydantic import BaseModel
from typing import Optional


# =========================================
# BASE SCHEMA
# =========================================
class SeatBaseSchema(BaseModel):
    flight_no: int
    seat_no: int
    seat_class: str = "Economy"


# =========================================
# CREATE SCHEMA
# =========================================
class SeatCreateSchema(SeatBaseSchema):
    pass


# =========================================
# UPDATE SCHEMA
# =========================================
class SeatUpdateSchema(BaseModel):
    seat_no: Optional[int] = None
    seat_class: Optional[str] = None
    is_book: Optional[bool] = None


# =========================================
# RESPONSE SCHEMA
# =========================================
class SeatResponseSchema(SeatBaseSchema):
    seat_id: int
    is_book: bool

   