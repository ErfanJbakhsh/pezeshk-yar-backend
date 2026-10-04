from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Appointment
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

