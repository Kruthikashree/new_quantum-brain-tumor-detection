import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser, logout, getPatientByCode, generateResult } from "../services/api";
import "./DoctorDashboard.css";

const TUMOR_COLORS = {
  Glioma: "#dc2626",
  Meningioma: "#d97706",
  "No Tumor": "#16a34a",
  Pituitary: "#7c3aed"
};

function DoctorDashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const [code, setCode] = useState("");
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

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

  const handleLookup = async (e) => {
    e.preventDefault();
    setError("");
    setPatient(null);
    setLoading(true);

    try {
      const data = await getPatientByCode(code.trim());
      setPatient(data);
    } catch (err) {
      const message =
        err.response?.data?.error || "No patient found for this code.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateResult = async () => {
    setAnalyzing(true);
    setError("");

    try {
      const data = await generateResult(patient.access_code);
      setPatient({ ...patient, status: "analyzed", result: data.result });
    } catch (err) {
      const message =
        err.response?.data?.error || "Failed to generate result.";
      setError(message);
    } finally {
      setAnalyzing(false);
    }
  };

  if (!user) return null;

  return (
    <div className="doctor-page">
      <div className="doctor-header">
        <div>
          <h1>Welcome, {user.name}</h1>
          <p>Enter a patient's access code to view their scan and generate a report</p>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Log Out
        </button>
      </div>

      <form className="code-lookup-card" onSubmit={handleLookup}>
        <label>Patient Access Code</label>
        <div className="code-input-row">
          <input
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="e.g. 483920"
            maxLength={6}
            required
          />
          <button type="submit" className="lookup-btn" disabled={loading}>
            {loading ? "Looking up..." : "Look Up"}
          </button>
        </div>
        {error && <div className="doctor-error">{error}</div>}
      </form>

      {patient && (
        <div className="patient-card">
          <h2>Patient Details</h2>

          <div className="patient-detail-grid">
            <div>
              <span className="detail-label">Name</span>
              <span className="detail-value">{patient.patient_name}</span>
            </div>
            <div>
              <span className="detail-label">Age</span>
              <span className="detail-value">{patient.patient_age}</span>
            </div>
            <div>
              <span className="detail-label">Gender</span>
              <span className="detail-value">{patient.patient_gender}</span>
            </div>
            <div>
              <span className="detail-label">Access Code</span>
              <span className="detail-value">{patient.access_code}</span>
            </div>
          </div>

          {patient.lab_notes && (
            <div className="lab-notes-block">
              <span className="detail-label">Lab Notes</span>
              <p>{patient.lab_notes}</p>
            </div>
          )}

          {patient.status === "pending" && (
            <>
              <button
                className="generate-btn"
                onClick={handleGenerateResult}
                disabled={analyzing}
              >
                {analyzing ? "Analyzing (this can take up to a minute)..." : "Generate Result"}
              </button>
              {analyzing && (
                <p className="analyzing-note">
                  Running the AI model and generating an explainability
                  heatmap — please don't close this page.
                </p>
              )}
            </>
          )}

          {patient.status === "analyzed" && patient.result && (
            <div className="result-block">
              <h3>AI Classification Result</h3>
              <div
                className="result-badge"
                style={{
                  background: (TUMOR_COLORS[patient.result.tumor] || "#2563eb") + "22",
                  color: TUMOR_COLORS[patient.result.tumor] || "#2563eb"
                }}
              >
                {patient.result.tumor}
              </div>
              <p className="result-confidence">
                Model Confidence: {patient.result.confidence}%
              </p>

              {patient.result.heatmap && (
                <div className="heatmap-block">
                  <span className="detail-label">Explainability Heatmap</span>
                  <img
                    src={patient.result.heatmap}
                    alt="Regions influencing the AI's prediction"
                    className="heatmap-img"
                  />
                  <p className="heatmap-caption">
                    Warmer colors show regions that most influenced the
                    model's decision, generated via Occlusion Sensitivity
                    on the actual Hybrid Quantum model.
                  </p>
                </div>
              )}

              <div className="doctor-disclaimer">
                This is an AI-generated classification intended to assist,
                not replace, clinical judgment. Final diagnosis and
                treatment decisions remain the responsibility of the
                reviewing physician.
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default DoctorDashboard;
