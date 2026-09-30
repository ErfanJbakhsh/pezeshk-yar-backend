from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Appointment

router = APIRouter(
    tags=["Appointments"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/Appointments/me", status_code=status.HTTP_200_OK)
def get_doctors(db: db_dependency):
    result = db.query(Appointment).all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No appointments found",
        )
    return result
