from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/doctors", status_code=status.HTTP_200_OK)
def get_doctors(db: db_dependency):
    result = db.execute(text("SELECT * FROM doctors ORDER BY id"))
    doctors = result.mappings().all()

    if not doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    return [dict(doctor) for doctor in doctors]
