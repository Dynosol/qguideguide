// Prof.tsx

import React from 'react';
import { Link } from 'react-router-dom';
import { ProfessorsTable } from './ProfessorsTable';
import { DepartmentsTable } from './DepartmentsTable';
import { useProfessors } from '../../utils/professorsContext';
import '/src/assets/css/Prof.css';

const Prof: React.FC = () => {
  const { professorsData, departmentsData, isLoading } = useProfessors();

  return (
    <div className="professors-page">
      <div className="guide">
        <i>
          <Link to="/about" className="guide-link">
            Each number is calculated via empirical bayes across every course an instructor has taught based on the "Evaluate your Instructor overall" question. Department scores are naive averages.
          </Link>
        </i>
      </div>

      <div className="professors-container">
        <div className="section-left">
          <ProfessorsTable data={professorsData} isLoading={isLoading} />
        </div>

        <div className="section-right">
          <DepartmentsTable data={departmentsData} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default Prof;
