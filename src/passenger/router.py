from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.utils.db import get_db

from src.passenger.controller import (
    create_passanger,
    get_all_passangers,
    get_passanger_by_id,
    update_passanger,
    delete_passanger
)

from src.passenger.dtos import (
    PassangerCreateSchema,
    PassangerUpdateSchema,
    PassangerResponseSchema
)

passanger_router = APIRouter(
    prefix="/passangers"
)


# =========================================
# CREATE PASSANGER
# =========================================
@passanger_router.post(
    "/create",
    response_model=PassangerResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create(
    body: PassangerCreateSchema,
    db: Session = Depends(get_db)
):
    return create_passanger(body, db)


# =========================================
# GET ALL PASSANGERS
# =========================================
@passanger_router.get(
    "/all",
    response_model=list[PassangerResponseSchema]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_passangers(db)


# =========================================
# GET PASSANGER BY ID
# =========================================
@passanger_router.get(
    "od/{id}",
    response_model=PassangerResponseSchema
)
def get_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return get_passanger_by_id(id, db)


# =========================================
# UPDATE PASSANGER
# =========================================
@passanger_router.put(
    "update/{id}",
    response_model=PassangerResponseSchema
)
def update(
    id: int,
    body: PassangerUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_passanger(id, body, db)


# =========================================
# DELETE PASSANGER
# =========================================
@passanger_router.delete(
    "delete/{id}",
    status_code=status.HTTP_200_OK
)
def delete(
    id: int,
    db: Session = Depends(get_db)
):
    return delete_passanger(id, db)