import json
import os
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")

AUTH_HEADERS = {"X-API-Key": "dev-secret"}

from unittest.mock import patch


def load_case(subpath: str, filename: str):
    filepath = os.path.join(SAMPLE_DATA_DIR, subpath, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@patch("backend.routers.reconcile.generate_reconciliation_reasoning")
@patch("backend.routers.reconcile.judge_medication_reasonableness")
def test_reconcile_case_1_returns_200(mock_judge, mock_reasoning):
    payload = load_case("reconcile", "case01_single.json")
    mock_judge.return_value = "YES"
    mock_reasoning.return_value = {
        "reasoning": "Only available Hospital EHR entry shows Albuterol on 2024-10-15 with “high” severity, and no other asthma-related records are present in the provided data.",
        "recommended_actions": [
            "Review the chart to confirm no other asthma exacerbations or inhalers are missing",
            "Assess current asthma control and need for controller therapy",
            "Consider renal function (eGFR 45) when reviewing medication choices"
        ],
        "status": "PASSED"
        
    }
    response = client.post(
        "/api/reconcile/medication",
        json=payload,
        
    )
    assert response.status_code == 200


@patch("backend.routers.reconcile.generate_reconciliation_reasoning")
@patch("backend.routers.reconcile.judge_medication_reasonableness")
def test_reconcile_case_2_returns_200(mock_judge, mock_reasoning):
    payload = load_case("reconcile", "case02_dose.json")
    mock_judge.return_value = "YES"
    mock_reasoning.return_value = {
        "reasoning": "Pharmacy record with Metformin 1000mg daily on 2025-01-25 is preferable to Hospital EHR noting 1000mg twice daily on 2024-10-15 because current dosing aligns better with renal risk at eGFR 45 and may reflect updated prescribing",
        "recommended_actions": [
            "Verify current metformin dose across records",
            "Reconcile medication list with the prescriber",
            "Monitor eGFR and consider B12 periodically",
            "Educate patient on correct daily dosing"
        ],
        "status": "PASSED"
    }


    response = client.post(
        "/api/reconcile/medication",
        json=payload,
        
    )

   
     
    assert response.status_code == 200


@patch("backend.routers.reconcile.generate_reconciliation_reasoning")
@patch("backend.routers.reconcile.judge_medication_reasonableness")
def test_reconcile_case_3_returns_200(mock_judge, mock_reasoning):
    # Hospital preference
    payload = load_case("reconcile", "case03_hospital.json")
    mock_judge.return_value = "YES"
    mock_reasoning.return_value = {
        "reasoning": "With eGFR 72, metformin 1000mg BID documented in Hospital EHR on 2025-02-10 likely provides stronger glycemic control than the earlier pharmacy record of 1000mg daily (2025-01-25) while remaining renal-safe for a 67-year-old.",
        "recommended_actions": [
            "Verify current dosing across records",
            "Review A1c and hypoglycemia risk",
            "Monitor renal function periodically"
        ],
        "status": "PASSED"
    }

    response = client.post(
        "/api/reconcile/medication",
        json=payload,
        
    )

    data = response.json()
    assert data['reconciliated_medication'] == "Metformin 1000mg twice daily"
    assert response.status_code == 200


@patch("backend.routers.reconcile.generate_reconciliation_reasoning")
@patch("backend.routers.reconcile.judge_medication_reasonableness")
def test_reconcile_case_4_returns_200(mock_judge, mock_reasoning):
    # Unsafe preference
    payload = load_case("reconcile", "case04_unsafe.json")
    mock_judge.return_value = "YES"
    mock_reasoning.return_value = {
        "reasoning": "With eGFR 22, twice-daily metformin increases lactic-acidosis risk; the pharmacy record uses a lower 1000 mg daily dose and later review, making it a safer interim choice than the higher-dose hospital EHR entry",
        "recommended_actions": [
            "Stop or hold metformin due to eGFR 22",
            "Check renal function and assess for lactic-acidosis symptoms",
            "Switch to CKD-appropriate diabetes therapy",
            "Urgently notify the prescriber/nephrology for regimen adjustment"
        ],
        "status": "FAILED"
    }

    response = client.post(
        "/api/reconcile/medication",
        json=payload,
        
    )
    data = response.json()

    print(data)
    assert data['clinical_safety_check'] == "FAILED"
    assert response.status_code == 200


