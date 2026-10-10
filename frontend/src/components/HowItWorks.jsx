import "./HowItWorks.css";
import { FaUpload, FaBrain, FaAtom, FaNotesMedical } from "react-icons/fa";

function HowItWorks() {

  const steps = [
    { icon: <FaUpload />, title: "Upload MRI", desc: "Upload a brain MRI image." },
    { icon: <FaBrain />, title: "Feature Extraction", desc: "MobileNetV2 extracts the relevant visual features." },
    { icon: <FaAtom />, title: "Hybrid Quantum-Classical Model", desc: "The extracted features are processed through the implemented hybrid model." },
    { icon: <FaNotesMedical />, title: "Prediction & Explanation", desc: "The system displays the predicted tumor class with a Grad-CAM style explanation." }
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
          </div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;