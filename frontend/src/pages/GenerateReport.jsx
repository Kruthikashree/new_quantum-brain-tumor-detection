import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import { createReport } from "../services/api";

const LANGUAGES = ["English", "Kannada", "Hindi", "Telugu", "Tamil", "Malayalam", "Marathi", "Other"];
const ANALYSIS_STEPS = [
  "Uploading MRI",
  "Preprocessing",
  "Running AI analysis",
  "Generating explainability heatmap",
  "Finalizing report & sending notifications",
  "Complete",
];
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

const nowLocal = () => {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
};

const WIZARD_STEPS = ["Patient", "Doctor", "MRI Upload", "Review", "Result"];

function GenerateReport() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0); // 0..3 wizard, 4 = analyzing/result
  const [form, setForm] = useState({
    patient_name: "", patient_id: "", patient_age: "", patient_gender: "Male",
    patient_email: "", patient_phone: "", preferred_language: "English",
    doctor_name: "", doctor_email: "", hospital: "", doctor_id: "",
    scan_date: nowLocal(), clinical_notes: "",
  });
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [consent, setConsent] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStage, setAnalysisStage] = useState(0);
  const [error, setError] = useState("");
  const timers = useRef([]);
  const uploadDone = useRef(false);

  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleFile = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    if (!/\.(png|jpe?g)$/i.test(selected.name)) {
      setError("MRI image must be a PNG or JPG file.");
      return;
    }
    setError("");
    if (preview) URL.revokeObjectURL(preview);
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  // Per-step validation
  const patientValid =
    form.patient_name.trim() && form.patient_id.trim() && String(form.patient_age).trim() &&
    EMAIL_RE.test(form.patient_email.trim()) && form.patient_phone.trim();

  const doctorValid =
    form.doctor_name.trim() && EMAIL_RE.test(form.doctor_email.trim()) && form.hospital.trim();

  const uploadValid = !!file && form.scan_date.trim();

  const reviewValid = consent;

  const stepValid = [patientValid, doctorValid, uploadValid, reviewValid][step];

  const goNext = () => {
    setError("");
    if (!stepValid) {
      setError("Please complete all required fields before continuing.");
      return;
    }
    setStep((s) => Math.min(s + 1, 3));
  };
  const goBack = () => {
    setError("");
    setStep((s) => Math.max(s - 1, 0));
  };

  const handleSubmit = async () => {
    if (!reviewValid) return;

    setError("");
    setStep(4);
    setAnalyzing(true);
    setAnalysisStage(0);
    uploadDone.current = false;

    const fd = new FormData();
    Object.entries(form).forEach(([k, v]) => fd.append(k, String(v).trim()));
    fd.append("image", file);
    fd.append("consent", "true");

    try {
      const data = await createReport(fd, (ev) => {
        if (!uploadDone.current && ev.total && ev.loaded >= ev.total) {
          uploadDone.current = true;
          setAnalysisStage(1);
          timers.current.push(setTimeout(() => setAnalysisStage(2), 2000));
          timers.current.push(setTimeout(() => setAnalysisStage(3), 14000));
          timers.current.push(setTimeout(() => setAnalysisStage(4), 22000));
        }
      });

      timers.current.forEach(clearTimeout);
      setAnalysisStage(5);
      timers.current = [setTimeout(() => navigate(`/reports/${data.report.id}`), 900)];
    } catch (err) {
      timers.current.forEach(clearTimeout);
      setAnalyzing(false);
      setStep(3);
      setError(err.response?.data?.error || "Report generation failed. Please try again.");
    }
  };

  // ---------- Step 5: analysis progress ----------
  if (step === 4) {
    return (
      <PortalLayout role="lab" title="Generating report" subtitle="Please keep this page open — AI analysis is running">
        <div className="pt-card">
          <ul className="pt-steps">
            {ANALYSIS_STEPS.map((label, i) => (
              <li key={label} className={i < analysisStage || analysisStage === 5 ? "done" : i === analysisStage ? "active" : ""}>
                <span>{i < analysisStage || analysisStage === 5 ? "✓" : i + 1}</span>
                {label}
              </li>
            ))}
          </ul>
        </div>
      </PortalLayout>
    );
  }

  return (
    <PortalLayout role="lab" title="Generate MRI Report" subtitle="Enter patient, doctor and MRI details">
      <div className="pt-card">
        <ol className="wizard-progress">
          {WIZARD_STEPS.slice(0, 4).map((label, i) => (
            <li key={label} className={i === step ? "active" : i < step ? "done" : ""}>
              <span className="wizard-dot">{i < step ? "✓" : i + 1}</span>
              {label}
            </li>
          ))}
        </ol>
      </div>

      {error && <div className="pt-alert">{error}</div>}

      {/* Step 0: Patient */}
      {step === 0 && (
        <div className="pt-card">
          <h2>Patient information</h2>
          <div className="pt-grid-3">
            <div className="pt-field"><label>Patient Full Name *</label><input value={form.patient_name} onChange={set("patient_name")} /></div>
            <div className="pt-field"><label>Patient ID *</label><input value={form.patient_id} onChange={set("patient_id")} /></div>
            <div className="pt-field"><label>Age *</label><input type="number" min="0" max="120" value={form.patient_age} onChange={set("patient_age")} /></div>
            <div className="pt-field">
              <label>Gender *</label>
              <select value={form.patient_gender} onChange={set("patient_gender")}>
                <option>Male</option><option>Female</option><option>Other</option>
              </select>
            </div>
            <div className="pt-field"><label>Patient Email *</label><input type="email" value={form.patient_email} onChange={set("patient_email")} /></div>
            <div className="pt-field"><label>Patient Phone Number *</label><input type="tel" value={form.patient_phone} onChange={set("patient_phone")} /></div>
            <div className="pt-field">
              <label>Preferred Language *</label>
              <select value={form.preferred_language} onChange={set("preferred_language")}>
                {LANGUAGES.map((l) => <option key={l}>{l}</option>)}
              </select>
            </div>
          </div>
          <div className="pt-actions" style={{ justifyContent: "flex-end" }}>
            <button className="pt-btn pt-btn-primary" onClick={goNext} disabled={!patientValid}>Next: Doctor</button>
          </div>
        </div>
      )}

      {/* Step 1: Doctor */}
      {step === 1 && (
        <div className="pt-card">
          <h2>Doctor information</h2>
          <div className="pt-grid-2">
            <div className="pt-field"><label>Doctor Full Name *</label><input value={form.doctor_name} onChange={set("doctor_name")} /></div>
            <div className="pt-field"><label>Doctor Email * (must match the doctor's portal login)</label><input type="email" value={form.doctor_email} onChange={set("doctor_email")} /></div>
            <div className="pt-field"><label>Hospital / Clinic Name *</label><input value={form.hospital} onChange={set("hospital")} /></div>
            <div className="pt-field"><label>Doctor ID (optional)</label><input value={form.doctor_id} onChange={set("doctor_id")} /></div>
          </div>
          <div className="pt-actions" style={{ justifyContent: "space-between" }}>
            <button className="pt-btn pt-btn-outline" onClick={goBack}>Back</button>
            <button className="pt-btn pt-btn-primary" onClick={goNext} disabled={!doctorValid}>Next: MRI Upload</button>
          </div>
        </div>
      )}

      {/* Step 2: MRI Upload */}
      {step === 2 && (
        <div className="pt-card">
          <h2>MRI information</h2>
          <div className="pt-grid-2">
            <div className="pt-field">
              <label>Scan Date & Time *</label>
              <input type="datetime-local" max={nowLocal()} value={form.scan_date} onChange={set("scan_date")} />
              <button
                type="button"
                className="pt-btn pt-btn-outline"
                style={{ marginTop: 6, alignSelf: "flex-start", padding: "6px 12px", fontSize: 12.5 }}
                onClick={() => setForm((f) => ({ ...f, scan_date: nowLocal() }))}
              >
                Use current date & time
              </button>
            </div>
            <div className="pt-field"><label>Clinical Notes (optional)</label><textarea rows={3} value={form.clinical_notes} onChange={set("clinical_notes")} /></div>
          </div>

          <div className="pt-field" style={{ marginTop: 16 }}>
            <label>MRI Image * (PNG or JPG)</label>
            <div className="pt-dropzone">
              {preview ? <img src={preview} alt="MRI preview" /> : <p>No file selected</p>}
              <label className="pt-btn pt-btn-outline" style={{ display: "inline-block" }}>
                Browse Files
                <input type="file" accept=".png,.jpg,.jpeg" onChange={handleFile} hidden />
              </label>
            </div>
          </div>

          <div className="pt-actions" style={{ justifyContent: "space-between" }}>
            <button className="pt-btn pt-btn-outline" onClick={goBack}>Back</button>
            <button className="pt-btn pt-btn-primary" onClick={goNext} disabled={!uploadValid}>Next: Review</button>
          </div>
        </div>
      )}

      {/* Step 3: Review + Consent */}
      {step === 3 && (
        <div className="pt-card">
          <h2>Review before generating</h2>

          <div className="pt-detail" style={{ marginBottom: 16 }}>
            <div><span>Patient</span><b>{form.patient_name} ({form.patient_id})</b></div>
            <div><span>Age / Gender</span><b>{form.patient_age} / {form.patient_gender}</b></div>
            <div><span>Patient contact</span><b>{form.patient_email} · {form.patient_phone}</b></div>
            <div><span>Preferred language</span><b>{form.preferred_language}</b></div>
            <div><span>Doctor</span><b>{form.doctor_name}</b></div>
            <div><span>Doctor email</span><b>{form.doctor_email}</b></div>
            <div><span>Hospital</span><b>{form.hospital}</b></div>
            <div><span>Scan date & time</span><b>{new Date(form.scan_date).toLocaleString()}</b></div>
          </div>

          {preview && (
            <div style={{ marginBottom: 16 }}>
              <small className="pt-muted">MRI preview</small>
              <img src={preview} alt="MRI preview" style={{ maxWidth: 220, borderRadius: 10, display: "block", marginTop: 6 }} />
            </div>
          )}

          {form.clinical_notes && (
            <p style={{ marginBottom: 16 }}>
              <span className="pt-muted">Clinical notes: </span>{form.clinical_notes}
            </p>
          )}

          <label className="pt-consent">
            <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
            Patient consent has been obtained for digital processing and report sharing.
          </label>

          <div className="pt-actions" style={{ justifyContent: "space-between" }}>
            <button className="pt-btn pt-btn-outline" onClick={goBack}>Back</button>
            <button className="pt-btn pt-btn-primary" onClick={handleSubmit} disabled={!reviewValid}>
              Generate Report
            </button>
          </div>
        </div>
      )}
    </PortalLayout>
  );
}

export default GenerateReport;