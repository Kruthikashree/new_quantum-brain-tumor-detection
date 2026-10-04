import "./HowItWorks.css";
import { FaUpload, FaBrain, FaAtom, FaNotesMedical } from "react-icons/fa";

function HowItWorks() {

  const steps = [
    { icon: <FaUpload />, title: "Upload MRI", desc: "Upload a brain MRI image." },
    { icon: <FaBrain />, title: "Feature Extraction", desc: "MobileNetV2 extracts important visual features." },
    { icon: <FaAtom />, title: "Hybrid Quantum AI", desc: "The extracted features are processed by the hybrid quantum-classical model." },
    { icon: <FaNotesMedical />, title: "Prediction", desc: "The system generates the predicted tumor class and confidence information." }
  ];

  return (
    <section className="workflow" id="how-it-works">
      <h2>From MRI Scan to AI-Assisted Prediction</h2>
      <p className="subtitle">Four stages transform an MRI image into a model prediction</p>

      <div className="workflow-container">
        {steps.map((step, index) => (
          <div className="workflow-card" key={index}>
            <span className="workflow-num">0{index + 1}</span>
            <div className="workflow-icon">{step.icon}</div>
            <h3>{step.title}</h3>
            <p>{step.desc}</p>
            {index < steps.length - 1 && <div className="workflow-connector"><span></span></div>}
          </div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;