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
        setIsLoading(true);
        
        // Always fetch fresh data in production to avoid caching issues
        if (import.meta.env.PROD) {
          const [professorsResponse, departmentsResponse] = await Promise.all([
            api.get('/api/professors/'),
            api.get('/api/departments/')
          ]);
          
          setProfessorsData(professorsResponse.data);
          setDepartmentsData(departmentsResponse.data);
          
          // Update IndexedDB cache
          await db.professors.clear();
          await db.departments.clear();
          await db.professors.bulkAdd(professorsResponse.data);
          await db.departments.bulkAdd(departmentsResponse.data);
          await db.metadata.put({ key: 'lastUpdate', value: new Date().toISOString() });
        } else {
          // In development, use the existing caching strategy
          const [localProfessors, localDepartments] = await Promise.all([
            db.professors.toArray(),
            db.departments.toArray()
          ]);

          const lastUpdateTime = await db.metadata.get('lastUpdate');

          if (localProfessors.length > 0 && localDepartments.length > 0 && lastUpdateTime) {
            try {
              const response = await api.get('/api/professors/');
              setProfessorsData(response.data);
              setDepartmentsData(localDepartments);
              
              // Update cache
              await db.professors.clear();
              await db.professors.bulkAdd(response.data);
              await db.metadata.put({ key: 'lastUpdate', value: new Date().toISOString() });
            } catch (error) {
              console.warn('Failed to fetch fresh data, using cache:', error);
              setProfessorsData(localProfessors);
              setDepartmentsData(localDepartments);
            }
          } else {
            // No cache, fetch fresh data
            const [professorsResponse, departmentsResponse] = await Promise.all([
              api.get('/api/professors/'),
              api.get('/api/departments/')
            ]);
            
            setProfessorsData(professorsResponse.data);
            setDepartmentsData(departmentsResponse.data);
            
            // Update cache
            await db.professors.clear();
            await db.departments.clear();
            await db.professors.bulkAdd(professorsResponse.data);
            await db.departments.bulkAdd(departmentsResponse.data);
            await db.metadata.put({ key: 'lastUpdate', value: new Date().toISOString() });
          }
        }
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