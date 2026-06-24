from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.patient import Patient
from backend.models.medication import Medication
from backend.models.allergies import Allergies
from backend.models.conditions import Conditions
from backend.models.lab_results import Labs
from backend.models.vital_signs import VitalSigns

def serialize_date(value):
    return value.isoformat() if value else None

def get_patient(db: Session, patient_id: int | None = None, mrn: str | None = None):
    if patient_id is not None:
        patient =  db.query(Patient).filter(Patient.id == patient_id).first()
    elif mrn is not None:
        patient = db.query(Patient).filter(Patient.mrn == mrn).first()
    else:
        raise HTTPException(status_code=400, detail="patient_id or mrn is required")

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    

    return patient


def build_patient_record(db: Session, patient_id: int | None = None, mrn: str | None = None):
    print("Testing the building of the patient record")
    print(mrn)
    print(patient_id)
    patient = get_patient(db, patient_id=patient_id, mrn=mrn)

    medications = db.query(Medication).filter(Medication.patient_id == patient.id).all()
    allergies = db.query(Allergies).filter(Allergies.patient_id == patient.id).all()
    conditions = db.query(Conditions).filter(Conditions.patient_id == patient.id).all()
    lab_results = db.query(Labs).filter(Labs.patient_id == patient.id).all()
    vital_signs = db.query(VitalSigns).filter(VitalSigns.patient_id == patient.id).all()

    return {
        "patient": {
            "id": patient.id,
            "mrn": patient.mrn,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": serialize_date(patient.date_of_birth),
            "gender": patient.gender,
            "age_years": patient.age_years,
            "last_updated": patient.last_updated,
        },
        "medications": [
            {
                "id": med.id,
                "system": med.system,
                "medication": med.medication,
                "last_updated": serialize_date(med.last_updated),
                "source_reliability": med.source_reliability,
            }
            for med in medications
        ],
        "allergies": [
            {
                "id": allergy.id,
                "allergen": allergy.allergen,
                "reaction": allergy.reaction,
            }
            for allergy in allergies
        ],
        "conditions": [
            {
                "id": condition.id,
                "condition_name": condition.condition_name,
            }
            for condition in conditions
        ],
        "lab_results": [
            {
                "id": lab.id,
                "lab_name": lab.lab_name,
                "value": lab.value,
                "unit": lab.unit,
            }
            for lab in lab_results
        ],
        "vital_signs": [
            {
                "id": vitals.id,
                "systolic_bp": vitals.systolic_bp,
                "diastolic_bp": vitals.diastolic_bp,
                "heart_rate": vitals.heart_rate,
                "last_updated": serialize_date(vitals.last_updated),
            }
            for vitals in vital_signs
        ],
    }