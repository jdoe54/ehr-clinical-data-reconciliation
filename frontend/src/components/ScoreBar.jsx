function getScoreColor(score) {
    if (score >= 70) return "bg-green-500";
    if (score >= 51) return "bg-yellow-400";
    return "bg-red-500";
}

export default function ScoreBar({ label, score }) {
  const colorClass = getScoreColor(score);

  return (
    <div className="flex flex-col items-center">
      <div className="mb-2 text-sm font-medium text-slate-700">
        {score}%
      </div>

      <div className="flex h-48 w-12 items-end rounded-xl bg-slate-200 p-1">
        <div
          className={`w-full rounded-lg ${colorClass}`}
          style={{ height: `${score}%` }}
        />
      </div>

      <div className="mt-3 text-center text-xs font-medium text-slate-600">
        {label}
      </div>
    </div>
  );
}

