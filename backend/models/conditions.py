from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Conditions(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    condition_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=True)
   
