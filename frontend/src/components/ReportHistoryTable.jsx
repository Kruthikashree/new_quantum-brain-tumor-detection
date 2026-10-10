import { useEffect, useMemo, useState } from "react";
import PortalLayout from "../components/PortalLayout";
import ReportHistoryTable from "../components/ReportHistoryTable";
import { listReports, getCurrentUser } from "../services/api";

const PAGE_SIZE = 10;
const PREDICTIONS = ["All", "Glioma", "Meningioma", "Pituitary", "No Tumor"];

function ReportHistory() {
  const user = getCurrentUser();
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");

  const [query, setQuery] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [prediction, setPrediction] = useState("All");
  const [sort, setSort] = useState({ key: "created_at", direction: "desc" });
  const [page, setPage] = useState(1);

  useEffect(() => {
    listReports()
      .then(setReports)
      .catch((err) => setError(err.response?.data?.error || "Could not load reports."));
  }, []);

  const handleSort = (key) => {
    setPage(1);
    setSort((s) =>
      s.key === key
        ? { key, direction: s.direction === "asc" ? "desc" : "asc" }
        : { key, direction: "asc" }
    );
  };

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    const from = dateFrom ? new Date(dateFrom) : null;
    const to = dateTo ? new Date(dateTo + "T23:59:59") : null;

    let rows = reports.filter((r) => {
      if (q) {
        const haystack = [r.patient.full_name, r.patient.patient_id, r.doctor.full_name, r.referral_code]
          .join(" ")
          .toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      const created = new Date(r.created_at);
      if (from && created < from) return false;
      if (to && created > to) return false;
      if (prediction !== "All" && r.result?.tumor !== prediction) return false;
      return true;
    });

    rows = [...rows].sort((a, b) => {
      let av, bv;
      if (sort.key === "created_at") {
        av = new Date(a.created_at).getTime();
        bv = new Date(b.created_at).getTime();
      } else if (sort.key === "patient") {
        av = a.patient.full_name.toLowerCase();
        bv = b.patient.full_name.toLowerCase();
      } else if (sort.key === "tumor") {
        av = a.result?.tumor || "";
        bv = b.result?.tumor || "";
      }
      if (av < bv) return sort.direction === "asc" ? -1 : 1;
      if (av > bv) return sort.direction === "asc" ? 1 : -1;
      return 0;
    });

    return rows;
  }, [reports, query, dateFrom, dateTo, prediction, sort]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const clampedPage = Math.min(page, totalPages);

  return (
    <PortalLayout title="Report History" subtitle="All reports you can access">
      {error && <div className="pt-alert">{error}</div>}

      <div className="pt-card">
        <div className="pt-filters">
          <div className="pt-field" style={{ minWidth: 220 }}>
            <label>Search</label>
            <input
              placeholder="Patient, ID, doctor or code"
              value={query}
              onChange={(e) => { setQuery(e.target.value); setPage(1); }}
            />
          </div>
          <div className="pt-field">
            <label>From</label>
            <input type="date" value={dateFrom} onChange={(e) => { setDateFrom(e.target.value); setPage(1); }} />
          </div>
          <div className="pt-field">
            <label>To</label>
            <input type="date" value={dateTo} onChange={(e) => { setDateTo(e.target.value); setPage(1); }} />
          </div>
          <div className="pt-field">
            <label>Prediction</label>
            <select value={prediction} onChange={(e) => { setPrediction(e.target.value); setPage(1); }}>
              {PREDICTIONS.map((p) => <option key={p}>{p}</option>)}
            </select>
          </div>
        </div>

        <p className="pt-muted" style={{ marginBottom: 12 }}>
          {filtered.length} report{filtered.length !== 1 ? "s" : ""} found
        </p>

        <ReportHistoryTable
          reports={filtered}
          role={user?.role}
          page={clampedPage}
          pageSize={PAGE_SIZE}
          sort={sort}
          onSort={handleSort}
        />

        {filtered.length > PAGE_SIZE && (
          <div className="pt-pagination">
            <button
              className="pt-btn pt-btn-outline"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={clampedPage === 1}
            >
              Previous
            </button>
            <span>Page {clampedPage} of {totalPages}</span>
            <button
              className="pt-btn pt-btn-outline"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={clampedPage === totalPages}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </PortalLayout>
  );
}

export default ReportHistory;