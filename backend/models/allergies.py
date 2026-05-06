from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Allergies(Base):
    __tablename__ = "allergies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    allergen: Mapped[str | None] = mapped_column(String(100), nullable=True)
    reaction: Mapped[str | None] = mapped_column(String(100), nullable=True)
   
