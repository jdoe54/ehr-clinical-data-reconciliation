from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.conditions import Conditions
from backend.models.patient import Patient


router = APIRouter(prefix="/api/conditions", tags=["conditions"])

@router.get("/")
def get_conditions(db: Session = Depends(get_db)):
    return db.query(Conditions).all()

@router.get("/patient/{patient_id}")
def get_conditions_by_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    conditions = (
        db.query(Conditions)
        .filter(Conditions.patient_id == patient_id)
        .all()
    )

    return [
        {
            "id": condition.id,
            "patient_id": condition.patient_id,
            "condition_name": condition.condition_name,
        }
        for condition in conditions
    ]