from pydantic import BaseModel
from typing import List, Dict

class PatientContext(BaseModel):
    age: int
    conditions: List[str]
    recent_labs: Dict[str, float]

class MedicationSource(BaseModel):
    system: str
    medication: str
    last_updated: str
    source_reliability: str

class MedicationReconciliationRequest(BaseModel):
    patient_context: PatientContext
    sources: List[MedicationSource]


class MedicationReconciliationResponse(BaseModel):
    reconciliated_medication: str
    confidence_score: float
    reasoning: str
    recommended_actions: List[str]
    clinical_safety_check: str