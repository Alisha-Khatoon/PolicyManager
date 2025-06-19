import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import UploadForm from "../components/UploadForm";

function Home() {
  const [policies, setPolicies] = useState([]);

  const fetchPolicies = () => {
    fetch("http://localhost:8000/api/policies")
      .then((res) => res.json())
      .then((data) => setPolicies(data))
      .catch((err) => console.error("Error fetching policies:", err));
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">📄 Uploaded Policies</h1>

      {/* Upload Form */}
      <UploadForm onUploadComplete={fetchPolicies} />

      {/* Uploaded Policies Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {policies.map((policy) => (
          <Link
            to={`/policy/${policy.id}`}
            key={policy.id}
            className="border p-4 rounded-lg shadow hover:bg-gray-100 transition"
          >
            <h2 className="text-lg font-semibold">{policy.filename}</h2>
            <p className="text-sm text-gray-600">
              Size: {(policy.size / 1024).toFixed(1)} KB
            </p>
            <p className="text-sm text-gray-500">
              Uploaded: {new Date(policy.uploaded_at).toLocaleString()}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;
