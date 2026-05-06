from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.conditions import Conditions


router = APIRouter(prefix="/api/conditions", tags=["conditions"])

@router.get("/")
def get_conditions(db: Session = Depends(get_db)):
    return db.query(Conditions).all()
