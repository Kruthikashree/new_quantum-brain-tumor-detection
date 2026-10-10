import { Link } from "react-router-dom";
import "./Healthcare.css";
import { FaUserMd, FaClipboardList, FaCheckCircle } from "react-icons/fa";
import { getCurrentUser } from "../services/api";

function Healthcare() {
    const user = getCurrentUser();

    return (
        <section className="healthcare" id="healthcare">
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
                    Laboratory staff submit MRI scans and generate AI-assisted reports.
                    Each report is linked to a 6-digit referral code, and only the
                    doctor it was addressed to can unlock and review it after logging
                    in. Predictions are intended to support professional assessment
                    and do not replace a clinician's judgment — final diagnosis and
                    treatment decisions remain with qualified healthcare professionals.
                </p>

                <div className="hc-points">
                    <div className="hc-point"><FaCheckCircle /> AI-Assisted Analysis</div>
                    <div className="hc-point"><FaClipboardList /> Referral-Coded Reports</div>
                    <div className="hc-point"><FaUserMd /> Professional Review</div>
                </div>

                {!user && (
                    <Link to="/login">
                        <button className="pt-btn pt-btn-primary" style={{ marginTop: 24 }}>
                            Log In to the Portal
                        </button>
                    </Link>
                )}
            </div>
        </section>
    );
}

export default Healthcare;