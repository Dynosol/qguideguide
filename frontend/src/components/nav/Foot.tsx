import React from 'react';
import { Link } from 'react-router-dom';
import '/src/assets/css/Footbar.css';

const Footbar: React.FC = () => {
  return (
    <footer className="footbar-container">
        {/* Example brand or logo if desired */}
        <div className="footbar-logo">
          <Link to="/" className="footbar-logo-link">
            QGuideGuide
          </Link>
        </div>

      {/* Optionally, some copyright or tagline */}
      <div className="footbar-bottom">
        <p>&copy; {new Date().getFullYear()} QGuideGuide. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footbar;
