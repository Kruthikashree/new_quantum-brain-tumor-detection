import "./Accuracy.css";

function Accuracy(){
    return(
        <section className="accuracy" id="performance">
            <h2>Model Performance</h2>
            <p className="subtitle">Comparison of experimental results on the test dataset</p>

            <div className="accuracy-chart">
                <div className="bar-row">
                    <span className="bar-label">MobileNetV2</span>
                    <div className="bar-track">
                        <div className="bar-fill mnv2" style={{width:"89.94%"}}></div>
                    </div>
                    <span className="bar-value">89.94%</span>
                </div>

                <div className="bar-row">
                    <span className="bar-label">Hybrid Quantum AI</span>
                    <div className="bar-track">
                        <div className="bar-fill hybrid" style={{width:"93.06%"}}></div>
                    </div>
                    <span className="bar-value">93.06%</span>
                </div>
            </div>

            <p className="disclaimer">
                Performance values represent experimental model evaluation and are
                not a substitute for clinical diagnosis.
            </p>
        </section>
    )
}

export default Accuracy;