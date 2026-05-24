from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.passenger.model import Passanger
from src.booking.model import Bookings

from src.passenger.dtos import (
    PassangerCreateSchema,
    PassangerUpdateSchema
)


# =========================================
# CREATE PASSANGER
# =========================================
def create_passanger(
    body: PassangerCreateSchema,
    db: Session
):

    # ==========================
    # CHECK BOOKING EXIST
    # ==========================
    booking = db.query(Bookings).filter(
        Bookings.b_id == body.booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # ==========================
    # CHECK EMAIL EXIST
    # ==========================
    is_email = db.query(Passanger).filter(
        Passanger.email == body.email
    ).first()

    if is_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # ==========================
    # CHECK PASSPORT EXIST
    # ==========================
    is_passport = db.query(Passanger).filter(
        Passanger.passport_num == body.passport_num
    ).first()

    if is_passport:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Passport already exists"
        )

    # ==========================
    # CREATE PASSANGER
    # ==========================
    new_passanger = Passanger(
        p_name=body.p_name,
        email=body.email,
        contact=body.contact,
        passport_num=body.passport_num,
        nationality=body.nationality,
        DOB=body.DOB,
        booking_id=body.booking_id
    )

    db.add(new_passanger)

    db.commit()

    db.refresh(new_passanger)

    return new_passanger


# =========================================
# GET ALL PASSANGERS
# =========================================
def get_all_passangers(db: Session):

    passangers = db.query(Passanger).all()

    return passangers


# =========================================
# GET PASSANGER BY ID
# =========================================
def get_passanger_by_id(id: int, db: Session):

    passanger = db.query(Passanger).filter(
        Passanger.p_id == id
    ).first()

    if not passanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passanger not found"
        )

    return passanger


# =========================================
# UPDATE PASSANGER
# =========================================
def update_passanger(
    id: int,
    body: PassangerUpdateSchema,
    db: Session
):

    passanger = db.query(Passanger).filter(
        Passanger.p_id == id
    ).first()

    if not passanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passanger not found"
        )

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(passanger, key, value)

    db.commit()

    db.refresh(passanger)

    return passanger


# =========================================
# DELETE PASSANGER
# =========================================
def delete_passanger(id: int, db: Session):

    passanger = db.query(Passanger).filter(
        Passanger.p_id == id
    ).first()

    if not passanger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passanger not found"
        )

    db.delete(passanger)

    db.commit()

    return {
        "message": "Passanger deleted successfully"
    }