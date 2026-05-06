from datetime import date
from database import SessionLocal
from models.patient import Patient

db = SessionLocal()

patient = Patient(
    first_name="John",
    last_name="Doe",
    date_of_birth=date(1980, 1, 15),

)

db.add(patient)
db.commit()
db.close()

print("Seeded patient.")