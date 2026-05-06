# backend/seed.py

import json
from pathlib import Path
from datetime import date

from backend.database import SessionLocal
from backend.models.patient import Patient
from backend.models.medication import Medication


BASE_DIR = Path(__file__).resolve().parent
SEED_DATA_DIR = BASE_DIR / "sample_data"


def load_json_files(folder_name: str):
    folder = SEED_DATA_DIR / folder_name

    if not folder.exists():
        print(f"Seed folder not found: {folder}")
        return []

    records = []

    for file_path in folder.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            records.append({
                "file_path": file_path,
                "data": json.load(file)
            })

    return records

def get_or_create_patient(db, mrn: str, first_name, last_name, date_of_birth):

    patient = db.query(Patient).filter(Patient.mrn == mrn).first()

    if patient:
        # Update demographics only if new info exists
        if first_name:
            patient.first_name = first_name
        if last_name:
            patient.last_name = last_name
        if date_of_birth:
            print(date_of_birth)
            if isinstance(date_of_birth, int):
                today = date.today()

                patient.date_of_birth = date(today.year - date_of_birth, 1, 1)
            else:
                patient.date_of_birth = date_of_birth

        db.commit()
        db.refresh(patient)
        return patient

    if isinstance(date_of_birth, int):
        today = date.today()
        new_date = date(today.year - date_of_birth, 1, 1)

    patient = Patient(
        mrn=mrn,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=new_date,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient

def seed_reconcile_cases(db):
    cases = load_json_files("reconcile")

    for case in cases:
        # Adjust these field names to match your real JSON.
        print(case)
        
        file_path = case["file_path"]
        patient_data = case["data"]

        existing_patient = get_or_create_patient(db, mrn=f"RECON-{file_path.stem.upper()}", first_name=None, last_name=None, date_of_birth=patient_data["patient_context"]["age"])

        

        for med_data in case.get("medications", []):
            existing_med = (
                db.query(Medication)
                .filter(
                    Medication.patient_id == existing_patient.id,
                    Medication.medication == med_data["medication"],
                    Medication.system == med_data["system"],
                )
                .first()
            )

            if existing_med:
                continue

            medication = Medication(
                patient_id=existing_patient.id,
                system=med_data["system"],
                medication=med_data["medication"],
                last_updated=date.fromisoformat(med_data["last_updated"]),
                source_reliability=med_data["source_reliability"],
            )

            db.add(medication)

    db.commit()
    print(f"Seeded {len(cases)} reconcile cases.")


def main():
    db = SessionLocal()

    try:
        seed_reconcile_cases(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()