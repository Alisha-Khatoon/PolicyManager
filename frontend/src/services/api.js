import axios from "axios";

// 1. Configuration: baseURL MUST be just the host and port, WITHOUT "/api"
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000", 
  withCredentials: true,
  timeout: 30000,
});

// 2. Request Interceptor - Enhanced but compatible
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      if (process.env.NODE_ENV === "development") {
        console.debug("Adding auth token to request:", config.url);
      }
    }
    return config;
  },
  (error) => {
    if (process.env.NODE_ENV !== "test") {
      console.error("Request error:", error);
    }
    return Promise.reject(error);
  }
);

// 3. Response Interceptor - More robust error handling
api.interceptors.response.use(
  (response) => {
    if (process.env.NODE_ENV === "development") {
      console.debug("API response:", response.config.url, response.data);
    }
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    if (process.env.NODE_ENV !== "test") {
      const errorMessage = error.response?.data?.message || error.message;
      console.error(`API Error [${error.response?.status}]:`, errorMessage);
    }
    return Promise.reject(error);
  }
);

// 4. API Endpoints: Each path MUST now include the "/api" prefix.
export const googleLogin = () => api.get("/api/auth/google/login"); // ADDED /api/
export const verifyToken = () => api.get("/api/auth/verify"); // ADDED /api/
export const handleGoogleCallback = (code) =>
  api.get(`/api/auth/google/callback?code=${code}`); // ADDED /api/
export const fetchPolicies = () => api.get("/api/policies/enterprise/policies"); // ADDED /api/
export const uploadPolicy = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/api/policies/upload", formData, {
    // ADDED /api/
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
export const uploadPolicies = (formData) =>
  api.post("/api/policies/upload-multiple", formData); // ADDED /api/
export const fetchPolicyById = (policyId) =>
  api.get(`/api/policies/policy/${policyId}`); // ADDED /api/
export const comparePolicies = (policyId, govPolicyText) =>
  api.post(`/api/policies/compare?policy_id=${policyId}`, {
    gov_policy_text: govPolicyText,
  }); // ADDED /api/

export default api;
