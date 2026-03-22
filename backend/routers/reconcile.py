from fastapi import APIRouter
from ..schema import MedicationReconciliationRequest, MedicationReconciliationResponse
from datetime import datetime
from backend.services.llm_service import (
    judge_medication_reasonableness,
    generate_reconciliation_reasoning,
)

import os
import re



router = APIRouter(prefix="/api/reconcile", tags=["reconcile"])


MAX_WEIGHT_SCORE = 5

MAX_ADDITIONAL_MED_SCORE = 1

MAX_SOURCE_VALIDITY_SCORE = 3
MEDIUM_SOURCE_VALIDITY_SCORE = 2
LOW_SOURCE_VALIDITY_SCORE = 1

MAX_MOST_RECENT_SCORE = 3
RECENT_DATE_FILLED_SCORE = 1


MAX_REDUCE_RECENT_SCORE = -2
MAX_OUTRAGEOUS_SCORE = -3
MAX_REDUCE_CLOSE_DAY_SCORE = -2
REDUCE_CLOSE_DAY_SCORE = -1

MAX_SCORE = MAX_WEIGHT_SCORE + MAX_ADDITIONAL_MED_SCORE + MAX_SOURCE_VALIDITY_SCORE + MAX_MOST_RECENT_SCORE


@router.post("/medication")
def reconcile_medication(data: MedicationReconciliationRequest):

    reliability_score = {}
    time_info = {}
    previous_entries = set()
    actions = []

    SOURCE_WEIGHTS = {
        "Pharmacy": MAX_WEIGHT_SCORE,
        "Hospital EHR": 4,
        "Specialist EHR": 4,
        "Primary Care": 3,
        "Patient Self Report": 2,
        "Old External Record": 1
    }

    current_date = datetime.today().date()

    medication_list = data.sources
    current_condition = data.patient_context.conditions
    current_age = data.patient_context.age
    recent_procedures = data.patient_context.recent_labs

    recent_date = None
    recent_date_index = None



    def logger(index: int, message: str):
        actions[index].append(message)

    for index, source in enumerate(medication_list):
        location = source.system

        # Given a base score based on location. Max score is 5.

        reliability_score[index] = SOURCE_WEIGHTS[location]
        actions.append([]) 

        logger(index, "Starting with " + str(reliability_score[index]))

        # Found additional sources with similar medication, an extra 1 point.

        meds = re.search(r'(\d+(?:\.\d+)?)\s*(mg|mcg|g|mL|units|tablets)(?:\s*/\s*(\d+(?:\.\d+)?)\s*(mL|L))?', source.medication, re.IGNORECASE)

        if meds in previous_entries:
            reliability_score[index] += MAX_ADDITIONAL_MED_SCORE
            logger(index, "Add 1 for previous medication found")
        
        previous_entries.add(meds)

        # Medication, say yes if good. Say no if not.

    
        medication_ok = judge_medication_reasonableness(
            current_age=current_age,
            current_condition=current_condition,
            recent_procedures=recent_procedures,
            medication=source.medication,
        )

        if medication_ok.upper() == "YES":
            logger(index, "No changes, not outrageous.")
        elif medication_ok.upper() == "NO":
            logger(index, "Reduce 3 for being outrageous.")
            reliability_score[index] += MAX_OUTRAGEOUS_SCORE

        # Increase reliability based on source reliability. Max score is 3.

        if source.source_reliability == "low":
            reliability_score[index] += LOW_SOURCE_VALIDITY_SCORE
            logger(index, "Add 1 for low site reliability")
            
        elif source.source_reliability == "medium":
            reliability_score[index] += MEDIUM_SOURCE_VALIDITY_SCORE
            logger(index, "Add 2 for medium site reliability")
        elif source.source_reliability == "high":
            reliability_score[index] += MAX_SOURCE_VALIDITY_SCORE
            logger(index, "Add 3 for high site reliability")

        # This checks to see if date is the most recent. Max score is 3

        recency = source.last_updated or source.last_filled

        if recency is not None:

            source_date = datetime.strptime(recency, "%Y-%m-%d").date()
        
            # Get relative distance from current date to current date

            time_delta = current_date - source_date
            time_info[index] = time_delta

            if recent_date is None:
                recent_date = time_delta.days 
                recent_date_index = index
            elif recent_date >= time_delta.days:
                recent_date = time_delta.days 
                recent_date_index = index

    if recent_date is not None:
        reliability_score[recent_date_index] += MAX_MOST_RECENT_SCORE
        logger(index, "Add 3 for being most recent.")
    
    # Reduce score if times are very close to one another

    time_info_list = time_info.items()

    

    for first_index, first_source in enumerate(time_info_list):
        for second_index, second_source in enumerate(time_info_list):
            if first_index != second_index:
                difference = abs(first_source[1].days - second_source[1].days)
                
                if difference < 10:
                   
                    logger(first_index, "Reduce 2 for being close in time distance by 10 days.")
                    reliability_score[first_index] += MAX_REDUCE_CLOSE_DAY_SCORE
                    break
                elif difference < 20:
                    
                    
                    logger(first_index, "Reduce 1 for being close in time distance by 20 days.")
                    reliability_score[first_index] += REDUCE_CLOSE_DAY_SCORE
                    break
    
    winning_score = None
    winning_index = None

    runner_up_score = None
    runner_up_index = None

    for index, source in enumerate(actions):
        print("ENTRY: " + str(index+1) + " | LOCATION: " + str(data.sources[index].system) + " ============================")
        for log_action in source:
            print(log_action)
        print("SCORE: " + str(reliability_score[index]))

        if winning_score is not None:
            #print("Found winning score not none")
            #print("Comparing against " + str(reliability_score[index]) + " against " + str(winning_score))
            if reliability_score[index] >= winning_score:
                runner_up_index = winning_index
                runner_up_score = winning_score

        if winning_score is None or reliability_score[index] >= winning_score:
            #print("Winning score being changed due to " + str(index))
            winning_score = reliability_score[index]
            winning_index = index
    
    #print("WINNER: " + str(winning_score) + " | Entry: " + str(winning_index))
    #print("RUNNER UP: " + str(runner_up_score) + " | Entry: " + str(runner_up_index))

    if runner_up_index is None:
        runner_up_score = 0
        runner_up_index = -1

    normalized_strength = winning_score / MAX_SCORE

    margin = (winning_score - runner_up_score) / max(winning_score, 1e-9)

    confidence = 0.7 * normalized_strength + 0.3 * margin
    
    #print("CONFIDENCE LEVELS: " + str(round(confidence, 3)))


    def build_case(source: dict):
        
        parts = [
            getattr(source, "system", None),
            getattr(source, "medication", None),
            getattr(source, "last_updated", None),
            getattr(source, "last_filled", None),
            getattr(source, "source_reliability", None),
        ]

        complete_case = ", ".join(str(part) for part in parts if part is not None)
        return complete_case

    winner_case = build_case(medication_list[winning_index])
    runner_case = None

    print(str(runner_up_index) + " is runner up")
    print(winning_index)
    
    if runner_up_index is not winning_index:

        print("Winning index is not the same")
        runner_case = build_case(medication_list[runner_up_index])

    print("Still going hehe")
 

    reasoning_result = generate_reconciliation_reasoning(
        current_age=current_age,
        current_condition=current_condition,
        recent_procedures=recent_procedures,
        confidence=confidence,
        winner_case=winner_case,
        runner_case=runner_case,
    )

    response = MedicationReconciliationResponse(
        reconciliated_medication = medication_list[winning_index].medication,
        reasoning = reasoning_result['reasoning'],
        recommended_actions = reasoning_result['recommended_actions'],
        clinical_safety_check = reasoning_result['status'],
        confidence_score = round(confidence, 3)
    )

    return response