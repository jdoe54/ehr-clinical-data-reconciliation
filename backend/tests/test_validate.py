import json
import os
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")




def load_case(subpath: str, filename: str):
    filepath = os.path.join(SAMPLE_DATA_DIR, subpath, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)



def test_validate_case_1():
    payload = {"patient_id": 5}
    
    response = client.post(
        "/api/validate/data-quality",
        json=payload,
    )
    assert response.status_code == 200


def test_validate_case_2():
    
    payload = {"patient_id": 6}
   
    response = client.post(
        "/api/validate/data-quality",
        json=payload,
    )

    data = response.json()
    
    assert response.status_code == 200
    assert data["breakdown"]["timeliness"] == 50
    assert data['overall_score'] <= 70



def test_validate_case_3():

    payload = {"patient_id": 7}

    response = client.post(
        "/api/validate/data-quality",
        json=payload,
    )

    data = response.json()
    assert response.status_code == 200
    assert data["breakdown"]["completeness"] < 40



def test_validate_case_4():
    payload = {"patient_id": 8}
   
    response = client.post(
        "/api/validate/data-quality",
        json=payload,
        
    )
    data = response.json()

    
    assert response.status_code == 200


