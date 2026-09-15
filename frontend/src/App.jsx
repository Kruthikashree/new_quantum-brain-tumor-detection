import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import LabDashboard from "./pages/LabDashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import Upload from "./pages/Upload";
import Prediction from "./pages/Prediction";
import History from "./pages/History";
import Doctors from "./pages/Doctors";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/dashboard" element={<LabDashboard />} />
      <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
      <Route path="/upload" element={<Upload />} />
      <Route path="/prediction" element={<Prediction />} />
      <Route path="/history" element={<History />} />
      <Route path="/doctors" element={<Doctors />} />
    </Routes>
  );
}

export default App;
