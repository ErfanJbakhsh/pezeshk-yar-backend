from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Appointment, DoctorSlot
from .auth import get_current_user

router = APIRouter(
    tags=["Appointments"],
    prefix="/appointments"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_appointments(db: db_dependency, user: user_dependency):
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication failed')
    result = db.query(Appointment).filter(Appointment.user_id == user.get("id")).all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No appointments found",
        )

    return result

@router.post("", status_code=status.HTTP_201_CREATED)
async def set_appointment(db: db_dependency, user: user_dependency, slot_id: int):
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication failed')
    slot = db.query(DoctorSlot).filter(DoctorSlot.id == slot_id, DoctorSlot.is_active == True).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    booked = db.query(Appointment).filter(Appointment.slot_id == slot_id, Appointment.status != "cancelled").first()
    if booked:
        raise HTTPException(status_code=409, detail="Slot is already booked")
    
    appointment = Appointment(user_id=user["id"], slot_id=slot_id)
    slot.is_active = False

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
