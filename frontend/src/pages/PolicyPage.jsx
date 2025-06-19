import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

function PolicyPage() {
  const { id } = useParams();
  const [policy, setPolicy] = useState(null);
  const [tab, setTab] = useState("content");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPolicy = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/policies/${id}`
        );
        const data = await response.json();
        setPolicy(data);
      } catch (err) {
        console.error("Error fetching policy:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchPolicy();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!policy) {
    return (
      <div className="p-6 text-center text-red-500">
        Failed to load policy. Please try again.
      </div>
    );
  }

  const downloadText = () => {
    const blob = new Blob([policy.content], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${policy.filename.replace(/\.[^/.]+$/, "")}.txt`;
    a.click();
  };

  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(policy.analysis, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${policy.filename.replace(/\.[^/.]+$/, "")}_analysis.json`;
    a.click();
  };

  // Format AI review text into sections with headings if present
  const formatAIReview = (text) => {
    if (!text) return null;

    // Replace **bold** with <strong>bold</strong>
    let formatted = text.replace(/\*\*(.*?)\*\*/g, (_, p1) => `<strong>${p1}</strong>`);
    // Replace *italic* with <em>italic</em>
    formatted = formatted.replace(/\*(.*?)\*/g, (_, p1) => `<em>${p1}</em>`);
    // Remove any remaining single asterisks that are not part of formatting
    formatted = formatted.replace(/(^|\s)\*+(\s|$)/g, " ");

    // Split into sections by headings (lines starting with - or * or <strong>)
    const sectionRegex = /(?:^|\n)([-*]\s*<strong>.*?<\/strong>.*?)(?=\n[-*]\s*<strong>|$)/gs;
    const matches = [...formatted.matchAll(sectionRegex)];

    if (matches.length > 0) {
      return matches.map((match, idx) => {
        // Extract heading and content
        const headingMatch = match[1].match(/<strong>(.*?)<\/strong>/);
        const heading = headingMatch ? headingMatch[1] : null;
        // Remove heading from content
        const rest = match[1].replace(/.*?<strong>.*?<\/strong>:?/, "").trim();

        // Split rest into sentences by full stop, keeping the full stop
        const sentences = rest.split(/(?<=\.)\s+/).filter(Boolean);

        return (
          <div key={idx} className="mb-4">
            {heading && (
              <h3 className="text-blue-700 font-bold mb-1">{heading}</h3>
            )}
            {sentences.map((sentence, i) => (
              <p
                key={i}
                className="text-sm leading-relaxed"
                dangerouslySetInnerHTML={{ __html: sentence.trim() }}
              />
            ))}
          </div>
        );
      });
    } else {
      // No headings, just split by full stop and bold any **text**
      return formatted
        .split(/(?<=\.)\s+/)
        .filter(Boolean)
        .map((sentence, idx) => (
          <p
            key={idx}
            className="text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: sentence.trim() }}
          />
        ));
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {/* Header */}
        <div className="bg-blue-600 px-6 py-4">
          <h1 className="text-xl font-bold text-white">{policy.filename}</h1>
          <p className="text-blue-100 text-sm">
            Uploaded: {new Date(policy.uploaded_at).toLocaleString()}
          </p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {["content", "analysis", "ai_review"].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  tab === t
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                {t === "content"
                  ? "📄 Content"
                  : t === "analysis"
                  ? "📊 Rule Analysis"
                  : "🤖 AI Review"}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {tab === "content" && (
            <div className="prose max-w-none">
              {policy.content
                .split(/(?<=\.|\n)\s{2,}|(?<=\.)(?=\s{1}[A-Z])/g)
                .map((para, idx) => (
                  <p
                    key={idx}
                    className="mb-4 pl-4 border-l-4 border-blue-200 bg-blue-50 p-2 rounded"
                  >
                    {para.trim()}
                  </p>
                ))}
            </div>
          )}

          {tab === "analysis" && (
            <div className="space-y-4">
              {Object.entries(policy.analysis).map(([key, value]) => (
                <div
                  key={key}
                  className="p-3 bg-gray-50 rounded border border-gray-200"
                >
                  <h3 className="font-semibold text-blue-700">{key}</h3>
                  <p className="mt-1 text-gray-800">{value}</p>
                </div>
              ))}
            </div>
          )}

          {tab === "ai_review" && (
            <div className="prose max-w-none">
              {policy.ai_review && policy.ai_review.trim() !== "" ? (
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  {formatAIReview(policy.ai_review)}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-2">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-12 w-12 mx-auto"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                  <p className="text-gray-500">
                    No AI review available for this policy.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Download Buttons */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end space-x-4">
          <button
            onClick={downloadText}
            className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
          >
            ⬇️ Download Text
          </button>
          <button
            onClick={downloadJson}
            className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
          >
            ⬇️ Download Analysis
          </button>
        </div>
      </div>
    </div>
  );
}

export default PolicyPage;
