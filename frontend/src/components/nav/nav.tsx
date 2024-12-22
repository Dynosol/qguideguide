import React from 'react';
import { Link } from 'react-router-dom';
import '/src/assets/css/Nav.css'; // Import corresponding CSS for styling

const Navbar: React.FC = () => {
    console.log('Navbar component rendering');
    return(
        <nav>
            <div className="nav-container">
                <div id="logo" className="logo" data-url="{% url 'courses_list' %}">
                    <span>QGuideGuide</span>
                </div>
                <ul className="nav-links">
                    <li className="navbar-item">
                        <Link to="/" className="navbar-link">Courses</Link>
                    </li>
                    <li className="navbar-item">
                        <Link to="/professors" className="navbar-link">Professor Rankings</Link>
                    </li>
                    <li className="navbar-item">
                        <Link to='/about' className="navbar-link">About</Link>
                    </li>
                    <li className="navbar-item">
                        <Link to="/contact" className="navbar-link">Contact</Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;