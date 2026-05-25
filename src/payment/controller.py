from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.payment.dtos import PaymentCreateSchema, PaymentUpdateSchema
from src.payment.model import Payment
from src.booking.model import Bookings
from src.user.model import User


def create_payment(body: PaymentCreateSchema, db: Session, current_user: User):
    # Check if booking exists and belongs to current user
    booking = db.query(Bookings).filter(Bookings.b_id == body.booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own bookings"
        )
    
    # Check if payment already exists for this booking
    existing_payment = db.query(Payment).filter(
        Payment.booking_id == body.booking_id,
        Payment.payment_status.in_(["completed", "processing"])
    ).first()
    
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment already processed for this booking"
        )
    
    new_payment = Payment(
        booking_id=body.booking_id,
        amount=body.amount,
        payment_status="pending"
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    return new_payment


def get_all_payments(db: Session, current_user: User):
    payments = db.query(Payment).join(Bookings).filter(
        Bookings.user_id == current_user.user_id
    ).all()
    
    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payments found"
        )
    
    return payments


def get_payment_by_id(payment_id: int, db: Session, current_user: User):
    payment = db.query(Payment).join(Bookings).filter(
        Payment.pay_id == payment_id,
        Bookings.user_id == current_user.user_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment


def update_payment(
    payment_id: int,
    body: PaymentUpdateSchema,
    db: Session,
    current_user: User
):
    payment = db.query(Payment).join(Bookings).filter(
        Payment.pay_id == payment_id,
        Bookings.user_id == current_user.user_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    data = body.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(payment, key, value)
    
    db.commit()
    db.refresh(payment)
    
    return payment


def process_payment(payment_id: int, db: Session, current_user: User):
    """Process payment and update status to completed"""
    payment = db.query(Payment).join(Bookings).filter(
        Payment.pay_id == payment_id,
        Bookings.user_id == current_user.user_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    if payment.payment_status == "completed":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment already completed"
        )
    
    payment.payment_status = "completed"
    db.commit()
    db.refresh(payment)
    
    return payment


def cancel_payment(payment_id: int, db: Session, current_user: User):
    """Cancel a pending payment"""
    payment = db.query(Payment).join(Bookings).filter(
        Payment.pay_id == payment_id,
        Bookings.user_id == current_user.user_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    if payment.payment_status in ["completed", "failed"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot cancel {payment.payment_status} payment"
        )
    
    payment.payment_status = "cancelled"
    db.commit()
    db.refresh(payment)
    
    return payment


def get_payment_by_booking(booking_id: int, db: Session, current_user: User):
    """Get payment for a specific booking"""
    payment = db.query(Payment).join(Bookings).filter(
        Payment.booking_id == booking_id,
        Bookings.user_id == current_user.user_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payment found for this booking"
        )
    
    return payment
