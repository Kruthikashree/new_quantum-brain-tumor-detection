import { Link } from "react-router-dom";
import "./Footer.css";

function Footer() {
    return (
        <footer className="site-footer">
            <div className="footer-top">
                <div className="footer-brand">
                    <div className="footer-logo">🧠 Quantum Brain AI</div>
                    <p>Quantum-Enhanced Brain Tumor Detection</p>
                </div>

                    <div className="footer-links">
                    <Link to="/">Home</Link>
                    <a href="#how-it-works">How It Works</a>
                    <Link to="/login">Login</Link>
                    <Link to="/signup">Sign Up</Link>
                </div>
            </div>

            <div className="footer-bottom">
                © 2026 Quantum Brain AI | Academic Research Project
            </div>
        </footer>
    );
}

export default Footer;