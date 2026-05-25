from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.utils.db import get_db

from src.seats.controller import (
    create_seat,
    get_all_seats,
    get_seat_by_id,
    update_seat,
    delete_seat
)

from src.seats.dtos import (
    SeatCreateSchema,
    SeatUpdateSchema,
    SeatResponseSchema
)

seat_router = APIRouter(
    prefix="/seats",
    tags=['Seats']
)


# =========================================
# CREATE SEAT
# =========================================
@seat_router.post(
    "/create",
    response_model=SeatResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create(
    body: SeatCreateSchema,
    db: Session = Depends(get_db)
):
    return create_seat(body, db)


# =========================================
# GET ALL SEATS
# =========================================
@seat_router.get(
    "/",
    response_model=list[SeatResponseSchema]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_seats(db)


# =========================================
# GET SEAT BY ID
# =========================================
@seat_router.get(
    "/{id}",
    response_model=SeatResponseSchema
)
def get_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return get_seat_by_id(id, db)


# =========================================
# UPDATE SEAT
# =========================================
@seat_router.put(
    "/{id}",
    response_model=SeatResponseSchema
)
def update(
    id: int,
    body: SeatUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_seat(id, body, db)


# =========================================
# DELETE SEAT
# =========================================
@seat_router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK
)
def delete(
    id: int,
    db: Session = Depends(get_db)
):
    return delete_seat(id, db)