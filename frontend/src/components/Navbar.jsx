import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        🧠 Quantum Brain AI
      </div>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/upload">Predict</Link>
        <Link to="/doctors">Doctors</Link>
        <Link to="/history">History</Link>
      </div>

      <div className="auth-buttons">
        <Link to="/login">
          <button className="login-btn">Login</button>
        </Link>

        <Link to="/signup">
          <button className="signup-btn">Sign Up</button>
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;