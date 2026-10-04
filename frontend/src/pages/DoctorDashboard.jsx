import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PortalLayout from "../components/PortalLayout";
import ReportsTable from "../components/ReportsTable";
import { lookupReport, listReports, getCurrentUser } from "../services/api";

function DoctorDashboard() {
  const navigate = useNavigate();
  const user = getCurrentUser();
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [reports, setReports] = useState([]);

  useEffect(() => {
    listReports().then(setReports).catch(() => {});
  }, []);

  const handleLookup = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await lookupReport(code);
      navigate(`/reports/${data.id}`);
    } catch (err) {
      setError(err.response?.data?.error || "Could not look up the report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PortalLayout
      role="doctor"
      title={`Welcome, Dr. ${user?.name || ""}`}
            subtitle="Enter a referral code to unlock and view a report"
    >
      <form className="pt-card" onSubmit={handleLookup}>
        <h2>Enter Referral Code</h2>
        {error && <div className="pt-alert">{error}</div>}
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <div className="pt-field" style={{ flex: "0 1 220px" }}>
            <input
              inputMode="numeric"
              maxLength={6}
              placeholder="6-digit code"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
            />
          </div>
          <button
            type="submit"
            className="pt-btn pt-btn-primary"
            disabled={code.length !== 6 || loading}
          >
            {loading ? "Checking..." : "View Report"}
          </button>
        </div>
      </form>

      <div className="pt-card">
        <h2>Reports assigned to you</h2>
        <ReportsTable reports={reports.slice(0, 5)} role="doctor" empty="No reports assigned to you yet." />
      </div>
    </PortalLayout>
  );
}

export default DoctorDashboard;