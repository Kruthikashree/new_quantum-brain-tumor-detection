import "./Healthcare.css";
import { FaUserMd, FaClipboardList, FaCheckCircle } from "react-icons/fa";

function Healthcare() {
    return (
        <section className="healthcare">
            <div className="healthcare-visual">
                <div className="hc-card">
                    <FaUserMd className="hc-doctor-icon" />
                    <div className="hc-scan-mini"></div>
                    <div className="hc-badge">AI Analysis</div>
                </div>
            </div>

            <div className="healthcare-text">
                <h2>Designed for Healthcare Professionals</h2>
                <p>
                    Quantum Brain AI is designed as an AI-assisted research and
                    decision-support system for brain MRI analysis. Final diagnosis
                    and treatment decisions remain with qualified healthcare
                    professionals.
                </p>

                <div className="hc-points">
                    <div className="hc-point">
                        <FaCheckCircle /> AI-Assisted Analysis
                    </div>
                    <div className="hc-point">
                        <FaClipboardList /> Structured Results
                    </div>
                    <div className="hc-point">
                        <FaUserMd /> Professional Review
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Healthcare;