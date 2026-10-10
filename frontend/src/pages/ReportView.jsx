import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import HeatmapExplorer from "../components/HeatmapExplorer";
import { getReport, downloadReportPdf, getCurrentUser } from "../services/api";

const TUMOR_COLORS = {
  Glioma: "#dc2626",
  Meningioma: "#d97706",
  "No Tumor": "#16a34a",
  Pituitary: "#7c3aed",
};

function formatScanDate(value) {
  try {
    const d = new Date(value);
    if (isNaN(d.getTime())) return value;
    return d.toLocaleString(undefined, {
      day: "2-digit", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  } catch {
    return value;
  }
}

function ReportView() {
  const { id } = useParams();
  const user = getCurrentUser();
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => {
    getReport(id)
      .then(setReport)
      .catch((err) => setError(err.response?.data?.error || "Could not load the report."));
  }, [id]);

  

  const download = async () => {
    setError("");
    try {
      const blob = await downloadReportPdf(report.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `MRI_Report_${report.referral_code}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Could not download the report.");
    }
  };

  const tumor = report?.result?.tumor;
  const color = TUMOR_COLORS[tumor] || "#2563eb";
  const isLab = user?.role === "lab";

  return (
    <PortalLayout title="MRI Analysis Report" subtitle="AI-assisted analysis for physician review">
      {error && <div className="pt-alert">{error}</div>}
      {note && <div className="pt-note">{note}</div>}
      {!report && !error && <p className="pt-muted">Loading...</p>}

      {report && (
        <>
          <div className="pt-card">
            <h2>Patient and doctor</h2>
            <div className="pt-detail">
              <div><span>Patient Name</span><b>{report.patient.full_name}</b></div>
              <div><span>Patient ID</span><b>{report.patient.patient_id}</b></div>
              <div><span>Age</span><b>{report.patient.age}</b></div>
              <div><span>Gender</span><b>{report.patient.gender}</b></div>
              <div><span>Doctor</span><b>{report.doctor.full_name}</b></div>
              <div><span>Hospital</span><b>{report.doctor.hospital}</b></div>
              <div><span>MRI Scan Date & Time</span><b>{formatScanDate(report.scan_date)}</b></div>
              <div><span>Laboratory</span><b>{report.lab_name}</b></div>
            </div>
            {report.clinical_notes && (
              <p style={{ marginTop: 16 }}>
                <span className="pt-muted">Clinical notes: </span>
                {report.clinical_notes}
              </p>
            )}
          </div>

          {isLab && (
            <div className="pt-card">
              <h2>Referral code</h2>
              <div className="pt-code">{report.referral_code}</div>

              <p className="pt-muted">
                Doctor email: {report.email_status?.doctor ? "sent" : "not sent"} ·
                Patient email: {report.email_status?.patient ? "sent" : "not sent"}
              </p>
            </div>
          )}
          <div className="pt-card">
            <h2>AI analysis</h2>

            {report.result ? (
              <>
                                <div className="result-hero" style={{ borderColor: color + "40", background: color + "0d" }}>
                  <div className="result-hero-label">AI PREDICTION</div>
                  <div className="result-hero-badge" style={{ background: color + "20", color }}>
                    {tumor || "-"}
                  </div>

                  {report.result.probabilities && (
                    <div className="prob-breakdown">
                      {Object.entries(report.result.probabilities)
                        .sort((a, b) => b[1] - a[1])
                        .map(([label, pct]) => (
                          <div className="prob-row" key={label}>
                            <span className="prob-label">{label}</span>
                            <div className="prob-track">
                              <div
                                className="prob-fill"
                                style={{
                                  width: `${pct}%`,
                                  background: TUMOR_COLORS[label] || "#2563eb",
                                }}
                              />
                            </div>
                            <span className="prob-pct">{pct}%</span>
                          </div>
                        ))}
                    </div>
                  )}
                </div>

                <div className="pt-images">
                  {report.mri_image && (
                    <div><small>MRI scan</small><img src={report.mri_image} alt="MRI scan" /></div>
                  )}
                  {report.result.heatmap && (
                    <div>
                      <div className="heatmap-title-row">
                        <small>Grad-CAM style explainability heatmap</small>
                        <span className="heatmap-info-icon">
                          ⓘ
                          <div className="heatmap-tooltip">
                            <p className="heatmap-tooltip-note">
                              Highlighted regions show where the AI focused
                              when making this prediction — not a confirmed
                              tumor location.
                            </p>
                            <div className="legend-item">
                              <span className="legend-swatch" style={{ background: "linear-gradient(135deg,#ef4444,#f97316)" }}></span>
                              High influence (warm)
                            </div>
                            <div className="legend-item">
                              <span className="legend-swatch" style={{ background: "#eab308" }}></span>
                              Moderate influence
                            </div>
                            <div className="legend-item">
                              <span className="legend-swatch" style={{ background: "linear-gradient(135deg,#3b82f6,#60a5fa)" }}></span>
                              Low influence (cool)
                            </div>
                          </div>
                        </span>
                      </div>
                      <HeatmapExplorer src={report.result.heatmap} alt="Regions that influenced the prediction" />
                    </div>
                  )}
                </div>

                <div className="pt-disclaimer">
                  This is an AI-generated analysis intended to assist, not replace,
                  clinical judgment. It is not a confirmed diagnosis. Final
                  interpretation remains with the reviewing physician.
                </div>
              </>
            ) : (
              <p className="pt-muted">AI analysis is not available for this report.</p>
            )}

            <div className="pt-actions" style={{ marginTop: 16 }}>
              <button className="pt-btn pt-btn-primary" onClick={download}>Download Report</button>
            </div>
          </div>
        </>
      )}
    </PortalLayout>
  );
}

export default ReportView;