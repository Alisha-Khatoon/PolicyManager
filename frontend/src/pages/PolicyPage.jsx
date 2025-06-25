import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function PolicyPage() {
  const { id } = useParams();
  const [policy, setPolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPolicy() {
      try {
        const response = await api.get(`/api/policies/policy/${id}`);
        setPolicy(response.data);
      } catch (error) {
        console.error("Error fetching policy:", error);
        navigate("/upload");
      } finally {
        setLoading(false);
      }
    }
    fetchPolicy();
  }, [id, navigate]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );

  if (!policy)
    return <div className="text-center text-red-500">Policy not found.</div>;

  return (
    <div className="min-h-screen p-4 bg-gradient-to-br from-gray-50 to-gray-200">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-xl">
        <h1 className="text-3xl font-bold text-primary mb-4">
          {policy.filename}
        </h1>
        <p className="text-gray-600 mb-4">
          Category: {policy.category} | Industry: {policy.industry}
        </p>
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              AI Review
            </h2>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
              {JSON.stringify(policy.ai_review, null, 2)}
            </pre>
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              Insights
            </h2>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
              {JSON.stringify(policy.insights, null, 2)}
            </pre>
          </div>
          <button
            onClick={() => navigate("/upload")}
            className="mt-4 bg-secondary text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition duration-300"
          >
            Back to Upload
          </button>
          <button
            onClick={() => navigate(`/compare/${policy.id}`)}
            className="mt-4 ml-2 bg-accent text-white py-2 px-4 rounded-lg hover:bg-yellow-600 transition duration-300"
          >
            Compare with Government Policy
          </button>
        </div>
      </div>
    </div>
  );
}
