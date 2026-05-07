from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.patient import Patient

from backend.services.record_service import build_patient_record

router = APIRouter(prefix="/validate-data", tags=["validate-data"])




@router.get("/patient/{patient_id}")
def get_validate_patient_data(patient_id: int, db: Session = Depends(get_db)):
    return build_patient_record(patient_id, db)


@router.get("/mrn/{mrn}")
def get_validate_patient_data_by_mrn(mrn: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.mrn == mrn).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return build_patient_record(patient.id, db)