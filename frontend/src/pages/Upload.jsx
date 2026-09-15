import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { predictImage } from "../services/api";
import "./Upload.css";

function Upload() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selected = e.target.files[0];

    if (!selected) return;

    setFile(selected);
    setError("");
    setPreview(URL.createObjectURL(selected));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];

    if (!dropped) return;

    setFile(dropped);
    setError("");
    setPreview(URL.createObjectURL(dropped));
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an MRI image first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await predictImage(file);

      navigate("/prediction", {
        state: {
          result,
          imagePreview: preview,
        },
      });
    } catch (err) {
      const message =
        err.response?.data?.error ||
        "Prediction failed. Make sure the backend server is running.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-card">
        <h1>Upload Scan Result</h1>
        <p className="upload-subtitle">
          Upload the patient's MRI scan to generate an AI-classification
          report for the treating physician
        </p>

        <div
          className="dropzone"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
        >
          {preview ? (
            <img src={preview} alt="MRI preview" className="preview-img" />
          ) : (
            <div className="dropzone-placeholder">
              <p>Drag & drop your MRI image here</p>
              <p className="dropzone-or">or</p>
            </div>
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

        {error && <div className="upload-error">{error}</div>}

        <button
          className="analyze-btn"
          onClick={handleSubmit}
          disabled={loading || !file}
        >
          {loading ? "Analyzing..." : "Analyze MRI"}
        </button>

        <div className="upload-disclaimer">
          This tool provides AI-assisted screening results and is not a
          substitute for professional medical diagnosis.
        </div>
      </div>
    </div>
  );
}

export default Upload;
