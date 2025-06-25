// src/pages/LoginPage.jsx
import GoogleLoginButton from "../components/auth/GoogleLoginButton";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-10 rounded-lg shadow-md text-center w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">
          Welcome to Policy Manager
        </h1>
        <p className="mb-4 text-gray-600">
          Sign in with your Google account to continue.
        </p>
        <GoogleLoginButton />
      </div>
    </div>
  );
}
