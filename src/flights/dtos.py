from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# =========================================
# BASE SCHEMA
# =========================================
class FlightBaseSchema(BaseModel):
    airline_id: int
    dep_city :str
    arr_city:str
    dep_airport: str
    airline_name : str
    dep_airport : str
    arr_airport : str
    arr_airport: str
    arrival_time: datetime
    departure_time: datetime
    total_seats: int
    available_seats:int 
    economy_seats:int 
    premium_seats:int 
    business_seats :int
    economy_price:int
    premium_price:int
    business_price:int
    

# =========================================
# CREATE SCHEMA
# =========================================
class FlightCreateSchema(BaseModel):
        airline_id:int
        dep_air_id:int 
        arr_air_id:int
        arrival_time:datetime
        departure_time:datetime 
        total_seats:int
        economy_seats:int 
        premium_seats:int 
        business_seats :int
        economy_price:int
        premium_price:int
        business_price:int


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

