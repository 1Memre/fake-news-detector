'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body className="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">
        <div className="bg-gray-800 p-8 rounded-xl border border-red-500/30 max-w-lg w-full text-center">
          <h2 className="text-2xl font-bold text-red-500 mb-4">Something went wrong!</h2>
          <p className="text-gray-300 mb-6 font-mono text-sm bg-black/30 p-4 rounded text-left overflow-auto max-h-40">
            {error.message}
          </p>
          <button
            onClick={() => reset()}
            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
