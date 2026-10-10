import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import ReportsTable from "../components/ReportsTable";
import { DistributionChart, WeeklyChart } from "../components/DashboardCharts";
import { listReports, getReportStats, getCurrentUser } from "../services/api";

function LabDashboard() {
  const user = getCurrentUser();
  const [reports, setReports] = useState([]);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    listReports().then(setReports).catch(() => {});
    getReportStats()
      .then(setStats)
      .catch((err) => setError(err.response?.data?.error || "Could not load dashboard stats."));
  }, []);

  return (
    <PortalLayout
      role="lab"
      title={`Welcome, ${user?.name || ""}`}
      subtitle="Generate MRI analysis reports and share them with doctors"
    >
      {error && <div className="pt-alert">{error}</div>}

      {stats && (
        <>
          <div className="pt-stats">
            <div className="pt-stat"><b>{stats.total}</b><span>Total reports</span></div>
            <div className="pt-stat"><b>{stats.last_7_days}</b><span>Last 7 days</span></div>
            <div className="pt-stat"><b>{stats.pending_email}</b><span>Pending email delivery</span></div>
          </div>

          <div className="pt-grid-2" style={{ marginBottom: 20 }}>
            <div className="pt-card">
              <h2>Prediction distribution</h2>
              <DistributionChart distribution={stats.distribution} />
            </div>
            <div className="pt-card">
              <h2>Reports this week</h2>
              <WeeklyChart weekly={stats.weekly} />
            </div>
          </div>
        </>
      )}

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