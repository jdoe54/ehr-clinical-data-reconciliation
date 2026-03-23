from openai import OpenAI
from typing import Literal
from dotenv import load_dotenv

import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AI_MODEL = "gpt-5.4-nano"


def judge_medication_reasonableness(
    current_age: int | str,
    current_condition: str,
    recent_procedures: str,
    medication: str,
) -> Literal["Yes", "No"]:
    
    medication_input = f"""
    Evaluate whether the following medication is safe for the patient.

    Age: {current_age}
    Conditions: {current_condition}
    Recent procedures: {recent_procedures}
    Medication: {medication}

    Return exactly one token:
    Yes
    or
    No
    """



    response = client.responses.create(
        model=AI_MODEL,
        reasoning={"effort": "high"},
        input=medication_input,
    )

    text = response.output_text.strip()

    if text not in {"Yes", "No"}:
        raise ValueError(f"Unexpected medication reasonableness response: {text}")

    return text


def generate_reconciliation_reasoning(
    current_age: int | str,
    current_condition: str,
    recent_procedures: str,
    confidence: float,
    winner_case: str,
    runner_case: str,
) -> dict:
    
    reasoning_input = ()
    
    if runner_case == None:
        reasoning_input = (
            f"Patient age: {current_age}. "
            f"Conditions: {current_condition}. "
            f"Recent procedures: {recent_procedures}. "
            f"Confidence level: {confidence}. "
            f"Explain in less than 50 words that {winner_case} is only record. "
            f"Return exactly three sections separated by ||. "
            f"Section 1: reasoning, one sentence, no line breaks. "
            f"Section 2: recommended actions separated only by @@. If none, write None. "
            f"Section 3: output only PASSED or FAILED if medication is safe for use. "
            f"Do not use bullets, numbering, or newline characters."
        )
    else:
        reasoning_input = (
            f"Patient age: {current_age}. "
            f"Conditions: {current_condition}. "
            f"Recent procedures: {recent_procedures}. "
            f"Confidence level: {confidence}. "
            f"Explain in less than 50 words why {winner_case} is better than {runner_case}. "
            f"Return exactly three sections separated by ||. "
            f"Section 1: reasoning, one sentence, no line breaks. "
            f"Section 2: recommended actions separated only by @@. If none, write None. "
            f"Section 3: output only PASSED or FAILED if medication is safe for use. "
            f"Do not use bullets, numbering, or newline characters."
        )

    response = client.responses.create(
        model=AI_MODEL,
        reasoning={"effort": "high"},
        input=reasoning_input,
    )

    text = response.output_text.strip()
    parts = [part.strip() for part in text.split("||")]

    if len(parts) != 3:
        raise ValueError(f"Unexpected reasoning response format: {text}")

    reasoning, actions_raw, status = parts

    if actions_raw == "None":
        actions = []
    else:
        actions = [a.strip() for a in actions_raw.split("@@") if a.strip()]

    if status not in {"PASSED", "FAILED"}:
        raise ValueError(f"Unexpected status in reasoning response: {status}")

    return {
        "reasoning": reasoning,
        "recommended_actions": actions,
        "status": status,
    }