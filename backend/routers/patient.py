from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.patient import Patient
from backend.models.lab_results import Labs
from backend.models.conditions import Conditions
from backend.models.allergies import Allergies


router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return [
         {
            "id": patient.id,
            "mrn": patient.mrn,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth.isoformat()
            if patient.date_of_birth
            else None,
            "age_years": patient.age_years,
            "gender": patient.gender,
            "last_updated": patient.last_updated.isoformat()
            if patient.last_updated
            else None,

            "can_reconcile": patient.mrn.startswith("RECON-")
            if patient.mrn
            else False,

            "can_validate": patient.mrn.startswith("VALIDATE-")
            if patient.mrn
            else False,
        }
        for patient in patients
    ]

@router.get("/{patient_id}")
def get_patients(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "id": patient.id,
        "mrn": patient.mrn,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth.isoformat()
        if patient.date_of_birth
        else None,
        "age_years": patient.age_years,
        "gender": patient.gender,
        "last_updated": patient.last_updated.isoformat()
        if patient.last_updated
        else None,

        "can_reconcile": patient.mrn.startswith("RECON-")
        if patient.mrn
        else False,

        "can_validate": patient.mrn.startswith("VALIDATE-")
        if patient.mrn
        else False,
    }
     

@router.get("/{patient_id}/labs")
def get_patient_lab(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Labs).filter(Labs.patient_id == patient_id).all()

@router.get("/{patient_id}/conditions")
def get_patient_conditions(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Conditions).filter(Labs.patient_id == patient_id).all()

@router.get("/{patient_id}/allergies")
def get_patient_allergies(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Allergies).filter(Labs.patient_id == patient_id).all()

