from datetime import date
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    systolic_bp: Mapped[str | None] = mapped_column(String(100), nullable=True)
    diastolic_bp: Mapped[str | None] = mapped_column(String(100), nullable=True)
    heart_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_updated: Mapped[date] = mapped_column(Date, nullable=False)