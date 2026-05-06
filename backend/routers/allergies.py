from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.allergies import Allergies

router = APIRouter(prefix="/api/allergies", tags=["allergies"])

@router.get("/")
def get_allergies(db: Session = Depends(get_db)):
    return db.query(Allergies).all()
