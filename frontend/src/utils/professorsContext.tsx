import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { db, Professor, Department } from '../components/professors/db';
import config from '../config'; // Assuming config is imported from a separate file

interface ProfessorsContextType {
  professorsData: Professor[];
  departmentsData: Department[];
  isLoading: boolean;
}

const ProfessorsContext = createContext<ProfessorsContextType>({
  professorsData: [],
  departmentsData: [],
  isLoading: true,
});

export const useProfessors = () => useContext(ProfessorsContext);

export const ProfessorsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
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
          const response = await axios.head(`${config.apiBaseUrl}/api/professors/professors/`);
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
          axios.get<Professor[]>(`${config.apiBaseUrl}/api/professors/professors/`),
          axios.get<Department[]>(`${config.apiBaseUrl}/api/professors/departments/`)
        ]);

        const currentTime = new Date().toISOString();

        // Store all data in parallel
        await db.transaction('rw', db.professors, db.departments, db.metadata, async () => {
          await Promise.all([
            db.professors.clear(),
            db.departments.clear(),
            db.professors.bulkAdd(professorsResponse.data),
            db.departments.bulkAdd(departmentsResponse.data),
            db.metadata.put({ key: 'lastUpdate', value: currentTime })
          ]);
        });

        setProfessorsData(professorsResponse.data);
        setDepartmentsData(departmentsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAllData();
  }, []);

  return (
    <ProfessorsContext.Provider value={{ professorsData, departmentsData, isLoading }}>
      {children}
    </ProfessorsContext.Provider>
  );
}; 