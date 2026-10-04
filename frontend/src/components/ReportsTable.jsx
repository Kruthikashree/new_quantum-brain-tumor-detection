import { useNavigate } from "react-router-dom";

function ReportsTable({ reports, role, empty = "No reports yet." }) {
  const navigate = useNavigate();
  const isLab = role === "lab";

  const analyzed = reports.filter((r) => r.status === "analyzed");
  const pending = reports.filter((r) => r.status !== "analyzed");

  return (
    <div>
      {analyzed.length === 0 && pending.length === 0 && (
        <p className="pt-muted">{empty}</p>
      )}

      {analyzed.length > 0 && (
        <div className="pt-table-wrap">
          <table className="pt-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Patient</th>
                <th>Patient ID</th>
                <th>{role === "doctor" ? "Laboratory" : "Doctor"}</th>
                {!isLab && <th>Prediction</th>}
                <th></th>
              </tr>
            </thead>
            <tbody>
              {analyzed.map((r) => (
                <tr key={r.id}>
                  <td>{new Date(r.created_at).toLocaleDateString()}</td>
                  <td>{r.patient.full_name}</td>
                  <td>{r.patient.patient_id}</td>
                  <td>{role === "doctor" ? r.lab_name : r.doctor.full_name}</td>
                  {!isLab && <td>{r.result?.tumor || "-"}</td>}
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
      )}

      {!isLab && pending.length > 0 && (
        <div style={{ marginTop: analyzed.length > 0 ? 28 : 0 }}>
          <p className="pt-muted" style={{ marginBottom: 10, fontWeight: 600 }}>
            Pending analysis ({pending.length})
          </p>
          <div className="pt-table-wrap">
            <table className="pt-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Patient</th>
                  <th>Patient ID</th>
                  <th>Laboratory</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {pending.map((r) => (
                  <tr key={r.id}>
                    <td>{new Date(r.created_at).toLocaleDateString()}</td>
                    <td>{r.patient.full_name}</td>
                    <td>{r.patient.patient_id}</td>
                    <td>{r.lab_name}</td>
                    <td>
                      <button className="pt-btn pt-btn-primary" onClick={() => navigate(`/reports/${r.id}`)}>
                        Pending — View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default ReportsTable;