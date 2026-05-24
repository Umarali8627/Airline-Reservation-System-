from pydantic import BaseModel


class CreateSchema(BaseModel):
    airport_name: str
    country:str
    city:str

class UpdateAirportSchema(BaseModel):
    airport_name: str | None = None
    country: str | None = None
    city: str | None = None