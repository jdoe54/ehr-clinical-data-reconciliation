from fastapi import APIRouter, Depends
from ..schema import DataIssueDetected, DataQualityRequest, DataQualityResponse, Breakdown
from ..auth import verify_token
from datetime import datetime


import re



router = APIRouter(prefix="/api/validate", tags=["validate"])

AI_MODEL = "gpt-5.4-nano"



@router.post("/data-quality")
def validate_data_quality(data: DataQualityRequest, token: str = Depends(verify_token)):

    # high severity - physiologically implausible, 
    # medium severity - incomplete info and old date
    # low severity - formatting issues

    current_date = datetime.today().date()

    MAX_BPM = 180
    MIN_BPM = 40

    MAX_SYSTOLIC = 200
    MAX_DIASTOLIC = 120

    ALLOWED_GENDERS = {"M", "F", "Other", "Unknown", "Male", "Female"}
    log = []

    completeness_score = 100
    timeliness_score = 100
    clinical_plausibility_score = 100
    accuracy_score = 100
    overall_score = 100

    # 80 - 40 is High
    # 39 - 21 is Medium
    # 20 - 5 is Low

    def logger(field: str, issue: str, severity: str):
        log.append([field, issue, severity])

    # Check to see if data is present in field

    for field, value in enumerate(data):
        if not value:
            logger(field, "Incomplete data at " + field + ".", "medium")
            completeness_score -= 10 
    

    # Check to see if date is not too long ago
         
    if getattr(data, "last_updated"):
        source_date = datetime.strptime(data.last_updated, "%Y-%m-%d").date()
        time_delta = current_date - source_date

        if time_delta.days > 180:
            logger("last_updated", "Data is more than 6 months old.", "medium")
            timeliness_score -= 50
        elif time_delta.days < 0:
            logger("last_updated", "Last updated date is in the future.", "low")
            clinical_plausibility_score -= 40
            timeliness_score = 0
        else:
            reduce = (time_delta.days / 180) * 50
            logger("last_updated", "Data is more than " + str(time_delta.days) + " days old", "low")
            timeliness_score -= int(reduce)

    else:
        logger("last_updated", "Last updated date field is missing.", "low")
        completeness_score -= 20

    
    # Check to see DOB is not in the future

    if getattr(data, "demographics"):
        if data.demographics.get("dob"):
            source_date = datetime.strptime(data.last_updated, "%Y-%m-%d").date()
            time_delta = current_date - source_date

            if time_delta.days < 0:
                logger("demograhics", "Date of birth is in the future.", "high")
                clinical_plausibility_score -= 40
        else:
            logger("demograhics", "No date of birth present.", "high")
            clinical_plausibility_score -= 40
        
        if data.demographics.get("gender"):
            if data.demographics.get("gender") not in ALLOWED_GENDERS:
                logger("demograhics", "Gender formatting issues.", "low")
                accuracy_score -= 10
    else:
        logger("demographics", "Missing demographics field", "low")
        completeness_score -= 20

    # Check to see if allergies has any values


    if hasattr(data, "allergies"):
   
        if len(data.allergies) == 0:
            logger("allergies", "No allergies documented. Include none documented", "low")
            completeness_score -= 20
    else:
        logger("allergies", "Missing allergies field", "low")
        completeness_score -= 20

    # Check to see vital signs are not too crazy

    if getattr(data, "vital_signs"):
        if data.vital_signs.get("blood_pressure"):
            bp = data.vital_signs.get("blood_pressure").split("/")

            # Check to see if format is correct
            if len(bp) == 1:
                logger("blood_pressure", "Formatting issue.", "low")
                completeness_score -= 10
            else:
                # Check to see if blood pressure is too high or low
                if int(bp[0]) >= MAX_SYSTOLIC or int(bp[1]) >= MAX_DIASTOLIC:
                    logger("blood_pressure", "Too high systolic and or diastolic.", "high")
                    clinical_plausibility_score -= 60

        # Check to see if HR is high or low
        if data.vital_signs.get("heart_rate"):
            hr = int(data.vital_signs.get("heart_rate"))

            if hr > MAX_BPM:
                logger("heart_rate", "Too high heart rate,", "high")
                clinical_plausibility_score -= 60
            elif hr < MIN_BPM:
                logger("heart_rate", "Too low heart rate.", "high")
                clinical_plausibility_score -= 60
        else:
            logger("heart_rate", "Missing heart rate field", "low")
            completeness_score -= 5
    else:
        logger("vital_signs", "Missing vital signs field", "low")
        completeness_score -= 20
            
    
    # Check to see if medications do not duplicate

    if getattr(data, "medications"):
        current_meds = set()

        for med in data.medications:
            med_word = re.sub(r"\s*\d.*$", "", med).strip().lower()

            if med in current_meds:
                accuracy_score -= 40
                logger("medications", "Duplicate medication.", "medium")
            
            current_meds.add(med_word)
    else:
        logger("medications", "Missing medications field", "low")
        completeness_score -= 20

    # Checks to see if conditions does not exist
    if getattr(data, "conditions") == False:
        logger("conditions", "Missing conditions field", "low")
        completeness_score -= 20
    else:
        if len(data.conditions) == 0:
            logger("conditions", "No conditions documented. Include none documented", "low")
            completeness_score -= 20

    issues = []
    for entry in log:
        issues.append(DataIssueDetected(
            field=entry[0],
            issue=entry[1],
            severity=entry[2]
            )
        )

    overall_score = int((completeness_score + timeliness_score + clinical_plausibility_score + accuracy_score) / 4)

    response = DataQualityResponse(
        overall_score=overall_score,
        breakdown=Breakdown(
            completeness=max(0, completeness_score),
            accuracy=max(0, accuracy_score),
            timeliness=max(0, timeliness_score),
            clinical_plausibility=max(0, clinical_plausibility_score)
        ),
        issues_detected=issues

    )


    return response
