from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Doctor, DoctorSlot

router = APIRouter(
    tags=["Doctors"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/Doctors", status_code=status.HTTP_200_OK)
def get_doctors(db: db_dependency):
    result = db.query(Doctor).all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctors not found",
        )
    return result
   
@router.get("/Doctors/{id}", status_code=status.HTTP_200_OK)
def get_doctor_by_id(db: db_dependency ,id: int):
    result = db.query(Doctor).filter(Doctor.id == id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return result

@router.get("/Doctors/{id}/slots", status_code=status.HTTP_200_OK)
def get_doctor_slots_by_id(db: db_dependency ,id: int):
    result = db.query(DoctorSlot).filter(DoctorSlot.doctor_id == id).all()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return result