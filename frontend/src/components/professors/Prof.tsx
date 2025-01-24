// Prof.tsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { ProfessorsTable } from './ProfessorsTable';
import { DepartmentsTable } from './DepartmentsTable';
import { db, Professor, Department } from './db';
import config from '../../config';
import api from '../../utils/api'; // Update the import path to point to utils/api
import '/src/assets/css/Prof.css';

const Prof: React.FC = () => {
  const [professorsData, setProfessorsData] = useState<Professor[]>([]);
  const [departmentsData, setDepartmentsData] = useState<Department[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        // Fetch both datasets in parallel
        const [localProfessors, localDepartments] = await Promise.all([
          db.professors.toArray(),
          db.departments.toArray()
        ]);

        const lastUpdateTime = await db.metadata.get('lastUpdate');

        if (localProfessors.length > 0 && localDepartments.length > 0 && lastUpdateTime) {
          // Check if server data has been updated
          const response = await api.head('/api/professors/');
          const serverLastModified = response.headers['last-modified'];

          if (serverLastModified && new Date(serverLastModified) <= new Date(lastUpdateTime.value)) {
            // Use cached data if server hasn't updated
            setProfessorsData(localProfessors);
            setDepartmentsData(localDepartments);
            setIsLoading(false);
            return;
          }
        }

        // Fetch new data in parallel if cache is invalid or empty
        const [professorsResponse, departmentsResponse] = await Promise.all([
          api.get('/api/professors/'),
          api.get('/api/departments/')
        ]);

        const currentTime = new Date().toISOString();
        
        // Extract data arrays from response
        const professors = Array.isArray(professorsResponse.data) ? professorsResponse.data : 
                         (professorsResponse.data.professors ? [professorsResponse.data.professors] : []);
        const departments = Array.isArray(departmentsResponse.data) ? departmentsResponse.data :
                          (departmentsResponse.data.departments ? [departmentsResponse.data.departments] : []);

        // Store all data in parallel
        await db.transaction('rw', db.professors, db.departments, db.metadata, async () => {
          await Promise.all([
            db.professors.clear(),
            db.departments.clear(),
            professors.length > 0 && db.professors.bulkAdd(professors),
            departments.length > 0 && db.departments.bulkAdd(departments),
            db.metadata.put({ key: 'lastUpdate', value: currentTime })
          ]);
        });

        setProfessorsData(professors);
        setDepartmentsData(departments);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAllData();
  }, []);

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