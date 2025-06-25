import React from "react";
import { useNavigate } from "react-router-dom";
import GoogleLoginButton from "../components/auth/GoogleLoginButton";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md text-center">
        <h1 className="text-3xl font-bold text-primary mb-6">
          Enterprise Policy Manager
        </h1>
        <p className="text-gray-600 mb-6">
          Streamline policy management with advanced analytics.
        </p>
        <GoogleLoginButton />
      </div>
    </div>
  );
}
