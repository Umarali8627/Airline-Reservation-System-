from pydantic import BaseModel

class UserRegisterSchema(BaseModel):
    user_name:str
    email:str
    password:str

class LoginSchema(BaseModel):
    email:str 
    password:str
class UserResponseSchema(BaseModel):
    user_name :str
    email:str
    
class UserData(BaseModel):
    user_id:int
    user_name:str
    email: str
    role:str
    Bookings:int 