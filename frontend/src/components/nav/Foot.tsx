import React from 'react';
import { NavLink } from 'react-router-dom';

const Footbar: React.FC = () => {
  return (
    <footer className="footbar-container">
        {/* Example brand or logo if desired */}
        <div className="footbar-logo">
          <NavLink to="/" className="footbar-logo-link">
            QGuideGuide
          </NavLink>
        </div>

      {/* Optionally, some copyright or tagline */}
      <div className="footbar-bottom">
        <p>&copy; {new Date().getFullYear()} QGuideGuide. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footbar;
