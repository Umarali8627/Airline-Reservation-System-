from fastapi import HTTPException, Depends, APIRouter, status,Request
from sqlalchemy.orm import Session
from src.user .model import User
from src.utils.db import get_db
from src.user.controller import is_authenticated

from src.booking.controller import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking
    )

from src.booking.dtos import (
    BookingCreateSchema,
    BookingResponseSchema,
    BookingUpdateSchema
)

booking_router = APIRouter(
    prefix='/bookings'
)
# get the current user 
def get_current_user(request:Request,db:Session=Depends(get_db)):
    return is_authenticated(request,db)


@booking_router.post(
    '/create',
    response_model=BookingResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create(
    body: BookingCreateSchema,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return create_booking(body, db,current_user)
@booking_router.get(
    '/',
    response_model=list[BookingResponseSchema],
    status_code=status.HTTP_200_OK
)
def get_all(db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_all_bookings(db,current_user)
@booking_router.get('/{id}',
    response_model=BookingResponseSchema,
    status_code=status.HTTP_200_OK
)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return get_booking_by_id(id, db,current_user)

@booking_router.put(
    '/{id}',
    response_model=BookingResponseSchema,
    status_code=status.HTTP_200_OK
)
def update(
    id: int,
    body: BookingUpdateSchema,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return update_booking(id, body, db,current_user)

@booking_router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return delete_booking(id, db,current_user)