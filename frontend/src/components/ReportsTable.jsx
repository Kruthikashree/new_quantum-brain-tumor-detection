import { useNavigate } from "react-router-dom";

function ReportsTable({ reports, role, empty = "No reports yet." }) {
  const navigate = useNavigate();

  if (!reports.length) return <p className="pt-muted">{empty}</p>;

  return (
    <div className="pt-table-wrap">
      <table className="pt-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Patient ID</th>
            <th>{role === "doctor" ? "Laboratory" : "Doctor"}</th>
            <th>Prediction</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {reports.map((r) => (
            <tr key={r.id}>
              <td>{new Date(r.created_at).toLocaleDateString()}</td>
              <td>{r.patient.full_name}</td>
              <td>{r.patient.patient_id}</td>
              <td>{role === "doctor" ? r.lab_name : r.doctor.full_name}</td>
              <td>{r.result?.tumor || "-"}</td>
              <td>
                <button className="pt-btn pt-btn-outline" onClick={() => navigate(`/reports/${r.id}`)}>
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReportsTable;