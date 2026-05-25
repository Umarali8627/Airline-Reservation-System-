from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.model import User
from src.payment.controller import (
    create_payment,
    get_all_payments,
    get_payment_by_id,
    update_payment,
    process_payment,
    cancel_payment,
    get_payment_by_booking
)
from src.payment.dtos import PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema

payment_router = APIRouter(prefix="/payments", tags=["Payments"])


@payment_router.post(
    "/",
    response_model=PaymentResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create_payment_endpoint(
    body: PaymentCreateSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return create_payment(body, db, current_user)


@payment_router.get("/", response_model=list[PaymentResponseSchema])
def get_payments(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return get_all_payments(db, current_user)


@payment_router.get("/{payment_id}", response_model=PaymentResponseSchema)
def get_payment(
    payment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return get_payment_by_id(payment_id, db, current_user)


@payment_router.put("/{payment_id}", response_model=PaymentResponseSchema)
def update_payment_endpoint(
    payment_id: int,
    body: PaymentUpdateSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return update_payment(payment_id, body, db, current_user)


@payment_router.post("/{payment_id}/process", response_model=PaymentResponseSchema)
def process_payment_endpoint(
    payment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return process_payment(payment_id, db, current_user)


@payment_router.post("/{payment_id}/cancel", response_model=PaymentResponseSchema)
def cancel_payment_endpoint(
    payment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return cancel_payment(payment_id, db, current_user)


@payment_router.get("/booking/{booking_id}", response_model=PaymentResponseSchema)
def get_payment_for_booking(
    booking_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = is_authenticated(request, db)
    return get_payment_by_booking(booking_id, db, current_user)
