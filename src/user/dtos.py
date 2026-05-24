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
    
