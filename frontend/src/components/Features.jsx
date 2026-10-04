import { FaBrain, FaBolt, FaLayerGroup, FaClipboardCheck } from "react-icons/fa";
import "./Features.css";

function Features() {

    const data = [
        { num: "01", icon: <FaBrain />, title: "Hybrid AI Model", desc: "MobileNetV2 feature extraction combined with a hybrid quantum neural network." },
        { num: "02", icon: <FaBolt />, title: "Fast Analysis", desc: "Efficient processing of MRI images for rapid model inference." },
        { num: "03", icon: <FaLayerGroup />, title: "Multi-Class Detection", desc: "Classification across four brain tumor categories." },
        { num: "04", icon: <FaClipboardCheck />, title: "Decision Support", desc: "Structured prediction information designed to support professional review." },
    ];

    return (
        <section className="features">
            <h2>Intelligent MRI Analysis, Built for Healthcare</h2>
            <p className="subtitle">Engineered for accuracy, speed, and clinical trust</p>

            <div className="feature-grid">
                {data.map((item, index) => (
                    <div className="card" key={index}>
                        <span className="card-num">{item.num}</span>
                        <div className="icon">{item.icon}</div>
                        <h3>{item.title}</h3>
                        <p>{item.desc}</p>
                    </div>
                ))}
            </div>
        </section>
    )
}

export default Features;