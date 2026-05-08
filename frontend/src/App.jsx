import { useEffect, useState } from 'react'
import { reconcileMedication, validateDataQuality, fetchPatients, fetchConditions, fetchMedications } from './services/api'

import PatientCard from "./components/PatientCard";
import DataQualityModal from "./components/DataQualityModal";
import ReconciliationModal from './components/ReconciliationModal';
import LoadingOverlay from './components/LoadingOverlay';

export default function App() {

  const [error, setError] = useState("");
  //const [loading, setLoading] = useState(false);
  
  const [qualityResult, setQualityResult] = useState(null);
  const [showQualityModal, setShowQualityModal] = useState(false);

  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);

  const [reconcileResult, setReconcileResult] = useState(null);
  const [showReconcileModal, setShowReconcileModal] = useState(null);
  const [reconcileLoading, setReconcileLoading] = useState(false);

  const [selectedMedications, setSelectedMedications] = useState([]);
  const [selectedConditions, setSelectedConditions] = useState([]);
  const [patientDetailsLoading, setPatientDetailsLoading] = useState(false); 

  useEffect(() => {
    async function loadPatients() {
      const data = await fetchPatients();

      console.log(data)
      setPatients(data);

      
    }

    loadPatients();
  }, []);


  async function handleSelectPatient(patient) {
    try {
      setError("");
      setSelectedPatient(patient);
      setPatientDetailsLoading(true);

      const [medications, conditions] = await Promise.all([
        fetchMedications(patient.id),
        fetchConditions(patient.id),
      ]);

      setSelectedMedications(medications);
      setSelectedConditions(conditions);

    } catch (err) {
      console.error("handleSelectPatient error:", err);
      setError(err.message || "Failed to load patient details.");
      setSelectedMedications([]);
      setSelectedConditions([]);
    } finally {
      setPatientDetailsLoading(false);
    }
  }

  async function handleReconcile() {
    try {
      setError("");
      setReconcileLoading(true);

      const data = await reconcileMedication({
        patient_id: selectedPatient.id,
      });


      setReconcileResult(data);
      setShowReconcileModal(true);
    } catch (err) {
      setError(err.message);
      console.error("handleReconcile error: ", err);
    } finally {
      setReconcileLoading(false);
    }
  }

  async function handleQuality() {
    try {
      setError("");

     
      const data = await validateDataQuality({
        patient_id: selectedPatient.id,
      });

      setQualityResult(data);
      setShowQualityModal(true);
    } catch (err) {
      console.error("Handle quality error: ", err)
      setError(err.message);
    }
  }

  

  
  return (
    <div className="flex min-h-screen w-full bg-gray-100">
      <aside className="w-48 bg-green-700 text-white p-6">
        <h1 className="mb-8 text-2xl font-bold">EHR Reconciliation Demo</h1>

        <nav className="space-y-2">
          
        </nav>
      </aside>

      

      <main className="flex-1 p-8 ">
        <h2 className="mb-6 text-3xl font-bold text-slate-800">Patients</h2>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="space-y-4 lg:col-span-1">
            {patients.map((patient) => (
              <PatientCard
                key={patient.id}
                patient={patient}
                isSelected={selectedPatient?.id === patient.id}
                onSelect={() => handleSelectPatient(patient)}
                conditions = {
                  selectedPatient?.id === patient.id ? selectedConditions : []
                }
                medications = {
                  selectedPatient?.id === patient.id ? selectedMedications : []
                }
                /*;*/
              />
            ))}
          </div>
            
          <div className="rounded-2xl bg-white p-6 shadow lg:col-span-2">
            <h3 className="text-2xl font-semibold text-slate-800">
              { (selectedPatient?.first_name ?? "Patient") + " " + (selectedPatient?.last_name ?? selectedPatient?.id)} 
            </h3>
            

            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Age</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  
                  {selectedPatient?.age_years ?? "N/A"}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">DOB</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient?.date_of_birth ?? "N/A"}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Gender</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient?.gender ?? "N/A"}
                </p>
              </div>

              <div className="rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">Last Updated</p>
                <p className="mt-1 text-lg font-semibold text-slate-800">
                  {selectedPatient?.last_updated ?? "N/A"}
                </p>
              </div>
            </div>

            <div className="mt-6">
              <p className="text-sm font-medium text-slate-700">Conditions</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedConditions.map((condition) => (
                  <span
                    key={condition}
                    className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-700"
                  >
                    {condition.condition_name}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-6">
              <p className="text-sm font-medium text-slate-700">Medications</p>
              <ul className="mt-2 list-inside list-disc text-slate-600">
                {selectedMedications.map((med) => (
                  <li key={med}>{med.medication}</li>
                ))}
              </ul>
            </div>

            <div className="mt-6 flex flex-row items-center gap-4">
               {selectedPatient?.can_reconcile && (
                <button
                  onClick={handleReconcile}
                  className="rounded-xl bg-slate-900 px-5 py-3 font-medium text-white shadow hover:bg-slate-600"
                >
                  Run Reconciliation
                </button>
              )}

              <button onClick={handleQuality} 
              className="rounded-xl bg-slate-900 px-5 py-3 font-medium text-white shadow hover:bg-slate-600">
                Run Data Quality
              </button>
            </div>
            
          </div>
        </div>
      </main>

      {showQualityModal && (
        <DataQualityModal 
          result={qualityResult} 
          onClose={() => setShowQualityModal(false)}
        />
      )}

      {reconcileLoading && (
        <LoadingOverlay message="Running reconciliation..." />
      )}

      {showReconcileModal && (
        <ReconciliationModal
          result={reconcileResult}
          onClose={() => setShowReconcileModal(false)}
        />
      )}

    </div>
  );
}


