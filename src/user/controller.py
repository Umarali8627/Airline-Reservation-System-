from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.user.dtos import LoginSchema, UserRegisterSchema
from src.user.model import User
from src.utils.db import get_db
from src.utils.helper import get_password_hash, verify_password
from src.utils.settings import settings


def register(body:UserRegisterSchema,db:Session):
    # check duplicate user 
    is_user = db.query(User).filter(User.user_name==body.user_name).first()
    if is_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= 'username already taken'
        )
    is_email = db.query(User).filter(User.email==body.email).first()
    if is_email:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= 'Email already Register'
        )
    # hash the password 
    hashed_password = get_password_hash(body.password)
    # create the new user object 
    new_user= User(
        user_name  = body.user_name,
        email= body.email,
        hash_password= hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
def login(body:LoginSchema,db:Session):
    is_user = db.query(User).filter(User.email==body.email).first()
    if not is_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= 'Email not Register'
        )
    # now verify password
    if not verify_password(body.password,is_user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = 'Wrong Password'
        )
    # now create token using algorthim and key 
     # creating expiry token
    exp_time=datetime.now()+timedelta(minutes=settings.EXP_TIME)
     
     # now creating token 
    token=jwt.encode({"_id":is_user.user_id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)
    
    return {
        "token": token,
        "user": {
            "id": is_user.user_id,
            "username": is_user.user_name,
            "email": is_user.email,
            "role": is_user.role
        }
    }

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    auth_header=request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is missing")
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = parts[1]
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id=payload.get("_id")
        user=db.query(User).filter(User.user_id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
      
    
def is_admin(request: Request, db: Session = Depends(get_db)):
    user = is_authenticated(request, db)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
