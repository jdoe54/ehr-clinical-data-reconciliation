from datetime import date
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Labs(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lab_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_updated: Mapped[date] = mapped_column(Date, nullable=False)