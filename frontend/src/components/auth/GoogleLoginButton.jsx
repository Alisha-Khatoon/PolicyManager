import { googleLogin } from "../../services/api";

export default function GoogleLoginButton() {
  const handleGoogleLogin = async () => {
    try {
      const response = await googleLogin();
      const { url } = response.data;
      console.log("OAuth URL:", url); // Debug
      if (url) {
        window.location.href = url;
      } else {
        throw new Error("No OAuth URL received");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Failed to initiate Google login. Please check console.");
    }
  };

  return (
    <button
      onClick={handleGoogleLogin}
      className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300"
    >
      Sign in with Google
    </button>
  );
}
