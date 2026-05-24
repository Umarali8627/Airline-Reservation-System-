from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# =========================================
# BASE SCHEMA
# =========================================
class FlightBaseSchema(BaseModel):
    airline_id: int
    dep_air_id: int
    arr_air_id: int
    arrival_time: datetime
    departure_time: datetime
    total_seats: int


# =========================================
# CREATE SCHEMA
# =========================================
class FlightCreateSchema(FlightBaseSchema):
    pass


# =========================================
# UPDATE SCHEMA
# =========================================
class FlightUpdateSchema(BaseModel):
    airline_id: Optional[int] = None
    dep_air_id: Optional[int] = None
    arr_air_id: Optional[int] = None
    arrival_time: Optional[datetime] = None
    departure_time: Optional[datetime] = None
    total_seats: Optional[int] = None
    status: Optional[str] = None


# =========================================
# RESPONSE SCHEMA
# =========================================
class FlightResponseSchema(FlightBaseSchema):
    f_id: int
    status: str

