import "./SectionNav.css";

function SectionNav() {
    return (
        <nav className="section-nav">
            <a href="#features">What It Does</a>
            <span className="section-nav-dot">•</span>
            <a href="#how-it-works">The Pipeline</a>
            <span className="section-nav-dot">•</span>
            <a href="#healthcare">For Clinicians</a>
        </nav>
    );
}

export default SectionNav;