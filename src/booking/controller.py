from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.booking.dtos import (
    BookingCreateSchema,
    BookingUpdateSchema
)
from src.user.model import User
from src.booking.model import Bookings
from src.seats.model import Seats

def create_booking(body: BookingCreateSchema, db: Session, current_user: User):

    # ── Resolve seat_id from seat_no + flight_id if not provided directly ──
    seat_id = body.seat_id

    if seat_id is None:
        seat = db.query(Seats).filter(
            Seats.seat_no == body.seat_no,
            Seats.flight_no == body.flight_id
        ).first()

        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seat {body.seat_no} not found for flight {body.flight_id}"
            )

        if seat.is_book:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seat {body.seat_no} is already booked"
            )

        seat_id = seat.seat_id

    # ── Check if seat is already booked ──
    is_exist = db.query(Bookings).filter(
        Bookings.seat_id == seat_id,
        Bookings.status != "cancelled"
    ).first()

    if is_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat already booked"
        )

    new_booking = Bookings(
        seat_id=seat_id,
        user_id=current_user.user_id
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # ── Mark seat as booked ──
    seat_record = db.query(Seats).filter(Seats.seat_id == seat_id).first()
    if seat_record:
        seat_record.is_book = True
        db.commit()

    return new_booking

def get_all_bookings(db: Session,current_user:User):

    bookings = db.query(Bookings).filter(Bookings.user_id==current_user.user_id).all()
    
    if not bookings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No Available Bookings'
        )

    return bookings

def get_booking_by_id(id: int, db: Session,current_user:User):

    booking = db.query(Bookings).filter(
        Bookings.b_id == id,Bookings.user_id==current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    return booking



def update_booking(
    id: int,
    body: BookingUpdateSchema,
    db: Session,
    current_user:User
):

    booking = db.query(Bookings).filter(
        Bookings.b_id == id,Bookings.user_id==current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)

    return booking
def delete_booking(id: int, db: Session,current_user:User):

    booking = db.query(Bookings).filter(
        Bookings.b_id == id,Bookings.user_id==current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    db.delete(booking)

    db.commit()

    return None