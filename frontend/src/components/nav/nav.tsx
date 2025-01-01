import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
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
        // ...theme.applyStyles('dark', {
        //   backgroundColor: '#2ECA45',
        // }),
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
      // ...theme.applyStyles('dark', {
      //   color: theme.palette.grey[600],
      // }),
    },
    '&.Mui-disabled + .MuiSwitch-track': {
      opacity: 0.7,
      // ...theme.applyStyles('dark', {
      //   opacity: 0.3,
      // }),
    },
  },
  '& .MuiSwitch-thumb': {
    boxSizing: 'border-box',
    width: 22,
    height: 22,
  },
  '& .MuiSwitch-track': {
    borderRadius: 26 / 2,
    backgroundColor: '#E9E9EA',
    opacity: 1,
    transition: theme.transitions.create(['background-color'], {
      duration: 500,
    }),
    // ...theme.applyStyles('dark', {
    //   backgroundColor: '#39393D',
    // }),
  },
}));

const Navbar: React.FC = () => {
  const { mode, toggleMode } = useThemeContext(); // get from context
  const [isMenuOpen, setIsMenuOpen] = useState(false);

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


  return (
    <nav>
      <div className="nav-container">
        <div id="logo" className="logo">
          <Link to="/" className="logo-link">
            <span>QGuideGuide</span>
          </Link>
        </div>

        <div className="toggle-modes">
        <FormControlLabel
          label={isDarkMode ? 'Dark Mode' : 'Light Mode'}
          control={
            <IOSSwitch
              sx={{m: 1}}
              checked={isDarkMode}
              onChange={handleThemeToggle}
            />
          }
        />
        </div>

        <button
          className={`menu-toggle ${isMenuOpen ? 'open' : ''}`}
          onClick={toggleMenu}
        >
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
