import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function ComparePage() {
  const { id } = useParams();
  const [policy, setPolicy] = useState(null);
  const [govPolicyText, setGovPolicyText] = useState("");
  const [comparison, setComparison] = useState(null);
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

  const handleCompare = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(`/api/policies/compare`, {
        policy_id: id,
        gov_policy_text: govPolicyText,
      });
      setComparison(response.data.comparison);
    } catch (error) {
      console.error("Error comparing policies:", error);
    }
  };

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
          Compare Policy: {policy.filename}
        </h1>
        <form onSubmit={handleCompare} className="space-y-4">
          <textarea
            value={govPolicyText}
            onChange={(e) => setGovPolicyText(e.target.value)}
            placeholder="Enter government policy text here..."
            className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary h-40"
          />
          <button
            type="submit"
            className="w-full bg-accent text-white py-2 px-4 rounded-lg hover:bg-yellow-600 transition duration-300"
          >
            Compare
          </button>
        </form>
        {comparison && (
          <div className="mt-6 space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">
              Comparison Results
            </h2>
            <div>
              <h3 className="text-lg font-semibold text-gray-700">
                Rule-Based Analysis
              </h3>
              <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
                {JSON.stringify(comparison.rule_based, null, 2)}
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700">
                AI Analysis
              </h3>
              <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
                {comparison.ai_analysis}
              </pre>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700">
                Compliance Score
              </h3>
              <p className="bg-gray-50 p-4 rounded-lg">
                {comparison.compliance_score}%
              </p>
            </div>
          </div>
        )}
        <button
          onClick={() => navigate(`/policy/${id}`)}
          className="mt-4 bg-secondary text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition duration-300"
        >
          Back to Policy
        </button>
      </div>
    </div>
  );
}
