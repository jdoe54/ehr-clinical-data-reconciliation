from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.medication import Medication
from backend.models.patient import Patient
from backend.schema import MedicationCreate, MedicationRead

router = APIRouter(prefix="/api/medications", tags=["medications"])

@router.get("/", response_model=list[MedicationRead])
def get_medications(db: Session = Depends(get_db)):
    return db.query(Medication).all()


@router.get("/patient/{patient_id}", response_model=list[MedicationRead])
def get_medications_by_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return db.query("Medication").filter(Medication.patient_id == patient_id).all()


@router.post("/", response_model=MedicationRead)
def create_medication(
    medication_data: MedicationCreate,
    db: Session = Depends(get_db)

):
    patient = db.query(Patient).filter(Patient.id == medication_data.patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    medication = Medication(**medication_data.model_dump())

    db.add(medication)
    db.commit()
    db.refresh(medication)

    return medication