import { googleLogin } from "../api";

function Login() {
  const handleGoogleLogin = async () => {
    try {
      const { data } = await googleLogin();
      window.location.href = data.url; // Redirect to Google
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return <button onClick={handleGoogleLogin}>Login with Google</button>;
}
