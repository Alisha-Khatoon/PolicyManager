import React from "react";

export default function PolicyDetailsModal({ policy, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-auto">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-xl font-bold">{policy.filename}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="font-semibold">Uploaded</h3>
            <p>{new Date(policy.uploaded_at).toLocaleString()}</p>
          </div>

          {policy.category && (
            <div>
              <h3 className="font-semibold">Category</h3>
              <p>{policy.category}</p>
            </div>
          )}

          {policy.industry && (
            <div>
              <h3 className="font-semibold">Industry</h3>
              <p>{policy.industry}</p>
            </div>
          )}

          {policy.ai_review && (
            <div>
              <h3 className="font-semibold">AI Review</h3>
              <p className="whitespace-pre-wrap">{policy.ai_review}</p>
            </div>
          )}

          {policy.insights && (
            <div>
              <h3 className="font-semibold">Key Insights</h3>
              <ul className="list-disc pl-5">
                {Object.entries(policy.insights).map(([key, value]) => (
                  <li key={key}>
                    <strong>{key}:</strong> {value}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
