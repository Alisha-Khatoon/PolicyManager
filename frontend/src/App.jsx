import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PolicyPage from "./pages/PolicyPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/policy/:id" element={<PolicyPage />} />
    </Routes>
  );
}

export default App;
