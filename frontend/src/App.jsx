import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import PolicyPage from "./pages/PolicyPage";
import ComparePage from "./pages/ComparePage";
import GoogleCallbackPage from "./pages/GoogleCallbackPage";
import ProtectedRoute from "./components/auth/ProtectedRoute.jsx";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/auth/google/callback"
            element={<GoogleCallbackPage />}
          />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<DashboardPage />}>
              <Route path="policies" element={<div />} />
            </Route>
            <Route path="/policy/:id" element={<PolicyPage />} />
            <Route path="/compare/:id" element={<ComparePage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
