import { Link } from "react-router-dom";
import "./AuthLayout.css";

function AuthLayout({ children }) {
  return (
    <div className="signup-page">
      <nav className="auth-navbar">
        <Link to="/" className="auth-brand">
          <span className="auth-brand-icon">🧠</span>
          Quantum Brain AI
        </Link>
        <div className="auth-nav-actions">
          <Link to="/login" className="nav-btn-outline">Login</Link>
          <Link to="/signup" className="nav-btn-solid">Sign Up</Link>
        </div>
      </nav>

      <main className="auth-layout">
        <section className="auth-intro">
          <span className="auth-badge">AI-POWERED MEDICAL DIAGNOSTICS</span>
          <h2 className="auth-headline">
            Join <span className="gradient-text">Quantum Brain AI</span>
          </h2>
          <p>
            Create an account to submit MRI scans and review AI-assisted
            analysis with Grad-CAM style explanations.
          </p>
          <div className="auth-chips">
            <span>✓ AI-Powered MRI Analysis</span>
            <span>✓ 4 Tumor Classes</span>
            <span>✓ Hybrid Quantum Model</span>
          </div>
        </section>

        <section className="auth-panel">{children}</section>
      </main>
    </div>
  );
}

export default AuthLayout;