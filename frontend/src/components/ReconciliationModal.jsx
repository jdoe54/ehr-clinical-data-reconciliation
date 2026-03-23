import { useState } from "react";

function getConfidenceColor(score) {
  const percent = score * 100;
  if (percent >= 70) return "bg-green-500";
  if (percent >= 51) return "bg-yellow-400";
  return "bg-red-500";
}

function getSafetyBadgeColor(status) {
  if (status === "PASSED") return "bg-green-100 text-green-800";
  if (status === "WARNING") return "bg-yellow-100 text-yellow-800";
  if (status === "FAILED") return "bg-red-100 text-red-800";
  return "bg-slate-100 text-slate-700";
}

export default function ReconciliationModal({ result, onClose }) {
  const [decision, setDecision] = useState(null);

  if (!result) return null;

  const confidencePercent = Math.round((result.confidence_score ?? 0) * 100);
  const confidenceColor = getConfidenceColor(result.confidence_score ?? 0);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
      onClick={onClose}
    >
      <div
        className="max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-2xl bg-white p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-6 flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">
              Reconciliation Result
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Review the AI recommendation, confidence, and safety guidance.
            </p>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300"
          >
            Close
          </button>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <div className="space-y-6">
            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">
                Reconciled Medication
              </p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">
                {result.reconciliated_medication ?? "N/A"}
              </p>
            </div>

            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">Reasoning</p>
              <p className="mt-2 leading-7 text-slate-700">
                {result.reasoning ?? "N/A"}
              </p>
            </div>

            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">
                Recommended Actions
              </p>

              {result.recommended_actions?.length ? (
                <ul className="mt-3 space-y-3">
                  {result.recommended_actions.map((action, index) => (
                    <li
                      key={index}
                      className="rounded-xl border border-slate-200 bg-white p-4 text-slate-700"
                    >
                      {action}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-2 text-slate-700">N/A</p>
              )}
            </div>
          </div>

          <div className="space-y-6">
            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">Confidence</p>

              <div className="mt-4">
                <div className="mb-2 flex items-center justify-between text-sm font-medium text-slate-700">
                  <span>AI Confidence</span>
                  <span>{confidencePercent}%</span>
                </div>

                <div className="h-4 w-full rounded-full bg-slate-200">
                  <div
                    className={`h-4 rounded-full ${confidenceColor}`}
                    style={{ width: `${confidencePercent}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">
                Clinical Safety Check
              </p>

              <span
                className={`mt-3 inline-block rounded-full px-3 py-1 text-sm font-medium ${getSafetyBadgeColor(
                  result.clinical_safety_check
                )}`}
              >
                {result.clinical_safety_check ?? "N/A"}
              </span>
            </div>

            <div className="rounded-2xl bg-slate-50 p-5">
              <p className="text-sm font-medium text-slate-500">
                Clinician Decision
              </p>

              <div className="mt-4 flex gap-3">
                <button
                  onClick={() => setDecision("approved")}
                  className="rounded-xl bg-green-600 px-4 py-3 font-medium text-white hover:bg-green-700"
                >
                  Approve
                </button>

                <button
                  onClick={() => setDecision("rejected")}
                  className="rounded-xl bg-red-600 px-4 py-3 font-medium text-white hover:bg-red-700"
                >
                  Reject
                </button>
              </div>

              <div className="mt-4">
                {decision === "approved" && (
                  <p className="rounded-xl bg-green-50 p-3 text-sm font-medium text-green-800">
                    Suggestion approved by clinician.
                  </p>
                )}

                {decision === "rejected" && (
                  <p className="rounded-xl bg-red-50 p-3 text-sm font-medium text-red-800">
                    Suggestion rejected. Manual review recommended.
                  </p>
                )}

                {!decision && (
                  <p className="text-sm text-slate-500">
                    No decision recorded yet.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
