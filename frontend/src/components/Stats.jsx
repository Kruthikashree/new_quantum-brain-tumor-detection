import "./Stats.css";
import { FaAtom, FaMicrochip, FaImages, FaLayerGroup } from "react-icons/fa";

function Stats(){
    const items = [
        { icon: <FaAtom />, value: "93.06%", label: "Hybrid Quantum AI — Model Accuracy" },
        { icon: <FaMicrochip />, value: "89.94%", label: "MobileNetV2 — Model Accuracy" },
        { icon: <FaImages />, value: "7200+", label: "MRI Images (Test Dataset)" },
        { icon: <FaLayerGroup />, value: "4", label: "Tumor Classes" },
    ];

    return (
        <section className="stats-section" id="performance-highlights">
            <h2>Performance Highlights</h2>
            <p className="subtitle">Test Dataset Accuracy across both models</p>

            <div className="stats">
                {items.map((item, i) => (
                    <div className="stat-card" key={i}>
                        <div className="stat-icon">{item.icon}</div>
                        <h1>{item.value}</h1>
                        <p>{item.label}</p>
                    </div>
                ))}
            </div>
        </section>
    )
}

export default Stats;