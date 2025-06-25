import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import PolicyDetailsModal from "./PolicyDetailsModal";

export default function PolicyList() {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPolicy, setSelectedPolicy] = useState(null);

  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        // CHANGED: Removed redundant /api from the path
        const response = await api.get("/policies/enterprise/policies");
        setPolicies(response.data);
      } catch (error) {
        console.error("Failed to fetch policies:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPolicies();
  }, []);

  if (loading) return <div>Loading policies...</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-medium mb-4">Your Policies</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Filename
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {policies.map((policy) => (
              <tr key={policy.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={() => setSelectedPolicy(policy)}
                    className="text-blue-600 hover:underline"
                  >
                    {policy.filename}
                  </button>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {policy.category || "-"}
                </td>
                <td className="px-6 py-4 whitespace-nowrap space-x-2">
                  <Link
                    to={`/policy/${policy.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    View
                  </Link>
                  <Link
                    to={`/compare/${policy.id}`}
                    className="text-green-600 hover:underline"
                  >
                    Compare
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedPolicy && (
        <PolicyDetailsModal
          policy={selectedPolicy}
          onClose={() => setSelectedPolicy(null)}
        />
      )}
    </div>
  );
}
