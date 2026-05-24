from src.utils.db import Base
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from src.airline.dtos import AirlineSchema
from src.airline.model import Airline


def add_airline(body:AirlineSchema,db:Session):
    is_exist = db.query(Airline).filter(Airline.model_name==body.model_name).first()
    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail = "Airline Already exist")
    new_airline= Airline(
        air_name= body.air_name,
        model_name = body.model_name,
        country= body.country
    )
    db.add(new_airline)
    db.commit()
    db.refresh(new_airline)
    return new_airline

def getbyId(id:int ,db :Session):
    is_airline= db.query(Airline).filter(Airline.air_id==id).first()
    if not is_airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not found"
        )
    return is_airline
def getbyname(name: str ,db:Session):
    is_airline = db.query(Airline).filter(Airline.air_name==name).all()
    if not is_airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not found"
        )
    return is_airline
def get_all_airline(db:Session):
    airlines = db.query(Airline).all()
    return airlines
def updateairline(id:int,body:AirlineSchema,db:Session):
    is_airline = getbyId(id,db)
    if not is_airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not found"
        )
    data= body.model_dump()
    for key,value in data.items():
        if value is not None:
            setattr(is_airline,key,value)
    db.commit()
    db.refresh(is_airline)
    return is_airline
def deleteAirlinebyId(id:int,db:Session):
    is_airline = db.query(Airline).filter(Airline.air_id==id).first()
    if not is_airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not Found"
        )
    db.delete(is_airline)
    db.commit()
    return None

