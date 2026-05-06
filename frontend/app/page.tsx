export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-8">
      <div className="text-center">
        <h1 className="text-5xl font-bold tracking-tight text-white">
          Reproducibility Radar
        </h1>
        <p className="mt-3 text-lg text-gray-400">
          coming soon
        </p>
      </div>

      <div className="rounded-2xl border border-gray-800 bg-gray-900 px-8 py-6 text-center max-w-md">
        <p className="text-sm text-gray-500">
          Nightly ML paper reproducibility verification
        </p>
        <p className="mt-1 text-xs text-gray-600">
          Team AVANI · Samsung PRISM OpenClaw Hackathon
        </p>
      </div>
    </main>
  );
}
