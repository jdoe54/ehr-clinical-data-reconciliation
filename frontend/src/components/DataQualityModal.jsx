import ScoreBar from "./ScoreBar";

export default function DataQualityModal({ result, onClose }) {
    if (!result) return null;

    const { overall_score, breakdown, issues_detected } = result;

    return (

    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="max-h-[90vh] w-full max-w-5xl overflow-y-auto rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-6 flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Data Quality Results</h2>
            <p className="mt-1 text-sm text-slate-500">
              Review score breakdown and detected issues.
            </p>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300"
          >
            Close
          </button>
        </div>

        <div className="grid gap-8 lg:grid-cols-[2fr_1fr]">
          <div>
            <h3 className="mb-4 text-lg font-semibold text-slate-900">Score Breakdown</h3>

            <div className="flex flex-wrap items-end gap-6 rounded-2xl bg-slate-50 p-6">
              <ScoreBar label="Overall" score={overall_score} />
              <ScoreBar label="Completeness" score={breakdown.completeness} />
              <ScoreBar label="Accuracy" score={breakdown.accuracy} />
              <ScoreBar label="Timeliness" score={breakdown.timeliness} />
              <ScoreBar
                label="Clinical Plausibility"
                score={breakdown.clinical_plausibility}
              />
            </div>
          </div>

          <div>
            <h3 className="mb-4 text-lg font-semibold text-slate-900">Issues Detected</h3>

            <div className="rounded-2xl bg-slate-50 p-4">
              {issues_detected?.length ? (
                <ul className="space-y-3">
                  {issues_detected.map((issueItem, index) => (
                    <li
                      key={index}
                      className="rounded-xl border border-slate-200 bg-white p-4"
                    >
                      <div className="mb-2 flex items-center justify-between gap-3">
                        <span className="text-sm font-semibold text-slate-900">
                          {issueItem.field || "Unknown Field"}
                        </span>

                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${
                            issueItem.severity === "low"
                              ? "bg-yellow-100 text-yellow-800"
                              : issueItem.severity === "medium"
                              ? "bg-orange-100 text-orange-800"
                              : issueItem.severity === "high"
                              ? "bg-red-100 text-red-800"
                              : "bg-slate-100 text-slate-700"
                          }`}
                        >
                          {issueItem.severity ?? "N/A"}
                        </span>
                      </div>

                      <p className="text-sm text-slate-600">
                        {issueItem.issue ?? "N/A"}
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-slate-500">No issues detected.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}