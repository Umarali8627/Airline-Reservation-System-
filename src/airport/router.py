from fastapi import APIRouter,Depends,status,Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.airport .dtos import CreateSchema,UpdateAirportSchema
from src.airport.controller import (create_airport,getbyname,get_all_airport,
                                    get_airportbyId,updateAirport,delete_airportbyid)
from src.user import controller
from src.user.model import User

airport_router= APIRouter(prefix='/airport',tags=['airport'])

def get_current_admin(request:Request,db:Session=Depends(get_db)):
    return controller.is_admin(request,db)

@airport_router.post('/create',response_model=CreateSchema,status_code=status.HTTP_201_CREATED)
def create(body:CreateSchema,db:Session=Depends(get_db),
        # current_admin:User=Depends(get_current_admin)
        ):
    return create_airport(body,db)
@airport_router.get('/name/{name}',response_model=list[CreateSchema],status_code=status.HTTP_200_OK)
def get_by_name(name:str,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return getbyname(name,db)
@airport_router.get('/all',status_code=status.HTTP_200_OK)
def get_all(db:Session=Depends(get_db)):
    return get_all_airport(db)
@airport_router.get('/id/{id}',response_model=CreateSchema,status_code=status.HTTP_200_OK)
def getbyId(id:int,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return get_airportbyId(id,db)
@airport_router.put('/update/{id}',status_code=status.HTTP_200_OK)
def update_airport(id:int,body:UpdateAirportSchema,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return updateAirport(id,body,db)
@airport_router.delete('/delete/{id}',)
def delete_airport(id:int,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return delete_airportbyid(id,db)
