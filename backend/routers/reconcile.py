from fastapi import APIRouter
from ..schema import MedicationReconciliationRequest, MedicationReconciliationResponse
from datetime import datetime
import re

router = APIRouter(prefix="/api/reconcile", tags=["reconcile"])

@router.post("/medication")
def reconcile_medication(data: MedicationReconciliationRequest):

    reliability_score = {}
    time_info = {}
    previous_entries = set()

    SOURCE_WEIGHTS = {
        "Hospital EHR": 1.0,
        "Specialist EHR": 0.9,
        "Pharmacy": 0.85,
        "Primary Care": 0.6,
        "Old External Record": 0.5
    }

    current_date = datetime.today().date()

    medication_list = data.sources
    current_condition = data.patient_context.conditions
    current_age = data.patient_context.age

    recent_date = None
    recent_date_index = None



    

    for index, source in enumerate(medication_list):
        location = source.system

        print(location)

        print(SOURCE_WEIGHTS)
        reliability_score[index] = SOURCE_WEIGHTS[location]

        # Found additional sources with similar medication

        meds = re.search(r'(\d+(?:\.\d+)?)\s*(mg|mcg|g|mL|units|tablets)(?:\s*/\s*(\d+(?:\.\d+)?)\s*(mL|L))?', source.medication, re.IGNORECASE)

        if meds in previous_entries:
            reliability_score[index] += 1
        
        previous_entries.add(meds)

        # Increase reliability based on source reliability

        if source.source_reliability == "low":
            reliability_score[index] += 1
        elif source.source_reliability == "medium":
            reliability_score[index] += 2
        elif source.source_reliability == "high":
            reliability_score[index] += 3

        # This checks to see if date is the most recent

        recency = source.last_updated or source.last_filled

        if recency is not None:

            source_date = datetime.strptime(recency, "%Y-%m-%d").date()
        
            if recent_date == None or recent_date < source_date:
                if recent_date_index is not None:
                    reliability_score[recent_date_index] -= 2

                reliability_score[index] += 3

                recent_date = source_date
                recent_date_index = index
            else:
                reliability_score[index] += 1

            # Get relative distance from current date to current date

            time_delta = current_date - source_date
            time_info[location] = time_delta

    
    # Reduce score if times are very close to one another

    time_info_list = time_info.items()

    for first_index, first_day in time_info_list:
        for second_index, second_day in time_info_list:
            difference = abs(first_day.days - second_day.days)
            if difference < 10:
                reliability_score[first_index] -= 2
            elif difference < 20:
                reliability_score[first_index] -= 1

    print(reliability_score)
        
    response = MedicationReconciliationResponse()
    return response