import { useState } from 'react'
import { reconcileMedication, validateDataQuality } from './services/api'
import { patients_data } from "./sample_data/patient";
import PatientCard from "./components/PatientCard";

import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
//import './App.css'

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
  const [selectedPatient, setSelectedPatient] = useState(patients_data[0]);

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
    <div className="flex min-h-screen w-full bg-gray-100">
      <aside className="w-48 bg-green-700 text-white p-6">
        <h1 className="mb-8 text-2xl font-bold">EHR Reconciliation Demo</h1>

        <nav className="space-y-2">
          
        </nav>
      </aside>

      

      <main className="flex-1 p-8">
        <h2 className="mb-6 text-3xl font-bold text-slate-800">Patients</h2>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="space-y-4 lg:col-span-1">
            {patients_data.map((patient) => (
              <PatientCard
                key={patient.id}
                patient={patient}
                isSelected={selectedPatient.id === patient.id}
                onSelect={setSelectedPatient}
              />
            ))}
          </div>

          <div className="rounded-2xl bg-white p-6 shadow lg:col-span-2">
            <h3 className="text-2xl font-semibold text-slate-800">
              {selectedPatient.name}
            </h3>

            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Age</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient.reconcilePayload['patient_context'].age}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">DOB</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient.dataQualityPayload.demographics.dob}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Gender</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient.dataQualityPayload.demographics.gender}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Last Updated</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient.dataQualityPayload['last_updated']}
                </p>
              </div>
            </div>

            <div className="mt-6">
              <p className="text-sm font-medium text-slate-700">Conditions</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedPatient.reconcilePayload['patient_context'].conditions.map((condition) => (
                  <span
                    key={condition}
                    className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-700"
                  >
                    {condition}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-6">
              <p className="text-sm font-medium text-slate-700">Medications</p>
              <ul className="mt-2 list-inside list-disc text-slate-600">
                {selectedPatient.dataQualityPayload.medications.map((med) => (
                  <li key={med}>{med}</li>
                ))}
              </ul>
            </div>

            <button onClick={handleReconcile} className="mt-6 rounded-xl bg-slate-900 px-5 py-3 font-medium text-white shadow hover:bg-slate-600">
              Run Reconciliation
            </button>

            <button onClick={handleQuality} className="mt-6 rounded-xl bg-slate-900 px-5 py-3 font-medium text-white shadow hover:bg-slate-600">
              Run Data Quality
            </button>
          </div>
        </div>
      </main>

      
    </div>
  );
}


/*

<div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-5xl space-y-6">
        

          <h1 className="text-3xl font-bold">Clinical Dashboard</h1>


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

    
*/
