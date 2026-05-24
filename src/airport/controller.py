from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from src.airport.dtos import CreateSchema
from src.airport.model import Airport


def create_airport(body:CreateSchema,db:Session):
    is_exist = db.query(Airport).filter(Airport.airport_name==body.airport_name).first()
    if is_exist:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = 'Aiport Already Exist'
        )
    new_airport= Airport(
        airport_name= body.airport_name,
        country = body.country,
        city = body.city
    )
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)

    return new_airport 
def getbyname(name : str,db:Session):
    is_exist = db.query(Airport).filter(Airport.airport_name==name).all()
    if not is_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Airport not found'
        )
    return is_exist
def get_all_airport(db:Session):
    airports = db.query(Airport).all()
    print(airports)
    if not airports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return airports
def get_airportbyId(id:int,db:Session):
    is_airport = db.query(Airport).filter(Airport.airp_id==id).first()
    if not is_airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return is_airport
def updateAirport(id:int,body:CreateSchema,db:Session):
    is_air= get_airportbyId(id,db)
    if not is_air :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    data = body.model_dump(exclude_unset=True)
    for key,value in data.items():
        if value is not None:
           setattr(is_air,key,value)
    
    db.commit()
    db.refresh(is_air)
    return is_air
def delete_airportbyid(id:int , db:Session):
    is_air= get_airportbyId(id,db)
    if not is_air :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    db.delete(is_air)
    db.commit()
    return None