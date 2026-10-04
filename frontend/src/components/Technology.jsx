import "./Technology.css";
import { SiPython, SiTensorflow, SiPytorch } from "react-icons/si";
import { FaAtom, FaBrain, FaCode, FaEye, FaXRay } from "react-icons/fa";

function Technology() {
    const items = [
        { icon: <SiPython />, label: "Python" },
        { icon: <SiTensorflow />, label: "TensorFlow / PyTorch" },
        { icon: <FaBrain />, label: "MobileNetV2" },
        { icon: <FaAtom />, label: "PennyLane" },
        { icon: <FaCode />, label: "Hybrid Quantum Neural Network" },
        { icon: <SiPytorch />, label: "Deep Learning" },
        { icon: <FaEye />, label: "Computer Vision" },
        { icon: <FaXRay />, label: "MRI Image Analysis" },
    ];

    return (
        <section className="technology" id="technology">
            <h2>Technology Behind the System</h2>
            <p className="subtitle">The tools and frameworks powering the pipeline</p>

            <div className="tech-grid">
                {items.map((item, i) => (
                    <div className="tech-chip" key={i}>
                        <span className="tech-icon">{item.icon}</span>
                        {item.label}
                    </div>
                ))}
            </div>
        </section>
    );
}

export default Technology;