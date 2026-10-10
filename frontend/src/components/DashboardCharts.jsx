const TUMOR_COLORS = {
  Glioma: "#dc2626",
  Meningioma: "#d97706",
  "No Tumor": "#16a34a",
  Pituitary: "#7c3aed",
};

export function DistributionChart({ distribution }) {
  const total = Object.values(distribution).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="dist-chart">
      {Object.entries(distribution).map(([label, count]) => (
        <div className="dist-row" key={label}>
          <span className="dist-label">{label}</span>
          <div className="dist-track">
            <div
              className="dist-fill"
              style={{ width: `${(count / total) * 100}%`, background: TUMOR_COLORS[label] }}
            />
          </div>
          <span className="dist-count">{count}</span>
        </div>
      ))}
    </div>
  );
}

export function WeeklyChart({ weekly }) {
  const max = Math.max(1, ...weekly.map((d) => d.count));
  return (
    <div className="weekly-chart">
      {weekly.map((d) => (
        <div className="weekly-bar-col" key={d.date}>
          <div className="weekly-bar-track">
            <div className="weekly-bar-fill" style={{ height: `${(d.count / max) * 100}%` }} />
          </div>
          <span className="weekly-day">
            {new Date(d.date).toLocaleDateString(undefined, { weekday: "short" })}
          </span>
          <span className="weekly-count">{d.count}</span>
        </div>
      ))}
    </div>
  );
}