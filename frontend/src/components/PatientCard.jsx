export default function PatientCard({ patient, isSelected, onSelect }) {
    return (
    <button
      onClick={() => onSelect(patient)}
      className={`w-full rounded-2xl border p-4 text-left shadow-sm transition ${
        isSelected
          ? "border-green-600 bg-green-50"
          : "border-slate-200 bg-white hover:border-green-400 hover:bg-slate-50"
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-800">{patient.name}</h3>
          <p className="text-sm text-slate-500">
            Age {patient.reconcilePayload['patient_context'].age} • {patient.reconcilePayload['patient_context'].gender}
          </p>
        </div>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
          ID {patient.id}
        </span>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium text-slate-700">Conditions</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {patient.reconcilePayload['patient_context'].conditions.map((condition) => (
            <span
              key={condition}
              className="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-700"
            >
              {condition}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium text-slate-700">Medications</p>
        <p className="mt-1 text-sm text-slate-600">
          {patient.dataQualityPayload.medications.join(", ")}
        </p>
      </div>

      <p className="mt-3 text-xs text-slate-400">
        Last updated: {patient.dataQualityPayload['last_updated']}
      </p>
    </button>
  );
}