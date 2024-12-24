import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '/src/assets/css/Nav.css';

const Navbar: React.FC = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <nav>
            <div className="nav-container">
                <div id="logo" className="logo">
                    <Link to="/" className="logo-link">
                        <span>QGuideGuide</span>
                    </Link>
                </div>
                <button className={`menu-toggle ${isMenuOpen ? 'open' : ''}`} onClick={toggleMenu}>
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
                <ul className={`nav-links ${isMenuOpen ? 'open' : ''}`}>
                    <li className="navbar-item">
                        <Link to="/" className="navbar-link">Course Search Tool</Link>
                    </li>
                    <li className="navbar-item">
                        <Link to="/professors" className="navbar-link">Professor Rankings</Link>
                    </li>
                    <li className="navbar-item">
                        <Link to="/about" className="navbar-link">About / Help</Link>
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
