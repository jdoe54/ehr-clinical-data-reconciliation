import { useState } from 'react'
import { reconcileMedication, validateDataQuality } from './services/api'

import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

const sampleReconcile = `{
  "patient_id": 
}`;

const sampleQuality = `{
  "demographics": {},
  "medications": [],
  "allergies": [],
  "conditions": [],
  "vital_signs": {},
  "last_updated": "2026-03-01"
}`;

export default function App() {
  const [reconcileInput, setReconcileInput] = useState(sampleReconcile);
  const [qualityInput, setQualityInput] = useState(sampleQuality);
  const [reconcileResult, setReconcileResult] = useState(null);
  const [qualityResult, setQualityResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleReconcile() {
    try {
      setLoading(true);
      setError("");
      const payload = JSON.parse(reconcileInput);
      const data = await reconcileMedication(payload);
      setReconcileResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleQuality() {
    try {
      setLoading(true);
      setError("");
      const payload = JSON.parse(qualityInput);
      const data = await validateDataQuality(payload);
      setQualityResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-5xl space-y-6">
          <h1 className="text-3xl font-bold">Clinical Dashboard</h1>
          <p className="text-slate-600">FastAPI + React + Tailwind</p>

          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
              {error}
            </div>
          )}

          <section className="rounded-2xl bg-white p-6 shadow">
            <h2 className="mb-3 text-xl font-semibold">Medication Reconciliation</h2>
            <textarea
              className="h-56 w-full rounded-xl border p-3 font-mono text-sm"
              value={reconcileInput}
              onChange={(e) => setReconcileInput(e.target.value)}
            />
            <div className="mt-3">
              <button
                onClick={handleReconcile}
                className="rounded-xl bg-slate-900 px-4 py-2 text-white"
              >
                {loading ? "Submitting..." : "Submit"}
              </button>
            </div>

            {reconcileResult && (
              <pre className="mt-4 overflow-auto rounded-xl bg-slate-100 p-4 text-sm">
                {JSON.stringify(reconcileResult, null, 2)}
              </pre>
            )}
          </section>

          <section className="rounded-2xl bg-white p-6 shadow">
            <h2 className="mb-3 text-xl font-semibold">Data Quality Validation</h2>
            <textarea
              className="h-56 w-full rounded-xl border p-3 font-mono text-sm"
              value={qualityInput}
              onChange={(e) => setQualityInput(e.target.value)}
            />
            <div className="mt-3">
              <button
                onClick={handleQuality}
                className="rounded-xl bg-slate-900 px-4 py-2 text-white"
              >
                {loading ? "Submitting..." : "Submit"}
              </button>
            </div>

            {qualityResult && (
              <pre className="mt-4 overflow-auto rounded-xl bg-slate-100 p-4 text-sm">
                {JSON.stringify(qualityResult, null, 2)}
              </pre>
            )}
          </section>
        </div>
    </div>
  );
}


