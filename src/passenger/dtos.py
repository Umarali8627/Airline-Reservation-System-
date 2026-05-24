from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# =========================================
# BASE SCHEMA
# =========================================
class PassangerBaseSchema(BaseModel):

    p_name: str
    email: EmailStr
    contact: str
    passport_num: str
    nationality: str
    DOB: date
    booking_id: int


# =========================================
# CREATE SCHEMA
# =========================================
class PassangerCreateSchema(PassangerBaseSchema):
    pass


# =========================================
# UPDATE SCHEMA
# =========================================
class PassangerUpdateSchema(BaseModel):

    p_name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact: Optional[str] = None
    passport_num: Optional[str] = None
    nationality: Optional[str] = None
    DOB: Optional[date] = None


# =========================================
# RESPONSE SCHEMA
# =========================================
class PassangerResponseSchema(PassangerBaseSchema):

    p_id: int

   