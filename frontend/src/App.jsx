import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import LabDashboard from "./pages/LabDashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import GenerateReport from "./pages/GenerateReport";
import ReportView from "./pages/ReportView";
import ReportHistory from "./pages/ReportHistory";
import Profile from "./pages/Profile";

import ForgotPassword from "./pages/ForgotPassword";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      <Route path="/dashboard" element={<LabDashboard />} />
      <Route path="/generate-report" element={<GenerateReport />} />
      <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
      <Route path="/reports" element={<ReportHistory />} />
      <Route path="/reports/:id" element={<ReportView />} />
      <Route path="/profile" element={<Profile />} />
      
    </Routes>
  );
}

export default App;