from pydantic import BaseModel
from typing import Any, List, Dict, Optional

class PatientContext(BaseModel):
    age: int
    conditions: List[str]
    recent_labs: Dict[str, float]

class MedicationSource(BaseModel):
    system: str
    medication: str
    last_filled: Optional[str] = None
    last_updated: Optional[str] = None
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

class DataQualityRequest(BaseModel):
    demographics: Dict[str, Any]
    medications: List[str]
    allergies: List[str]
    conditions: List[str]
    vital_signs: Dict[str, Any]
    last_updated: str    

class Breakdown(BaseModel):
    completeness: int
    accuracy: int
    timeliness: int
    clinical_plausibility: int

class DataIssueDetected(BaseModel):
    field: str
    issue: str
    severity: str

class DataQualityResponse(BaseModel):
    overall_score: int
    breakdown: Breakdown
    issues_detected: List[DataIssueDetected]

