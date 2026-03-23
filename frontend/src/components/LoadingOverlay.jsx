export default function LoadingOverlay({ message = "Loading..." }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="flex w-full max-w-sm flex-col items-center rounded-2xl bg-white p-8 shadow-2xl">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-slate-300 border-t-slate-900" />
        <p className="mt-4 text-lg font-semibold text-slate-900">{message}</p>
        <p className="mt-2 text-sm text-slate-500 text-center">
          Running medication reconciliation and safety checks...
        </p>
      </div>
    </div>
  );
}