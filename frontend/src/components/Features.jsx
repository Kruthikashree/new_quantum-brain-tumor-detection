import { FaBrain, FaRobot, FaHospital, FaChartLine } from "react-icons/fa";
import "./Features.css";

function Features() {

    const data = [

        {
            icon: <FaBrain />,
            title: "Hybrid AI Model",
            desc: "MobileNetV2 integrated with Hybrid Quantum Neural Network."
        },

        {
            icon: <FaRobot />,
            title: "Fast Prediction",
            desc: "Predict MRI scans in just a few seconds."
        },

        {
            icon: <FaChartLine />,
            title: "93.06% Accuracy",
            desc: "High accuracy using deep learning and quantum computing."
        },

        {
            icon: <FaHospital />,
            title: "Doctor Suggestions",
            desc: "Receive recommendations for specialists and hospitals."
        }

    ];

    return (

        <section className="features">

            <h2>Why Choose Our System?</h2>

            <div className="feature-grid">

                {

                    data.map((item,index)=>(

                        <div className="card" key={index}>

                            <div className="icon">
                                {item.icon}
                            </div>

                            <h3>{item.title}</h3>

                            <p>{item.desc}</p>

                        </div>

                    ))

                }

            </div>

        </section>

    )

}

export default Features;