import "./Hero.css";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

function Hero() {

    return (

        <section className="hero">

            <motion.div
                className="hero-left"
                initial={{x:-100,opacity:0}}
                animate={{x:0,opacity:1}}
                transition={{duration:1}}
            >

                <h1>

                    Quantum Enhanced
                    <br/>
                    Brain Tumor Detection

                </h1>

                <p>

                    A laboratory tool for uploading MRI scans and generating
                    AI-assisted classification reports, powered by MobileNetV2
                    and a Hybrid Quantum Neural Network, for physicians to
                    review when planning patient treatment.

                </p>

                <div className="hero-buttons">

                    <Link to="/upload">
                        <button className="primary-btn">

                            Upload MRI

                        </button>
                    </Link>

                    <Link to="/signup">

                        <button className="secondary-btn">

                            Get Started

                        </button>

                    </Link>

                </div>

            </motion.div>

            <motion.div

                className="hero-right"

                initial={{x:100,opacity:0}}

                animate={{x:0,opacity:1}}

                transition={{duration:1}}

            >

                <img

                    src="https://images.unsplash.com/photo-1579154204601-01588f351e67?w=700"

                    alt="AI"

                />

            </motion.div>

        </section>

    )

}

export default Hero;
