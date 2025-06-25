import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export default function UploadPage() {
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [policies, setPolicies] = useState([]);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first");
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/api/policies/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(`Successfully uploaded: ${response.data.policy_id}`);
      fetchPolicies();
      setFile(null);
      document.getElementById("file-upload").value = "";
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          error.message ||
          "Upload failed. Please try again."
      );
    } finally {
      setUploading(false);
    }
  };

  const fetchPolicies = async () => {
    try {
      const response = await api.get("/api/policies/enterprise/policies");
      setPolicies(response.data);
    } catch (error) {
      console.error("Failed to fetch policies:", error);
      setMessage("Failed to load your policies");
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  return (
    <div className="min-h-screen p-4 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">
            Welcome, {user?.email || "User"}
          </h1>

          <form onSubmit={handleUpload} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Policy Document
              </label>
              <input
                id="file-upload"
                type="file"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
                accept=".pdf,.docx,.txt"
              />
            </div>

            <button
              type="submit"
              disabled={!file || uploading}
              className={`px-4 py-2 rounded-md text-white font-medium
                ${
                  !file || uploading
                    ? "bg-gray-400"
                    : "bg-blue-600 hover:bg-blue-700"
                }
                transition duration-200`}
            >
              {uploading ? "Uploading..." : "Upload Policy"}
            </button>

            {message && (
              <p
                className={`text-sm ${
                  message.includes("Success")
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                {message}
              </p>
            )}
          </form>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Your Policy Documents
          </h2>

          {policies.length > 0 ? (
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
                      Industry
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {policies.map((policy) => (
                    <tr key={policy.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {policy.filename}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {policy.category || "-"}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {policy.industry || "-"}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => navigate(`/policy/${policy.id}`)}
                          className="text-blue-600 hover:text-blue-900 mr-4"
                        >
                          View
                        </button>
                        <button
                          onClick={() => navigate(`/compare/${policy.id}`)}
                          className="text-green-600 hover:text-green-900"
                        >
                          Compare
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No policies uploaded yet.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
