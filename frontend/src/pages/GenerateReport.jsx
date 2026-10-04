import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import { createReport } from "../services/api";

const LANGUAGES = ["English", "Kannada", "Hindi", "Telugu", "Tamil", "Malayalam", "Marathi", "Other"];
const STEPS = ["Uploading MRI", "Saving Record", "Generating Referral Code", "Sending Notifications", "Complete"];
const REQUIRED = [
  "patient_name", "patient_id", "patient_age", "patient_gender",
  "patient_email", "patient_phone", "preferred_language",
  "doctor_name", "doctor_email", "hospital", "scan_date",
];
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

const nowLocal = () => {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
};

function GenerateReport() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    patient_name: "", patient_id: "", patient_age: "", patient_gender: "Male",
    patient_email: "", patient_phone: "", preferred_language: "English",
    doctor_name: "", doctor_email: "", hospital: "", doctor_id: "",
    scan_date: nowLocal(), clinical_notes: "",
  });
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [consent, setConsent] = useState(false);
  const [stage, setStage] = useState(-1);
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

  const valid =
    REQUIRED.every((k) => String(form[k]).trim()) &&
    EMAIL_RE.test(form.patient_email.trim()) &&
    EMAIL_RE.test(form.doctor_email.trim()) &&
    file &&
    consent;

  const busy = stage >= 0;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!valid || busy) return;

    setError("");
    setStage(0);
    uploadDone.current = false;

    const fd = new FormData();
    Object.entries(form).forEach(([k, v]) => fd.append(k, String(v).trim()));
    fd.append("image", file);
    fd.append("consent", "true");

    try {
      const data = await createReport(fd, (ev) => {
        if (!uploadDone.current && ev.total && ev.loaded >= ev.total) {
          uploadDone.current = true;
          setStage(1);
          timers.current.push(setTimeout(() => setStage(2), 500));
        }
      });

      timers.current.forEach(clearTimeout);
      setStage(3);
      timers.current = [
        setTimeout(() => setStage(4), 500),
        setTimeout(() => navigate(`/reports/${data.report.id}`), 1100),
      ];
    } catch (err) {
      timers.current.forEach(clearTimeout);
      setStage(-1);
      setError(err.response?.data?.error || "Report generation failed. Please try again.");
    }
  };

  if (busy) {
    return (
      <PortalLayout role="lab" title="Generating report" subtitle="Please keep this page open">
        <div className="pt-card">
          <ul className="pt-steps">
            {STEPS.map((label, i) => (
              <li key={label} className={i < stage || stage === 4 ? "done" : i === stage ? "active" : ""}>
                <span>{i < stage || stage === 4 ? "✓" : i + 1}</span>
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
      <form onSubmit={handleSubmit}>
        {error && <div className="pt-alert">{error}</div>}

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
          </div>
        </div>

        <div className="pt-card">
          <h2>Doctor information</h2>
          <div className="pt-grid-2">
            <div className="pt-field"><label>Doctor Full Name *</label><input value={form.doctor_name} onChange={set("doctor_name")} /></div>
            <div className="pt-field"><label>Doctor Email * (must match the doctor's portal login)</label><input type="email" value={form.doctor_email} onChange={set("doctor_email")} /></div>
            <div className="pt-field"><label>Hospital / Clinic Name *</label><input value={form.hospital} onChange={set("hospital")} /></div>
            <div className="pt-field"><label>Doctor ID (optional)</label><input value={form.doctor_id} onChange={set("doctor_id")} /></div>
          </div>
        </div>

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

          <label className="pt-consent">
            <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
            Patient consent has been obtained for digital processing and report sharing.
          </label>

          <button type="submit" className="pt-btn pt-btn-primary" disabled={!valid}>
            Generate Report
          </button>
        </div>
      </form>
    </PortalLayout>
  );
}

export default GenerateReport;