from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.lab_results import Labs


router = APIRouter(prefix="/api/labs", tags=["labs"])

@router.get("/")
def get_labs(db: Session = Depends(get_db)):
    return db.query(Labs).all()