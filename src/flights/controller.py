from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.flights.model import Flights
from src.airline.model import Airline
from src.airport.model import Airport
from src.flights.dtos import (
    FlightCreateSchema,
    FlightUpdateSchema
)


# =========================================
# CREATE FLIGHT
# =========================================
def create_flight(body: FlightCreateSchema, db: Session):

    # ==========================
    # CHECK AIRLINE EXIST
    # ==========================
    airline = db.query(Airline).filter(
        Airline.air_id == body.airline_id
    ).first()

    if not airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airline not found"
        )

    # ==========================
    # CHECK DEPARTURE AIRPORT
    # ==========================
    dep_airport = db.query(Airport).filter(
        Airport.airp_id == body.dep_air_id
    ).first()

    if not dep_airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Departure airport not found"
        )

    # ==========================
    # CHECK ARRIVAL AIRPORT
    # ==========================
    arr_airport = db.query(Airport).filter(
        Airport.airp_id == body.arr_air_id
    ).first()

    if not arr_airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arrival airport not found"
        )

    # ==========================
    # CHECK SAME AIRPORT
    # ==========================
    if body.dep_air_id == body.arr_air_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Departure and arrival airport cannot be same"
        )

    # ==========================
    # CREATE FLIGHT
    # ==========================
    new_flight = Flights(
        airline_id=body.airline_id,
        dep_air_id=body.dep_air_id,
        arr_air_id=body.arr_air_id,
        arrival_time=body.arrival_time,
        departure_time=body.departure_time,
        total_seats=body.total_seats
    )

    db.add(new_flight)

    db.commit()

    db.refresh(new_flight)

    return new_flight


# =========================================
# GET ALL FLIGHTS
# =========================================
def get_all_flights(db: Session):

    flights = db.query(Flights).all()

    return flights


# =========================================
# GET FLIGHT BY ID
# =========================================
def get_flight_by_id(id: int, db: Session):

    flight = db.query(Flights).filter(
        Flights.f_id == id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )

    return flight


# =========================================
# UPDATE FLIGHT
# =========================================
def update_flight(
    id: int,
    body: FlightUpdateSchema,
    db: Session
):

    flight = db.query(Flights).filter(
        Flights.f_id == id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(flight, key, value)

    db.commit()

    db.refresh(flight)

    return flight


# =========================================
# DELETE FLIGHT
# =========================================
def delete_flight(id: int, db: Session):

    flight = db.query(Flights).filter(
        Flights.f_id == id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )

    db.delete(flight)

    db.commit()

    return {
        "message": "Flight deleted successfully"
    }