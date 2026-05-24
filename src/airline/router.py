from fastapi import APIRouter,Depends,status,Request
from sqlalchemy.orm import Session
from src.airline.dtos import AirlineSchema,ResponseSchema
from src.airline.controller import add_airline,getbyId,getbyname,updateairline,deleteAirlinebyId,get_all_airline
from src.utils.db import get_db
from src.user import controller
from src.user.model import User


airline_router = APIRouter(prefix='/airline')

def get_current_admin(request:Request,db:Session=Depends(get_db)):
    return controller.is_admin(request,db)

@airline_router.post('/create',response_model=ResponseSchema,status_code=status.HTTP_201_CREATED)
def create_airline(body:AirlineSchema,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return add_airline(body,db)
@airline_router.get('/all',response_model=ResponseSchema,status_code=status.HTTP_200_OK)
def get_all(db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return get_all_airline(db)
@airline_router.get('/{id}',response_model=ResponseSchema,status_code=status.HTTP_200_OK)
def getairbyId(id:int,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return getbyId(id,db)
@airline_router.get('/search/{name}',status_code=status.HTTP_200_OK,response_model=ResponseSchema)
def getairbyname(name:str,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return getbyname(name,db)


@airline_router.put('/update/{id}',response_model=ResponseSchema,status_code=status.HTTP_200_OK)
def updatebyId(id:int,body:AirlineSchema,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return updateairline(id,body,db)
@airline_router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delateairline(id:int,db:Session=Depends(get_db),current_admin:User=Depends(get_current_admin)):
    return deleteAirlinebyId(id,db)
