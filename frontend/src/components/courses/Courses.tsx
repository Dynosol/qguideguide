import React from 'react';
import CoursesTable from './CoursesTable'; // Adjust the path based on your file structure
import '/src/assets/css/Courses.css';

const Courses: React.FC = () => (
    <div className="non-navbar">
        <div className="main-table">
            <CoursesTable />
        </div>
    </div>
);

export default Courses;
