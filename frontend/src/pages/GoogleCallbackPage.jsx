import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function GoogleCallbackPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { setUser } = useAuth();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get("code");
      const hasProcessed = sessionStorage.getItem("googleCallbackProcessed");

      if (!code) {
        navigate("/login?error=no_code", { replace: true });
        return;
      }

      if (code && hasProcessed === code) {
        console.warn(
          "Callback already processed for this code, navigating to dashboard."
        );
        navigate("/dashboard", { replace: true });
        return;
      }

      try {
        const response = await api.get(
          `/api/auth/google/callback?code=${code}` // Ensure this has /api/
        );

        if (!response.data?.access_token || !response.data?.user) {
          throw new Error("Invalid response structure");
        }

        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        setUser(response.data.user);

        sessionStorage.setItem("googleCallbackProcessed", code);

        // Clear the code from the URL and navigate to dashboard
        window.history.replaceState(
          {},
          document.title,
          window.location.pathname
        );
        navigate("/dashboard", { replace: true });
      } catch (error) {
        console.error("Google auth failed:", error);
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        // Clear the code from the URL even on error
        window.history.replaceState(
          {},
          document.title,
          window.location.pathname
        );
        sessionStorage.removeItem("googleCallbackProcessed"); // Clear flag on error
        navigate("/login?error=auth_failed", { replace: true });
      }
    };

    handleCallback();
  }, [navigate, searchParams, setUser]);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-white">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mx-auto mb-4"></div>
        <p className="text-gray-700 text-lg">Processing Google login...</p>
      </div>
    </div>
  );
}
