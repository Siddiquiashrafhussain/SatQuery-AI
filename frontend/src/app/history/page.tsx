import Link from "next/link";

export default function HistoryPage() {
	return (
		<main className="min-h-screen bg-[var(--background)] px-6 py-24 text-[var(--foreground)]">
			<section className="mx-auto max-w-3xl border border-[var(--border)] bg-[var(--surface)] p-8">
				<p className="eyebrow">ANALYSIS ARCHIVE</p>
				<h1 className="mt-4 text-4xl font-medium">Your analysis history</h1>
				<p className="mt-4 max-w-xl text-[var(--text-muted)]">
					Persistent session history is not enabled in this development build. Start a new analysis from the workstation to inspect its evidence and trace.
				</p>
				<Link className="mt-8 inline-flex bg-[var(--accent)] px-4 py-3 text-sm font-medium text-black" href="/workstation">
					Open workstation
				</Link>
			</section>
		</main>
	);
}
