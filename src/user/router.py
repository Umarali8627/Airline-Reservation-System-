from fastapi import APIRouter,Depends,HTTPException,status,Request
from src.utils.db import get_db
from src.user.controller import register,login,is_authenticated
from src.user.dtos import UserRegisterSchema,LoginSchema,UserResponseSchema
from sqlalchemy.orm import Session

user_router= APIRouter(prefix='/Users',tags=['Users'])

@user_router.post('/register',response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register_user(body:UserRegisterSchema,db:Session=Depends(get_db)):
    return register(body,db)
@user_router.post('/login',status_code=status.HTTP_200_OK)
def login_user(body:LoginSchema,db:Session=Depends(get_db)):
    return login(body,db)
@user_router.get('/is_auth',status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return is_authenticated(request,db)