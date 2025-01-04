// Prof.tsx

import React from 'react';
import { Link } from 'react-router-dom';
import { ProfessorsTable } from './ProfessorsTable';
import { DepartmentsTable } from './DepartmentsTable';
import '/src/assets/css/Prof.css';

const Prof: React.FC = () => {
  return (
    <div className="professors-page">
      {/* Top Guide Section */}
      <div className="guide">
        <i>
          <Link to="/about" className="guide-link">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Each number is calculated via empirical bayes across every course an instructor has taught based on the "Evaluate your Instructor overall" question. Department scores are naive averages.
          </Link>
        </i>
      </div>

      {/* Main Content Section */}
      <div className="professors-container">

        <div className="section-left">
          <ProfessorsTable />
        </div>

        <div className="section-middle">
          <DepartmentsTable />
        </div>
        
        <div className="section-right">
          <h2>Section Right</h2>
          {/* Add content for right section */}
        </div>
      </div>
    </div>
  );
};

export default Prof;
