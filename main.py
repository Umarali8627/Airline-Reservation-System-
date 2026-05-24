from fastapi import FastAPI
from src.utils.db import Base,engine
from src.airline.model import Airline
from src.airport.model import Airport
from src.booking.model import Bookings
from src.flights.model import Flights
from src.passenger.model import Passanger
from src.payment.model import Payment
from src.seats.model import Seats
from src.user.model import User
from src.airline.router import airline_router
from src.airport .router import airport_router
from src.booking.router import booking_router
from src.seats.router import seat_router
from src.user.router import user_router
from src.flights.router import flight_router

Base.metadata.create_all(engine)

app = FastAPI(
    title = 'Airline Reservation System',
    description='adbms project',
    version='1.0'
)


@app.get('/')
def home(): 
    return {'message': "welcome to airline Reservation"}

app.include_router(airline_router)
app.include_router(airport_router)
app.include_router(booking_router)
app.include_router(seat_router)
app.include_router(user_router)
app.include_router(flight_router)
