import { FaBrain, FaXRay, FaLayerGroup, FaEye } from "react-icons/fa";
import "./Features.css";

function Features() {

    const data = [
        { num: "01", icon: <FaBrain />, title: "Hybrid AI Model", desc: "MobileNetV2 feature extraction combined with a hybrid quantum-classical neural network for classification." },
        { num: "02", icon: <FaXRay />, title: "MRI Image Analysis", desc: "Upload a brain MRI scan for automated, AI-assisted analysis within the application." },
        { num: "03", icon: <FaLayerGroup />, title: "Four-Class Classification", desc: "Distinguishes between Glioma, Meningioma, Pituitary tumor, and No Tumor." },
        { num: "04", icon: <FaEye />, title: "Explainable AI with Grad-CAM", desc: "A Grad-CAM style heatmap highlights the regions that most influenced each prediction." },
    ];

    return (
        <section className="features" id="features">
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