const API_BASE = "http://127.0.0.1:8000";
const TOKEN = "super-secret-ehr-token";

export async function reconcileMedication(payload) {
    const response = await fetch(`${API_BASE}/api/reconcile/medication`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${TOKEN}`
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error("Failed to reconcile medication");
    }

    return response.json();
}

export async function validateDataQuality(payload) {
    const response = await fetch(`${API_BASE}/api/validate/data-quality`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${TOKEN}`
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error("Failed to validate data quality");
    }

    return response.json();
}