import React, { useState, useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom"; // Import useLocation
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import PolicyList from "../components/PolicyList";
import UploadForm from "../components/UploadForm";

export default function DashboardPage() {
  const location = useLocation(); // Get current location
  const [showUploadForm, setShowUploadForm] = useState(false);

  useEffect(() => {
    // Check for 'action=upload' query parameter
    const params = new URLSearchParams(location.search);
    if (params.get("action") === "upload") {
      setShowUploadForm(true);
    } else {
      setShowUploadForm(false); // Reset if not explicitly for upload
    }
  }, [location.search]); // Re-run when location search params change

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex">
        {/* Sidebar will still allow direct access to upload/policies */}
        <Sidebar onUploadClick={() => setShowUploadForm(true)} />
        {/* Added px-8 py-6 for better spacing around main content */}
        <main className="flex-1 p-6 sm:px-8 sm:py-6">
          {showUploadForm ? (
            <UploadForm onUploadComplete={() => setShowUploadForm(false)} />
          ) : (
            <PolicyList />
          )}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
