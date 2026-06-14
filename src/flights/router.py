from fastapi import APIRouter, Depends, status,Request
from sqlalchemy.orm import Session
from src.user import controller
from src.utils.db import get_db

from src.flights.controller import (
    create_flight,
    get_all_flights,
    get_flight_by_id,
    update_flight,
    delete_flight,
    search_flights,

)
from datetime import datetime 
from src.user.model import User
from src.flights.dtos import (
    FlightCreateSchema,
    FlightUpdateSchema,
    FlightResponseSchema
)

flight_router = APIRouter(
    prefix="/flights",
    tags=['flights']
)


def get_current_admin(request:Request,db:Session=Depends(get_db)):
    return controller.is_admin(request,db)


# =========================================
# CREATE FLIGHT
# =========================================
@flight_router.post(
    "/create",
    response_model=FlightCreateSchema,
    status_code=status.HTTP_201_CREATED
)
def create(
    body: FlightCreateSchema,
    db: Session = Depends(get_db),
    # current_admin:User=Depends(get_current_admin)
):
    return create_flight(body, db)


# =========================================
# GET ALL FLIGHTS
# =========================================
@flight_router.get(
    "/all",
    response_model=list[FlightResponseSchema]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_flights(db)


# =========================================
# GET FLIGHT BY ID
# =========================================
@flight_router.get(
    "/id/{id}",
    response_model=FlightResponseSchema
)
def get_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return get_flight_by_id(id, db)


# =========================================
# UPDATE FLIGHT
# =========================================
@flight_router.put(
    "/update/{id}",
    response_model=FlightResponseSchema
)
def update(
    id: int,
    body: FlightUpdateSchema,
    db: Session = Depends(get_db),
    current_admin:User=Depends(get_current_admin)
):
    return update_flight(id, body, db)


# =========================================
# DELETE FLIGHT
# =========================================
@flight_router.delete(
    "/dletete/{id}",
    status_code=status.HTTP_200_OK
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_admin:User=Depends(get_current_admin)
):
    return delete_flight(id, db)

@flight_router.get('/search/flights')
def search_flight(
   dep_airp:str,
   arr_airp:str,
   dept_time : datetime,
   db=Depends(get_db)
):
    return search_flights(dep_airp,arr_airp,dept_time,db)