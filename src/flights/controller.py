from fastapi import HTTPException, status
from sqlalchemy.orm import Session,aliased

from src.flights.model import Flights
from src.airline.model import Airline
from src.airport.model import Airport
from src.seats.model import Seats
from src.flights.dtos import (
    FlightCreateSchema,
    FlightUpdateSchema
)
from datetime import datetime, timedelta


# =========================================
# CREATE FLIGHT
# =========================================
def create_flight(body: FlightCreateSchema, db: Session):

    
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
    count_seats = (body.economy_seats+body.premium_seats+body.business_seats)
    if count_seats>body.total_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Economy + Premium + Business seats cannot exceed total seats'
        )
    if count_seats != body.total_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat class counts must equal total seats"
        )
    new_flight = Flights(
        airline_id=body.airline_id,
        dep_air_id=body.dep_air_id,
        arr_air_id=body.arr_air_id,
        arrival_time=body.arrival_time,
        departure_time=body.departure_time,
        total_seats=body.total_seats,
        economy_seats= body.economy_seats,
        premium_seats= body.premium_seats,
        business_seats = body.business_seats,
        economy_price= body.economy_price,
        premium_price= body.premium_price,
        business_price = body.business_price,
    )

    db.add(new_flight)

    db.commit()

    db.refresh(new_flight)
#   now creating the seats for the current flight 


    seats = []

    letters = ["A", "B", "C", "D", "E", "F"]

# Business (Row 1–?)
    row = 1
    for i in range(body.business_seats):
        seats.append(
            Seats(
                flight_no=new_flight.f_id,
                seat_no=f"{row}{letters[i % len(letters)]}",
                seat_class="Business"
            )
        )
        if (i + 1) % 6 == 0:
            row += 1

    # Premium (Row starts after Business)
    row = 5
    for i in range(body.premium_seats):
        seats.append(
            Seats(
                flight_no=new_flight.f_id,
                seat_no=f"{row}{letters[i % len(letters)]}",
                seat_class="Premium"
            )
        )
        if (i + 1) % 6 == 0:
            row += 1

    # Economy (Row starts after Premium)
    row = 11
    for i in range(body.economy_seats):
        seats.append(
            Seats(
                flight_no=new_flight.f_id,
                seat_no=f"{row}{letters[i % len(letters)]}",
                seat_class="Economy"
            )
        )
        if (i + 1) % 6 == 0:
            row += 1

    db.add_all(seats)
    db.commit()
    return new_flight


# =========================================
# GET ALL FLIGHTS
# =========================================
# def get_all_flights(db: Session):
#     depAirport = aliased(Airport)
#     arrAirport = aliased(Airport)
#     flights = (db.query(Flights).all())
        
    
    
#     return flights
def get_all_flights(db: Session):
    flights = db.query(Flights).all()
    
    result = []
     
    for flight in flights:
        airline = db.query(Airline).filter(Airline.air_id==flight.airline_id).first()
        flight_seats = db.query(Seats).filter(Seats.flight_no==flight.f_id).all()
        
        available_seats = sum(
            1 for seat in flight_seats
            if not seat.is_book
        )
        # print(available_seats)
        result.append({
            "f_id": flight.f_id,
            "economy_price": flight.economy_price,
            "premium_price":flight.premium_price,
            "business_price":flight.business_price,
            "dep_city":flight.departure_airport.city,
            "arr_city":flight.arrival_airport.city,
            "airline_id": flight.airline_id,
            "airline_name":airline.air_name,
            "dep_airport": flight.departure_airport.airport_name,
            "arr_airport": flight.arrival_airport.airport_name,
            "status": flight.status,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "total_seats": flight.total_seats,
            "economy_seats":flight.economy_seats,
            "premium_seats":flight.premium_seats,
            'business_seats':flight.business_seats,
            "available_seats": available_seats,
        })

    return result

# =========================================
# GET FLIGHT BY ID
# =========================================
def get_flight_by_id(id: int, db: Session):

    flight = db.query(Flights).filter(
        Flights.f_id == id
    ).first()
    # print(flight)
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    result = []
   
    airline = db.query(Airline).filter(Airline.air_id==flight.airline_id).first()
    flight_seats = db.query(Seats).filter(Seats.flight_no==flight.f_id).all()
        
    available_seats = sum(
            1 for seat in flight_seats
            if not seat.is_book
        )
        # print(available_seats)
    return {
            "f_id": flight.f_id,
            "economy_price": flight.economy_price,
            "premium_price":flight.premium_price,
            "business_price":flight.business_price,
            "dep_city":flight.departure_airport.city,
            "arr_city":flight.arrival_airport.city,
            "airline_id": flight.airline_id,
            "airline_name":airline.air_name,
            "dep_airport": flight.departure_airport.airport_name,
            "arr_airport": flight.arrival_airport.airport_name,
            "status": flight.status,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "total_seats": flight.total_seats,
            "economy_seats":flight.economy_seats,
            "premium_seats":flight.premium_seats,
            'business_seats':flight.business_seats,
            "available_seats": available_seats,
        }

    # return result

   


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

# create a route for search the flights from destionation to source 
def search_flights(
    from_airp: str,
    to_airp: str,
    departure_time: datetime,
    db: Session
):
    DepAirport = aliased(Airport)
    ArrAirport = aliased(Airport)

    departure_start = departure_time.replace(hour=0, minute=0, second=0, microsecond=0)
    departure_end = departure_start + timedelta(days=1)

    flights = (
        db.query(Flights)
        .join(DepAirport, Flights.dep_air_id == DepAirport.airp_id)
        .join(ArrAirport, Flights.arr_air_id == ArrAirport.airp_id)
        .filter(
            DepAirport.airport_name == from_airp,
            ArrAirport.airport_name == to_airp,
            Flights.departure_time >= departure_start,
            Flights.departure_time < departure_end
        )
        .all()
    )

    if not flights:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not available"
        )

    result = []

    for flight in flights:
        airline = db.query(Airline).filter(
            Airline.air_id == flight.airline_id
        ).first()

        flight_seats = db.query(Seats).filter(
            Seats.flight_no == flight.f_id
        ).all()

        available_seats = sum(1 for seat in flight_seats if not seat.is_book)

        result.append({
            "f_id": flight.f_id,
            "economy_price": flight.economy_price,
            "premium_price": flight.premium_price,
            "business_price": flight.business_price,

           
            "dep_city": flight.departure_airport.city,
            "arr_city": flight.arrival_airport.city,

            "airline_id": flight.airline_id,
            "airline_name": airline.air_name,

            "dep_airport": flight.departure_airport.airport_name,
            "arr_airport": flight.arrival_airport.airport_name,

            "status": flight.status,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,

            "total_seats": flight.total_seats,
            "economy_seats": flight.economy_seats,
            "premium_seats": flight.premium_seats,
            "business_seats": flight.business_seats,

            "available_seats": available_seats,
        })

    return result