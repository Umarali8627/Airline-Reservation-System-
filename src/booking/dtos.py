from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional


class BookingCreateSchema(BaseModel):
    seat_id: Optional[int] = None      # can pass directly if known
    seat_no: Optional[str] = None      # e.g. "7D"
    flight_id: Optional[int] = None    # required when using seat_no

    @model_validator(mode="after")
    def check_seat_input(self):
        if self.seat_id is None and (self.seat_no is None or self.flight_id is None):
            raise ValueError(
                "Provide either seat_id, or both seat_no and flight_id"
            )
        return self


class BookingUpdateSchema(BaseModel):
    status: Optional[str] = None
    seat_id: Optional[int] = None


class BookingResponseSchema(BaseModel):
    b_id: int
    
    b_date: datetime
    status: str
    seat_id: int
    user_id: int