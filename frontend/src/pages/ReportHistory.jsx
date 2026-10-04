import { useEffect, useState } from "react";
import PortalLayout from "../components/PortalLayout";
import ReportsTable from "../components/ReportsTable";
import { listReports, getCurrentUser } from "../services/api";

function ReportHistory() {
  const user = getCurrentUser();
  const [reports, setReports] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    listReports()
      .then(setReports)
      .catch((err) => setError(err.response?.data?.error || "Could not load reports."));
  }, []);

  const q = query.trim().toLowerCase();
  const shown = q
    ? reports.filter((r) =>
        [r.patient.full_name, r.patient.patient_id, r.doctor.full_name, r.referral_code]
          .join(" ")
          .toLowerCase()
          .includes(q)
      )
    : reports;

  return (
    <PortalLayout title="Report History" subtitle="All reports you can access">
      {error && <div className="pt-alert">{error}</div>}
      <div className="pt-card">
        <div className="pt-field" style={{ maxWidth: 360, marginBottom: 16 }}>
          <input
            placeholder="Search by patient, ID, doctor or code"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <ReportsTable reports={shown} role={user?.role} />
      </div>
    </PortalLayout>
  );
}

export default ReportHistory;