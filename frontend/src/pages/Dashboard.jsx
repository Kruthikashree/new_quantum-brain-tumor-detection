import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser, logout } from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const currentUser = getCurrentUser();

    if (!currentUser) {
      navigate("/login");
      return;
    }

    setUser(currentUser);
  }, [navigate]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) return null;

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h1>Welcome, {user.name}</h1>
          <p>Laboratory Portal — Upload scans and generate reports for physician review</p>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Log Out
        </button>
      </div>

      <div className="dashboard-cards">
        <div
          className="dashboard-card primary"
          onClick={() => navigate("/upload")}
        >
          <h2>Upload Scan Result</h2>
          <p>Upload a patient's MRI scan to generate an AI-classification report for the treating physician.</p>
          <span className="card-cta">Start Analysis →</span>
        </div>

        <div className="dashboard-card" onClick={() => navigate("/history")}>
          <h2>Report History</h2>
          <p>View previously generated scan reports for this lab.</p>
          <span className="card-cta">View History →</span>
        </div>

        <div className="dashboard-card" onClick={() => navigate("/doctors")}>
          <h2>Physician Directory</h2>
          <p>Find and route reports to the physician responsible for the patient's care.</p>
          <span className="card-cta">Search Physicians →</span>
        </div>
      </div>

      <div className="dashboard-disclaimer">
        <strong>Note:</strong> This tool generates an AI-assisted
        classification report for laboratory use. The report is provided to
        the treating physician, who is responsible for confirming the
        diagnosis and deciding on treatment.
      </div>
    </div>
  );
}

export default Dashboard;
