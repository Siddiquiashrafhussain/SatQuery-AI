"use client";

import { useState } from "react";
import type { GeoNLIResult } from "@/types/domain";
import { api } from "@/lib/api";
import { normalizeAnalysisError } from "@/lib/errors";

export function GeoNLIChatConversation() {
  const [premise, setPremise] = useState("");
  const [hypothesis, setHypothesis] = useState("");
  const [imageId, setImageId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GeoNLIResult | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmedPremise = premise.trim();
    const trimmedHypothesis = hypothesis.trim();
    if (!trimmedPremise || !trimmedHypothesis) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await api.submitGeoNLI({
        premise: trimmedPremise,
        hypothesis: trimmedHypothesis,
        image_id: imageId.trim() || null,
      });
      setResult(res);
    } catch (err) {
      setError(normalizeAnalysisError(err));
    } finally {
      setLoading(false);
    }
  }

  function getBadgeClass(entailment: string) {
    switch (entailment) {
      case "entailment":
        return "badge--success";
      case "contradiction":
        return "badge--danger";
      case "neutral":
      default:
        return "badge--warning";
    }
  }

  return (
    <div className="geonli-container p-4 border rounded shadow-sm bg-white" data-testid="geonli-chat-conversation">
      <h3 className="text-lg font-semibold mb-4">GeoNLI AI Chat</h3>
      <p className="text-sm text-gray-600 mb-4">
        Evaluate a hypothesis against a geospatial premise (and optional image).
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Premise</label>
          <textarea
            className="w-full border rounded p-2 text-sm"
            rows={3}
            value={premise}
            onChange={(e) => setPremise(e.target.value)}
            placeholder="Describe the known context..."
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Hypothesis</label>
          <textarea
            className="w-full border rounded p-2 text-sm"
            rows={2}
            value={hypothesis}
            onChange={(e) => setHypothesis(e.target.value)}
            placeholder="State the hypothesis to evaluate..."
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Image ID (Optional)</label>
          <input
            type="text"
            className="w-full border rounded p-2 text-sm"
            value={imageId}
            onChange={(e) => setImageId(e.target.value)}
            placeholder="Optional reference image ID"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !premise.trim() || !hypothesis.trim()}
          className="mt-2 bg-blue-600 text-white rounded p-2 font-medium disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Evaluate NLI"}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-700 rounded border border-red-200 text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 border-t pt-4">
          <h4 className="font-medium mb-2">Analysis Result</h4>
          <div className="flex items-center gap-2 mb-3">
            <span className="text-sm font-semibold">Classification:</span>
            <span
              className={`px-2 py-1 text-xs uppercase font-bold rounded ${getBadgeClass(
                result.entailment_class
              )}`}
            >
              {result.entailment_class}
            </span>
          </div>
          <div className="text-sm text-gray-800 bg-gray-50 p-3 rounded">
            <strong>Reasoning: </strong>
            {result.reasoning}
          </div>
          <dl className="mt-4 text-xs text-gray-500 flex flex-col gap-1">
            <div className="flex">
              <dt className="w-24 font-medium">Provider:</dt>
              <dd>{result.provider}</dd>
            </div>
            <div className="flex">
              <dt className="w-24 font-medium">Model:</dt>
              <dd>{result.model_name}</dd>
            </div>
          </dl>
        </div>
      )}
    </div>
  );
}
