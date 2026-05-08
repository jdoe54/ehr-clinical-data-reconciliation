export default function PatientCard({ patient, medications, conditions, isSelected, onSelect }) {
  const displayName = 
    patient.first_name && patient.last_name 
      ? `${patient.first_name} ${patient.last_name}`
      : patient.mrn || `Patient ${patient.id}`;  
  
  console.log("PatientCard medications: ", medications);
  return (
    <button
      onClick={onSelect}
      className={`w-full rounded-2xl border p-4 text-left shadow-sm transition ${
        isSelected
          ? "border-green-600 bg-green-50"
          : "border-slate-200 bg-white hover:border-green-400 hover:bg-slate-50"
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-800">{displayName}</h3>
          
          <p className="text-sm text-slate-500">
            Age {patient.age_years ?? "N/A"} • {patient.gender ?? "N/A Gender"}
          </p>
        </div>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
          ID {patient.id ?? "UNKNOWN"}
        </span>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium text-slate-700">Conditions</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {conditions.map((condition) => (
            <span
              key={condition.id}
              className="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-700"
            >
              {condition.condition_name}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium text-slate-700">Medications</p>
        <p className="mt-1 text-sm text-slate-600">
          {medications.map((medication_entry) => (
            <span
              key={medication_entry.id}
              className="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-700"
            >
              {medication_entry.medication}
            </span>
          ))}
        </p>
      </div>

      <p className="mt-3 text-xs text-slate-400">
        Last updated: {patient.last_updated ?? "N/A"}
      </p>
    </button>
  );
}