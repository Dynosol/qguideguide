// Prof.tsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProfessorsTable } from './ProfessorsTable';
import { DepartmentsTable } from './DepartmentsTable';
import { db, Professor, Department } from './db';
import { fetchProfessors, fetchDepartments } from '../../utils/api';
import '/src/assets/css/Prof.css';

const Prof: React.FC = () => {
  const [professorsData, setProfessorsData] = useState<Professor[]>([]);
  const [departmentsData, setDepartmentsData] = useState<Department[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        setIsLoading(true);

        // First try to get data from IndexedDB
        const cachedProfessors = await db.professors.toArray();
        const cachedDepartments = await db.departments.toArray();
        const metadata = await db.metadata.get('etags');
        
        // If we have cached data, show it immediately
        if (cachedProfessors.length > 0) {
          setProfessorsData(cachedProfessors);
          setIsLoading(false);
        }
        if (cachedDepartments.length > 0) {
          setDepartmentsData(cachedDepartments);
          setIsLoading(false);
        }

        // Prepare headers for conditional requests
        const headers: Record<string, string> = {};
        if (metadata) {
          if (metadata.professorsEtag) headers['If-None-Match'] = metadata.professorsEtag;
          if (metadata.departmentsEtag) headers['If-None-Match'] = metadata.departmentsEtag;
        }

        // Fetch fresh data in the background
        const [professorsResponse, departmentsResponse] = await Promise.all([
          fetchProfessors(headers),
          fetchDepartments(headers)
        ]);

        // Only update if we got new data (not 304)
        if (professorsResponse.status !== 304) {
          setProfessorsData(professorsResponse.data);
          await db.professors.clear();
          await db.professors.bulkAdd(professorsResponse.data);
        }

        if (departmentsResponse.status !== 304) {
          setDepartmentsData(departmentsResponse.data);
          await db.departments.clear();
          await db.departments.bulkAdd(departmentsResponse.data);
        }

        // Store new ETags
        await db.metadata.put({
          key: 'etags',
          value: {
            professorsEtag: professorsResponse.headers.etag,
            departmentsEtag: departmentsResponse.headers.etag,
            lastUpdate: new Date().toISOString()
          }
        });

      } catch (error) {
        console.error('Error fetching data:', error);
        // If fetch fails and we don't have cached data, show error state
        if (professorsData.length === 0 || departmentsData.length === 0) {
          // You might want to show an error message to the user here
        }
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