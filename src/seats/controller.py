from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.seats.model import Seats
from src.flights.model import Flights

from src.seats.dtos import (
    SeatCreateSchema,
    SeatUpdateSchema
)


# =========================================
# CREATE SEAT
# =========================================
def create_seat(body: SeatCreateSchema, db: Session):

    # ==========================
    # CHECK FLIGHT EXIST
    # ==========================
    flight = db.query(Flights).filter(
        Flights.f_id == body.flight_no
    ).first()

    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )

    # ==========================
    # CHECK DUPLICATE SEAT
    # ==========================
    is_exist = db.query(Seats).filter(
        Seats.flight_no == body.flight_no,
        Seats.seat_no == body.seat_no
    ).first()

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat already exists for this flight"
        )

    new_seat = Seats(
        flight_no=body.flight_no,
        seat_no=body.seat_no,
        seat_class=body.seat_class
    )

    db.add(new_seat)

    db.commit()

    db.refresh(new_seat)

    return new_seat


# =========================================
# GET ALL SEATS
# =========================================
def get_all_seats(db: Session):

    seats = db.query(Seats).all()

    return seats


# =========================================
# GET SEAT BY ID
# =========================================
def get_seat_by_id(id: int, db: Session):

    seat = db.query(Seats).filter(
        Seats.seat_id == id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )

    return seat


# =========================================
# UPDATE SEAT
# =========================================
def update_seat(
    id: int,
    body: SeatUpdateSchema,
    db: Session
):

    seat = db.query(Seats).filter(
        Seats.seat_id == id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(seat, key, value)

    db.commit()

    db.refresh(seat)

    return seat


# =========================================
# DELETE SEAT
# =========================================
def delete_seat(id: int, db: Session):

    seat = db.query(Seats).filter(
        Seats.seat_id == id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )

    db.delete(seat)

    db.commit()

    return None