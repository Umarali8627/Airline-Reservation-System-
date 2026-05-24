from pydantic import BaseModel

class AirlineSchema(BaseModel):
    air_name : str
    model_name: str
    country:str
class ResponseSchema(BaseModel):
    air_id:int
    air_name:str
    model_name:str
    country:str
    
