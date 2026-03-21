from fastapi import APIRouter
from ..schema import MedicationReconciliationRequest

router = APIRouter(prefix="/api/reconcile", tags=["reconcile"])

@router.post("/medication")
def reconcile_medication(data: MedicationReconciliationRequest):
    
    return {"Age": data.patient_context.age}