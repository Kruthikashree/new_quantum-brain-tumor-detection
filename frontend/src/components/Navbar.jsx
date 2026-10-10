import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getCurrentUser, logout } from "../services/api";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getCurrentUser());
  }, []);

  const handleLogout = () => {
    logout();
    setUser(null);
    navigate("/");
  };

  const dashboardPath = user?.role === "doctor" ? "/doctor-dashboard" : "/dashboard";

  return (
    <nav className="navbar">
      <div className="logo">
        <span className="logo-icon">🧠</span> Quantum Brain AI
      </div>

      

      <div className="auth-buttons">
        {user ? (
          <>
            <Link to={dashboardPath}>
              <button className="login-btn">{user.name}</button>
            </Link>
            <button className="signup-btn" onClick={handleLogout}>
              Log Out
            </button>
          </>
        ) : (
          <>
            <Link to="/login">
              <button className="login-btn">Login</button>
            </Link>
            <Link to="/signup">
              <button className="signup-btn">Sign Up</button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;