import React, { useState, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
import '/src/assets/css/Nav.css';
import { styled } from '@mui/material/styles';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch, { SwitchProps } from '@mui/material/Switch';
import { useThemeContext } from '../../utils/themeHelper'; // <--- import context
import { colorPalettes } from '../../utils/colors';

const IOSSwitch = styled((props: SwitchProps) => (
  <Switch focusVisibleClassName=".Mui-focusVisible" disableRipple {...props} />
))(({ theme }) => ({
  width: 42,
  height: 26,
  padding: 0,
  '& .MuiSwitch-switchBase': {
    padding: 0,
    margin: 2,
    transitionDuration: '300ms',
    '&.Mui-checked': {
      transform: 'translateX(16px)',
      color: '#fff',
      '& + .MuiSwitch-track': {
        backgroundColor: colorPalettes.light.harvard,
        opacity: 1,
        border: 0,
      },
      '&.Mui-disabled + .MuiSwitch-track': {
        opacity: 0.5,
      },
    },
    '&.Mui-focusVisible .MuiSwitch-thumb': {
      color: '#33cf4d',
      border: '6px solid #fff',
    },
    '&.Mui-disabled .MuiSwitch-thumb': {
      color: theme.palette.grey[100],
    },
    '&.Mui-disabled + .MuiSwitch-track': {
      opacity: 0.7,
    },
  },
  '& .MuiSwitch-thumb': {
    boxSizing: 'border-box',
    width: 22,
    height: 22,
  },
  '& .MuiSwitch-track': {
    borderRadius: 13,
    backgroundColor: '#E9E9EA',
    opacity: 1,
    transition: theme.transitions.create(['background-color'], {
      duration: 500,
    }),
  },
}));

const Navbar: React.FC = () => {
  const { mode, toggleMode } = useThemeContext();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navRef = useRef<HTMLElement>(null); // Add this line

  const isDarkMode = mode === 'dark';

  useEffect(() => {
    // apply body class for dark mode
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  const handleThemeToggle = (event: React.ChangeEvent<HTMLInputElement>) => {
    toggleMode(event.target.checked); // direct context call
  };

  const toggleMenu = () => {
    setIsMenuOpen((prev) => !prev);
  };

  // Mouse move handler
  const handleMouseMove = (e: React.MouseEvent) => {
    if (navRef.current) {
      const rect = navRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      navRef.current.style.setProperty('--mouse-x', `${x}px`);
      navRef.current.style.setProperty('--mouse-y', `${y}px`);
    }
  };

  return (
    <nav ref={navRef} onMouseMove={handleMouseMove}>
      <div className="nav-container">
        <div id="logo" className="logo">
          <NavLink to="/" className="logo-link">
            <span>QGuideGuide</span>
          </NavLink>
        </div>

        <div className="toggle-modes">
          <FormControlLabel
            label={isDarkMode ? 'Dark Mode' : 'Light Mode'}
            control={
              <IOSSwitch
                sx={{ m: 1 }}
                checked={isDarkMode}
                onChange={handleThemeToggle}
              />
            }
          />
        </div>

        <button
          className={`menu-toggle ${isMenuOpen ? 'open' : ''}`}
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`nav-links ${isMenuOpen ? 'open' : ''}`}>
          <li className="navbar-item">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                isActive ? 'navbar-link active' : 'navbar-link'
              }
              onClick={() => setIsMenuOpen(false)} // Close menu on link click
            >
              Course Search Tool
            </NavLink>
          </li>
          <li className="navbar-item">
            <NavLink
              to="/professors"
              className={({ isActive }) =>
                isActive ? 'navbar-link active' : 'navbar-link'
              }
              onClick={() => setIsMenuOpen(false)}
            >
              Professor Rankings
            </NavLink>
          </li>
          <li className="navbar-item">
            <NavLink
              to="/about"
              className={({ isActive }) =>
                isActive ? 'navbar-link active' : 'navbar-link'
              }
              onClick={() => setIsMenuOpen(false)}
            >
              About / Help
            </NavLink>
          </li>
          <li className="navbar-item">
            <NavLink
              to="/contact"
              className={({ isActive }) =>
                isActive ? 'navbar-link active' : 'navbar-link'
              }
              onClick={() => setIsMenuOpen(false)}
            >
              Contact
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
