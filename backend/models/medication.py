from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    system: Mapped[str] = mapped_column(String(100), nullable=False)
    medication: Mapped[str] = mapped_column(String(100), nullable=False)
    last_updated: Mapped[date] = mapped_column(Date, nullable=False)
    source_reliability: Mapped[str] = mapped_column(String(50), nullable=False)

    patient = relationship("Patient", back_populates="medications")