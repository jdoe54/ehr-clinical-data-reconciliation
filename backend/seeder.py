import json
from pathlib import Path
from datetime import date

from backend.database import SessionLocal
from backend.models.patient import Patient
from backend.models.medication import Medication
from backend.models.conditions import Conditions
from backend.models.lab_results import Labs
from backend.models.allergies import Allergies
from backend.models.vital_signs import VitalSigns


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
                "data": json.load(file),
            })

    return records


def parse_date(value):
    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return date.fromisoformat(value)

    return None


def split_name(name_value):
    if not name_value:
        return None, None

    if isinstance(name_value, dict):
        return name_value.get("first"), name_value.get("last")

    parts = str(name_value).split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else None

    return first_name, last_name


def parse_blood_pressure(value):
    if not value:
        return None, None

    if isinstance(value, dict):
        return value.get("systolic"), value.get("diastolic")

    if isinstance(value, str) and "/" in value:
        systolic, diastolic = value.split("/", 1)
        return int(systolic), int(diastolic)

    return None, None


def get_or_create_patient(
    db,
    mrn: str,
    first_name=None,
    last_name=None,
    date_of_birth=None,
    gender=None,
    age_years=None,
):
    patient = db.query(Patient).filter(Patient.mrn == mrn).first()
    parsed_dob = parse_date(date_of_birth)

    if patient:
        if first_name is not None:
            patient.first_name = first_name

        if last_name is not None:
            patient.last_name = last_name

        if parsed_dob is not None:
            patient.date_of_birth = parsed_dob

        if gender is not None:
            patient.gender = gender

        if age_years is not None:
            patient.age_years = age_years

        db.flush()
        return patient

    patient = Patient(
        mrn=mrn,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=parsed_dob,
        gender=gender,
        age_years=age_years,
    )

    db.add(patient)
    db.flush()

    return patient


def get_medication_name(med):
    if isinstance(med, dict):
        return (
            med.get("medication")
            or med.get("name")
            or med.get("drug")
            or med.get("display")
        )

    if med is None:
        return None

    return str(med)


def add_medication_if_missing(
    db,
    patient_id: int,
    medication_name: str | None,
    system: str = "unknown",
    source_reliability: str = "unknown",
    last_updated=None,
):
    if not medication_name:
        return

    existing = (
        db.query(Medication)
        .filter(
            Medication.patient_id == patient_id,
            Medication.medication == medication_name,
            Medication.system == system,
        )
        .first()
    )

    if existing:
        return

    db.add(
        Medication(
            patient_id=patient_id,
            system=system,
            medication=medication_name,
            last_updated=parse_date(last_updated),
            source_reliability=source_reliability,
        )
    )


def add_condition_if_missing(db, patient_id: int, condition_name: str | None):
    if not condition_name:
        return

    existing = (
        db.query(Conditions)
        .filter(
            Conditions.patient_id == patient_id,
            Conditions.condition_name == condition_name,
        )
        .first()
    )

    if existing:
        return

    db.add(
        Conditions(
            patient_id=patient_id,
            condition_name=condition_name,
        )
    )


def add_lab_if_missing(
    db,
    patient_id: int,
    lab_name: str | None,
    value,
    unit=None,

):
    if not lab_name:
        return

    existing = (
        db.query(Labs)
        .filter(
            Labs.patient_id == patient_id,
            Labs.lab_name == lab_name,
        )
        .first()
    )

    if existing:
        return

    db.add(
        Labs(
            patient_id=patient_id,
            lab_name=lab_name,
            value=str(value) if value is not None else None,
            unit=unit,
         
        )
    )


def add_allergy_if_missing(
    db,
    patient_id: int,
    allergen: str | None,
    reaction=None,
):
    if not allergen:
        return

    existing = (
        db.query(Allergies)
        .filter(
            Allergies.patient_id == patient_id,
            Allergies.allergen == allergen,
        )
        .first()
    )

    if existing:
        return

    db.add(
        Allergies(
            patient_id=patient_id,
            allergen=allergen,
            reaction=reaction,
        )
    )


def add_vitals_if_missing(
    db,
    patient_id: int,
    systolic_bp=None,
    diastolic_bp=None,
    heart_rate=None,
    last_updated=None,
):
    existing = (
        db.query(VitalSigns)
        .filter(VitalSigns.patient_id == patient_id)
        .first()
    )

    if existing:
        return

    db.add(
        VitalSigns(
            patient_id=patient_id,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            heart_rate=heart_rate,
            last_updated=parse_date(last_updated),
        )
    )

def seed_reconcile_medications(db, patient_id: int, patient_data: dict):
    """
    Handles reconcile-style medication data.

    Expected flexible shapes:
    1.
    {
    "sources": [
        {
        "system": "EHR",
        "medication": "Metformin",
        "source_reliability": "high"
        }
    ]
    }

    2.
    {
    "sources": [
        {
        "system": "EHR",
        "source_reliability": "high",
        "medications": ["Metformin", "Lisinopril"]
        }
    ]
    }
    """

    sources = (
        patient_data.get("sources")
        or patient_data.get("medication_sources")
        or patient_data.get("source_records")
        or patient_data.get("records")
        or []
    )

    if isinstance(sources, dict):
        normalized_sources = []

        for source_name, source_value in sources.items():
            if isinstance(source_value, dict):
                source_value["system"] = source_value.get("system") or source_name
                normalized_sources.append(source_value)
            else:
                normalized_sources.append({
                    "system": source_name,
                    "medication": source_value,
                })

        sources = normalized_sources

    for source in sources:
        if not isinstance(source, dict):
            add_medication_if_missing(
                db=db,
                patient_id=patient_id,
                medication_name=str(source),
                system="reconcile",
                source_reliability="unknown",
            )
            continue

        system = (
            source.get("system")
            or source.get("source")
            or source.get("source_name")
            or "reconcile"
        )

        source_reliability = (
            source.get("source_reliability")
            or source.get("reliability")
            or "unknown"
        )

        last_updated = source.get("last_updated")

        if "medications" in source and isinstance(source["medications"], list):
            for med in source["medications"]:
                med_name = get_medication_name(med)

                add_medication_if_missing(
                    db=db,
                    patient_id=patient_id,
                    medication_name=med_name,
                    system=system,
                    source_reliability=source_reliability,
                    last_updated=last_updated,
                )
        else:
            med_name = get_medication_name(source)

            add_medication_if_missing(
                db=db,
                patient_id=patient_id,
                medication_name=med_name,
                system=system,
                source_reliability=source_reliability,
                last_updated=last_updated,
            )


def seed_reconcile_cases(db):
    cases = load_json_files("reconcile")

    for case_file in cases:
        file_path = case_file["file_path"]
        patient_data = case_file["data"]

        patient_context = patient_data.get("patient_context", {})

        patient = get_or_create_patient(
            db=db,
            mrn=f"RECON-{file_path.stem.upper()}",
            age_years=patient_context.get("age"),
        )

        for condition_name in patient_context.get("conditions", []):
            add_condition_if_missing(
                db=db,
                patient_id=patient.id,
                condition_name=condition_name,
            )

        recent_labs = patient_context.get("recent_labs", {})

        if isinstance(recent_labs, dict):
            for lab_name, lab_value in recent_labs.items():
                add_lab_if_missing(
                    db=db,
                    patient_id=patient.id,
                    lab_name=lab_name,
                    value=lab_value,
                    unit=None,
                )

        elif isinstance(recent_labs, list):
            for lab in recent_labs:
                if isinstance(lab, dict):
                    add_lab_if_missing(
                        db=db,
                        patient_id=patient.id,
                        lab_name=lab.get("name") or lab.get("lab_name"),
                        value=lab.get("value"),
                        unit=lab.get("unit"),
                        last_updated=lab.get("last_updated"),
                    )

        seed_reconcile_medications(
            db=db,
            patient_id=patient.id,
            patient_data=patient_data,
        )

    print(f"Seeded {len(cases)} reconcile cases.")


def seed_validate_cases(db):
    cases = load_json_files("validate")

    for case_file in cases:
        file_path = case_file["file_path"]
        data = case_file["data"]

        first_name, last_name = split_name(data.get("name"))

        patient = get_or_create_patient(
            db=db,
            mrn=f"VALIDATE-{file_path.stem.upper()}",
            first_name=first_name,
            last_name=last_name,
            date_of_birth=data.get("dob"),
            gender=data.get("gender"),
        )

        last_updated = data.get("last_updated")

        for med in data.get("medications", []):
            med_name = get_medication_name(med)

            add_medication_if_missing(
                db=db,
                patient_id=patient.id,
                medication_name=med_name,
                system="validate",
                source_reliability="unknown",
                last_updated=last_updated,
            )

        for allergy in data.get("allergies", []):
            if isinstance(allergy, dict):
                allergen = allergy.get("allergen") or allergy.get("name")
                reaction = allergy.get("reaction")
            else:
                allergen = str(allergy)
                reaction = None

            add_allergy_if_missing(
                db=db,
                patient_id=patient.id,
                allergen=allergen,
                reaction=reaction,
            )

        for condition_name in data.get("conditions", []):
            add_condition_if_missing(
                db=db,
                patient_id=patient.id,
                condition_name=condition_name,
            )

        vital_signs = data.get("vital_signs", {})
        systolic, diastolic = parse_blood_pressure(
            vital_signs.get("blood_pressure")
        )

        add_vitals_if_missing(
            db=db,
            patient_id=patient.id,
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            heart_rate=vital_signs.get("heart_rate"),
            last_updated=last_updated,
        )

    print(f"Seeded {len(cases)} validate cases.")


def main():
    db = SessionLocal()

    try:
        print("Starting seeder...")

        seed_reconcile_cases(db)
        seed_validate_cases(db)

        db.commit()
        print("Seeding complete.")

    except Exception:
        db.rollback()
        print("Seeder failed. Rolled back.")
        raise

    finally:
        db.close()
        print("Database session closed.")


if __name__ == "__main__":
    main()