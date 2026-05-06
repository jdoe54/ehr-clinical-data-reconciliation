from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.patient import Patient
from backend.models.lab_results import Labs
from backend.models.conditions import Conditions
from backend.models.allergies import Allergies


router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.get("/{patient_id}")
def get_patients(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Patient).filter(Patient.id == patient_id).all()

@router.get("/{patient_id}/labs")
def get_patient_lab(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Labs).filter(Labs.patient_id == patient_id).all()

@router.get("/{patient_id}/conditions")
def get_patient_conditions(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Conditions).filter(Labs.patient_id == patient_id).all()

@router.get("/{patient_id}/allergies")
def get_patient_allergies(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Allergies).filter(Labs.patient_id == patient_id).all()

