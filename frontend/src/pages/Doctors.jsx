import { useState } from "react";
import "./Doctors.css";

const PHYSICIANS = [
  {
    name: "Dr. Anita Rao",
    specialty: "Neuro-Oncology",
    hospital: "City General Hospital",
    availability: "Mon-Fri, 9 AM - 4 PM"
  },
  {
    name: "Dr. Suresh Menon",
    specialty: "Neurosurgery",
    hospital: "St. Xavier's Medical Center",
    availability: "Mon-Sat, 10 AM - 5 PM"
  },
  {
    name: "Dr. Kavya Iyer",
    specialty: "Endocrinology",
    hospital: "Metro Health Institute",
    availability: "Tue-Sat, 9 AM - 3 PM"
  },
  {
    name: "Dr. Ravi Patel",
    specialty: "Radiology",
    hospital: "City General Hospital",
    availability: "Mon-Fri, 8 AM - 6 PM"
  }
];

function Doctors() {
  const [routedTo, setRoutedTo] = useState(null);

  const handleRoute = (name) => {
    setRoutedTo(name);
    setTimeout(() => setRoutedTo(null), 3000);
  };

  return (
    <div className="doctors-page">
      <div className="doctors-header">
        <h1>Physician Directory</h1>
        <p>Route AI classification reports to the appropriate treating physician.</p>
      </div>

      <div className="doctors-list">
        {PHYSICIANS.map((doc, index) => (
          <div className="doctor-card" key={index}>
            <div className="doctor-info">
              <h3>{doc.name}</h3>
              <p className="doctor-specialty">{doc.specialty}</p>
              <p className="doctor-detail">{doc.hospital}</p>
              <p className="doctor-detail">{doc.availability}</p>
            </div>
            <button
              className="route-btn"
              onClick={() => handleRoute(doc.name)}
            >
              Route Report
            </button>
          </div>
        ))}
      </div>

      {routedTo && (
        <div className="route-toast">
          Report routed to {routedTo}
        </div>
      )}
    </div>
  );
}

export default Doctors;
