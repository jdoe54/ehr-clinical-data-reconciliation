from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.vital_signs import VitalSigns

router = APIRouter(prefix="/api/vital-signs", tags=["vital-signs"])

@router.get("/")
def get_vitals(db: Session = Depends(get_db)):
    return db.query(VitalSigns).all()
