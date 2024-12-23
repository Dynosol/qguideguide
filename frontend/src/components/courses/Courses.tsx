import React from 'react';
import CoursesTable from './CoursesTable'; // Adjust the path based on your file structure

const Courses: React.FC = () => (
    <div className="non-navbar">
        <h1 className="title">Courses</h1>
        <p className="description">Welcome to the courses page!</p>
        
        {/* Integrate the table */}
        <div style={{ marginTop: '20px' }}>
            <CoursesTable />
        </div>
    </div>
);

export default Courses;
