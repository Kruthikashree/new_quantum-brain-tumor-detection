import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import ReportsTable from "../components/ReportsTable";
import { listReports, getCurrentUser } from "../services/api";

function LabDashboard() {
  const user = getCurrentUser();
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    listReports()
      .then(setReports)
      .catch((err) => setError(err.response?.data?.error || "Could not load reports."));
  }, []);

  const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
  const thisWeek = reports.filter((r) => new Date(r.created_at).getTime() >= weekAgo).length;
  const undelivered = reports.filter(
    (r) => !r.email_status?.doctor || !r.email_status?.patient
  ).length;

  return (
    <PortalLayout
      role="lab"
      title={`Welcome, ${user?.name || ""}`}
      subtitle="Generate MRI analysis reports and share them with doctors"
    >
      {error && <div className="pt-alert">{error}</div>}

      <div className="pt-stats">
        <div className="pt-stat"><b>{reports.length}</b><span>Total reports</span></div>
        <div className="pt-stat"><b>{thisWeek}</b><span>Last 7 days</span></div>
        <div className="pt-stat"><b>{undelivered}</b><span>With undelivered emails</span></div>
      </div>

      <div className="pt-card">
        <h2>Generate MRI Report</h2>
        <p className="pt-muted">
          Enter the patient and doctor details, upload the MRI and let the AI
          produce a report with a referral code.
        </p>
        <Link to="/generate-report">
          <button className="pt-btn pt-btn-primary">Generate MRI Report</button>
        </Link>
      </div>

      <div className="pt-card">
        <h2>Recent reports</h2>
        <ReportsTable reports={reports.slice(0, 5)} role="lab" />
      </div>
    </PortalLayout>
  );
}

export default LabDashboard;