import { useState } from "react";
import "./Hero.css";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { getCurrentUser } from "../services/api";

function Hero() {
    const user = getCurrentUser();
    const [heatmapView, setHeatmapView] = useState(false);

    const primaryTo = !user
        ? "/signup"
        : user.role === "doctor"
        ? "/doctor-dashboard"
        : "/dashboard";

    const primaryLabel = !user ? "Get Started" : "Go to Dashboard";

    return (
        <section className="hero">

            <motion.div
                className="hero-left"
                initial={{x:-60,opacity:0}}
                animate={{x:0,opacity:1}}
                transition={{duration:0.8}}
            >
                <div className="hero-badge">
                    <span></span> AI-POWERED MEDICAL DIAGNOSTICS
                </div>

                <h1>
                    Smarter Brain MRI Analysis
                    <br/>
                    with <span className="accent">Hybrid AI</span>
                </h1>

                <p>
                    Quantum Brain AI combines deep-learning feature extraction
                    (MobileNetV2), a hybrid quantum-classical classifier, and
                    Grad-CAM style explainability to support faster, more
                    transparent brain MRI assessment.
                </p>

                <div className="hero-buttons">
                    <Link to={primaryTo}>
                        <button className="primary-btn">{primaryLabel}</button>
                    </Link>
                    <a href="#how-it-works">
                        <button className="secondary-btn">Explore How It Works</button>
                    </a>
                </div>

                <ul className="hero-checklist">
                    <li>✓ AI-Powered MRI Analysis</li>
                    <li>✓ 4 Tumor Classes</li>
                    <li>✓ Hybrid Quantum Model</li>
                </ul>
            </motion.div>

            <motion.div
                className="hero-right"
                initial={{x:60,opacity:0}}
                animate={{x:0,opacity:1}}
                transition={{duration:0.8}}
            >
                <div className="mri-panel">
                    <div className="mri-panel-header">
                        <span className="dot red"></span>
                        <span className="dot yellow"></span>
                        <span className="dot green"></span>
                        <span className="mri-panel-title">MRI Diagnostic Viewer</span>
                        <button
                            className="mri-toggle"
                            onClick={() => setHeatmapView((v) => !v)}
                            type="button"
                        >
                            {heatmapView ? "View MRI" : "View Grad-CAM"}
                        </button>
                    </div>

                    <div className="mri-panel-body">
                        <div className={`mri-scan ${heatmapView ? "heatmap-mode" : ""}`}>
                            <div className="mri-grid"></div>
                            <div className="scan-line"></div>
                            {heatmapView && <div className="heat-zone"></div>}
                            {!heatmapView && <div className="detect-box"></div>}
                            <svg className="brain-outline" viewBox="0 0 200 200">
                                <path d="M100 25c-30 0-52 20-58 45-10 4-16 15-13 27-6 8-6 20 2 28-2 14 8 27 22 30 6 12 20 20 34 20 8 0 15-2 21-6 6 4 13 6 21 6 14 0 28-8 34-20 14-3 24-16 22-30 8-8 8-20 2-28 3-12-3-23-13-27-6-25-28-45-58-45-4 0-8 0-12 1-4-1-8-1-12-1z"
                                    fill="none" stroke="#2563eb" strokeWidth="2" opacity="0.55"/>
                            </svg>
                            {[...Array(6)].map((_, i) => (
                                <span key={i} className={`node node-${i}`}></span>
                            ))}
                        </div>
                        <p className="mri-caption">
                            Illustrative visualization — not an actual patient scan or prediction.
                        </p>

                        <div className="mri-pipeline">
                            <div className="mri-step done">MRI Input</div>
                            <div className="mri-arrow">↓</div>
                            <div className="mri-step done">Feature Extraction</div>
                            <div className="mri-arrow">↓</div>
                            <div className="mri-step active">Hybrid Quantum-Classical Model</div>
                            <div className="mri-arrow">↓</div>
                            <div className="mri-step">Prediction</div>
                        </div>
                    </div>
                </div>
            </motion.div>

        </section>
    )
}

export default Hero;