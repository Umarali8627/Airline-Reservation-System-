from fastapi import APIRouter,Depends,HTTPException,status,Request
from src.utils.db import get_db
from src.user.controller import register,login,is_authenticated
from src.user.dtos import UserRegisterSchema,LoginSchema,UserResponseSchema
from sqlalchemy.orm import Session
from src.user import controller
from src.user.model import User
from src.user.dtos import UserData

user_router= APIRouter(prefix='/Users',tags=['Users'])

def get_current_admin(request:Request,db:Session=Depends(get_db)):
    return controller.is_admin(request,db)

@user_router.post('/register',response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register_user(body:UserRegisterSchema,db:Session=Depends(get_db)):
    return register(body,db)
@user_router.post('/login',status_code=status.HTTP_200_OK)
def login_user(body:LoginSchema,db:Session=Depends(get_db)):
    return login(body,db)
@user_router.get('/is_auth',status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return is_authenticated(request,db)
@user_router.get('/all',status_code=status.HTTP_200_OK,response_model=list[UserData])
def get_all_Users(db:Session=Depends(get_db),
                current_admin:User=Depends(get_current_admin)
                  ):
    return controller.get_allUser(db)