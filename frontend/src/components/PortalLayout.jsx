import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { getCurrentUser, logout } from "../services/api";
import "./PortalLayout.css";

const NAV = {
  lab: [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/generate-report", label: "Generate Report" },
    { to: "/reports", label: "Report History" },
    { to: "/profile", label: "Profile" },
  ],
  doctor: [
    { to: "/doctor-dashboard", label: "Dashboard" },
    { to: "/reports", label: "Report History" },
    { to: "/profile", label: "Profile" },
  ],
};

function PortalLayout({ role, title, subtitle, children }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const current = getCurrentUser();
    if (!current || !current.token) {
      logout();
      navigate("/login");
      return;
    }
    if (role && current.role !== role) {
      navigate(current.role === "doctor" ? "/doctor-dashboard" : "/dashboard");
      return;
    }
    setUser(current);
  }, [navigate, role]);

  if (!user) return null;

  const links = NAV[user.role] || NAV.lab;

  return (
    <div className="portal">
      <aside className="portal-side">
        <div className="portal-brand">
          Quantum Brain Tumor Detection
          <small>{user.role === "doctor" ? "Doctor Portal" : "Laboratory Portal"}</small>
        </div>

        <nav className="portal-nav">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>

        <div className="portal-user">
          <strong>{user.name}</strong>
          <span>{user.role === "doctor" ? "Doctor" : "Laboratory"}</span>
          <button
            className="portal-logout"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Log Out
          </button>
        </div>
      </aside>

      <main className="portal-main">
        <header className="portal-top">
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </header>
        {children}
      </main>
    </div>
  );
}

export default PortalLayout;