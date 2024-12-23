import React from 'react';
import { Link } from 'react-router-dom';
import '/src/assets/css/Nav.css'; // Import corresponding CSS for styling

const Navbar: React.FC = () => {
    return(
        <nav>
            <div className="nav-container">
                <div id="logo" className="logo">
                    <Link to="/" className="logo-link">
                        <span>QGuideGuide</span>
                    </Link>
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