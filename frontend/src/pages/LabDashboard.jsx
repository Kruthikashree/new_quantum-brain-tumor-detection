import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser, logout, createPatient } from "../services/api";
import { useEffect } from "react";
import "./LabDashboard.css";

function LabDashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [patientGender, setPatientGender] = useState("Male");
  const [labNotes, setLabNotes] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [accessCode, setAccessCode] = useState(null);

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

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  const resetForm = () => {
    setPatientName("");
    setPatientAge("");
    setPatientGender("Male");
    setLabNotes("");
    setFile(null);
    setPreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!file) {
      setError("Please upload an MRI scan.");
      return;
    }

    setLoading(true);

    try {
      const data = await createPatient({
        patientName,
        patientAge,
        patientGender,
        labNotes,
        imageFile: file,
      });

      setAccessCode(data.access_code);
    } catch (err) {
      const message =
        err.response?.data?.error ||
        "Failed to create patient record. Make sure the backend is running.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  if (accessCode) {
    return (
      <div className="lab-page">
        <div className="access-code-card">
          <h1>Patient Record Created</h1>
          <p>Share this access code with the treating physician:</p>
          <div className="access-code-display">{accessCode}</div>
          <p className="access-code-note">
            The doctor will enter this code to view the scan and generate
            the AI classification report.
          </p>
          <button
            className="primary-btn"
            onClick={() => {
              setAccessCode(null);
              resetForm();
            }}
          >
            Upload Another Scan
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="lab-page">
      <div className="lab-header">
        <div>
          <h1>Welcome, {user.name}</h1>
          <p>Laboratory Portal — Register a patient and upload their MRI scan</p>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Log Out
        </button>
      </div>

      <form className="lab-form-card" onSubmit={handleSubmit}>
        <h2>New Patient Record</h2>

        {error && <div className="lab-error">{error}</div>}

        <div className="form-row">
          <div className="form-field">
            <label>Patient Name</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              placeholder="Full name"
              required
            />
          </div>

          <div className="form-field">
            <label>Age</label>
            <input
              type="number"
              value={patientAge}
              onChange={(e) => setPatientAge(e.target.value)}
              placeholder="Age"
              min="0"
              required
            />
          </div>

          <div className="form-field">
            <label>Gender</label>
            <select
              value={patientGender}
              onChange={(e) => setPatientGender(e.target.value)}
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        <div className="form-field">
          <label>Lab Notes (optional)</label>
          <textarea
            value={labNotes}
            onChange={(e) => setLabNotes(e.target.value)}
            placeholder="Any relevant notes for the physician"
            rows={3}
          />
        </div>

        <div className="form-field">
          <label>MRI Scan</label>
          <div className="lab-dropzone">
            {preview ? (
              <img src={preview} alt="MRI preview" className="lab-preview-img" />
            ) : (
              <p>No file selected</p>
            )}
            <label className="browse-btn">
              Browse Files
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                hidden
              />
            </label>
          </div>
        </div>

        <button type="submit" className="analyze-btn" disabled={loading}>
          {loading ? "Uploading..." : "Create Patient Record & Get Access Code"}
        </button>
      </form>
    </div>
  );
}

export default LabDashboard;
