from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from database import Base


appointment_status = ENUM(
    "confirmed",
    "cancelled",
    "completed",
    name="appointment_status",
    create_type=False,
)


class User(Base):
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    full_name = Column(
        String(100),
        nullable=False,
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    appointments = relationship(
        "Appointment",
        back_populates="user",
    )


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    specialty = Column(
        String(100),
        nullable=False,
    )

    medical_code = Column(
        String(30),
        unique=True,
        nullable=False,
    )

    address = Column(
        String(255),
        nullable=False,
    )

    experience_years = Column(
        Integer,
        default=0,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    slots = relationship(
        "DoctorSlot",
        back_populates="doctor",
    )


class DoctorSlot(Base):
    __tablename__ = "doctor_slots"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    doctor_id = Column(
        BigInteger,
        ForeignKey(
            "doctors.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    starts_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    doctor = relationship(
        "Doctor",
        back_populates="slots",
    )

    appointments = relationship(
        "Appointment",
        back_populates="slot",
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    slot_id = Column(
        BigInteger,
        ForeignKey(
            "doctor_slots.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    status = Column(
        appointment_status,
        default="confirmed",
        server_default="confirmed",
        nullable=False,
    )

    booked_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    cancelled_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="appointments",
    )

    slot = relationship(
        "DoctorSlot",
        back_populates="appointments",
    )
