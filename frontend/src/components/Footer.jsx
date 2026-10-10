import { Link } from "react-router-dom";
import "./Footer.css";

function Footer() {
    const year = new Date().getFullYear();

    return (
        <footer className="site-footer">
            <div className="footer-top">
                <div className="footer-brand">
                    <div className="footer-logo">🧠 Quantum Brain AI</div>
                    <p>Quantum-Enhanced Brain Tumor Detection — AI-assisted brain MRI classification combining deep learning and hybrid quantum computing.</p>
                </div>

                <div className="footer-links">
                    <Link to="/">Home</Link>
                    <a href="#how-it-works">How It Works</a>
                    <Link to="/login">Login</Link>
                    <Link to="/signup">Sign Up</Link>
                </div>
            </div>

            <div className="footer-bottom">
                © {year} Quantum Brain AI | Academic Research Project
            </div>
        </footer>
    );
}

export default Footer;