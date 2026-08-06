import "./HowItWorks.css";
import { FaUpload, FaBrain, FaAtom, FaNotesMedical } from "react-icons/fa";

function HowItWorks() {

  const steps = [
    {
      icon: <FaUpload />,
      title: "Upload MRI",
      desc: "Upload a brain MRI scan in JPG, JPEG, or PNG format."
    },
    {
      icon: <FaBrain />,
      title: "Feature Extraction",
      desc: "MobileNetV2 extracts high-level image features from the MRI."
    },
    {
      icon: <FaAtom />,
      title: "Hybrid Quantum AI",
      desc: "A Hybrid Quantum Neural Network classifies the extracted features."
    },
    {
      icon: <FaNotesMedical />,
      title: "Prediction",
      desc: "The system predicts the tumor class with confidence and suggestions."
    }
  ];

  return (
    <section className="workflow">

      <h2>How Our AI Works</h2>

      <div className="workflow-container">

        {steps.map((step, index) => (

          <div className="workflow-card" key={index}>

            <div className="workflow-icon">
              {step.icon}
            </div>

            <h3>{step.title}</h3>

            <p>{step.desc}</p>

          </div>

        ))}

      </div>

    </section>
  );

}

export default HowItWorks;