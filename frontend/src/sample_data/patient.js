export const patients_data = [

    {
        id: 1, 
        name: "John Doe",
        reconcilePayload: {
            "patient_context": {
                "age": 55,
                "conditions": ["Asthma"],
                "recent_labs": {"eGFR": 45}
            },

            "sources": [{
                "system": "Hospital EHR",
                "medication": "Albuterol",
                "last_updated": "2024-10-15",
                "source_reliability": "high"
            }]
        },
        dataQualityPayload: {
            demographics: {
                name: "John Doe",
                dob: "1970-03-15",
                gender: "M"
            },
            medications: ["Albuterol inhaler"],
            allergies: ["Penicillin"],
            conditions: ["Asthma"],
            vital_signs: {
                blood_pressure: "128/78",
                heart_rate: 72
            },
            last_updated: "2026-02-15"
        }
        
    },
    {
        id: 2,
        name: "Jane Doe",
        reconcilePayload: {
            "patient_context": {
                "age": 64,
                "conditions": ["Type 2 Diabetes", "Hypertension"],
                "recent_labs": {"eGFR": 45}
            },

            "sources": [
                {
                    "system": "Hospital EHR",
                    "medication": "Metformin 1000mg twice daily",
                    "last_updated": "2024-10-15",
                    "source_reliability": "high"
                },
                
                {
                    "system": "Primary Care",
                    "medication": "Metformin 500mg twice daily",
                    "last_updated": "2025-01-20",
                    "source_reliability": "high"
                },
                {
                    "system": "Pharmacy",
                    "medication": "Metformin 1000mg daily",
                    "last_filled": "2025-01-25",
                    "source_reliability": "medium"
                }
            ]
        },
        dataQualityPayload: {
            "demographics": 
                {
                    "name": "Jane Doe", 
                    "dob": "1961-03-15", 
                    "gender": "F"
                },

            "medications": 
                [
                    "Metformin 500mg", 
                    "Lisinopril 10mg"
                ],
            "allergies": [],
            "conditions": 
                [
                    "Type 2 Diabetes"
                ],
            "vital_signs": 
                {
                    "blood_pressure": "340/180", 
                    "heart_rate": 72
                },
            "last_updated": "2024-06-15"
        }
    },
    {
        id: 3,
        name: "Bob Doe",
        reconcilePayload: {
            "patient_context": {
                "age": 67,
                "conditions": ["Type 2 Diabetes", "Hypertension"],
                "recent_labs": {"eGFR": 72}
            },
            
            "sources": [
                {
                    "system": "Hospital EHR",
                    "medication": "Metformin 1000mg twice daily",
                    "last_updated": "2025-02-10",
                    "source_reliability": "high"
                },
                {
                    "system": "Primary Care",
                    "medication": "Metformin 500mg twice daily",
                    "last_updated": "2025-01-20",
                    "source_reliability": "high"
                },
                {
                    "system": "Pharmacy",
                    "medication": "Metformin 1000mg daily",
                    "last_filled": "2025-01-25",
                    "source_reliability": "medium"
                }
            ]
        },
        dataQualityPayload: {
            "demographics": {
                "name": "Bob Doe",
                "dob": "1958-02-11",
                "gender": "M"
            },
            "medications": [],
            "allergies": [],
            "conditions": [],
            "vital_signs": {},
            "last_updated": "2026-02-15"
        }

    }, 
    {
        id: 4,
        name: "Samantha Doe",
        reconcilePayload: {
            "patient_context": {
                "age": 82,
                "conditions": ["Type 2 Diabetes", "Chronic Kidney Disease"],
                "recent_labs": {"eGFR": 22}
            },
            "sources": [
                {
                    "system": "Hospital EHR",
                    "medication": "Metformin 1000mg twice daily",
                    "last_updated": "2025-02-01",
                    "source_reliability": "high"
                },
                {
                    "system": "Primary Care",
                    "medication": "Metformin 500mg daily",
                    "last_updated": "2025-01-28",
                    "source_reliability": "high"
                },
                {
                "system": "Pharmacy",
                "medication": "Metformin 1000mg daily",
                "last_filled": "2025-02-03",
                "source_reliability": "medium"
                }
            ]
        },
        dataQualityPayload: {
            "demographics": {
                "name": "Samantha Doe",
                "dob": "1941-08-14",
                "gender": "F"
            },
            "medications": [
                "Metformin 500mg"
            ],
            "allergies": [],
            "conditions": [
                "Type 2 Diabetes"
            ],
            "vital_signs": {
                "blood_pressure": "130/82",
                "heart_rate": 70
            },
            "last_updated": "2023-11-01"
        }

    }

    

]