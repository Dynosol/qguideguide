import React, { useState, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
import '../../assets/css/Nav.css';
import { styled } from '@mui/material/styles';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch, { SwitchProps } from '@mui/material/Switch';
import { useThemeContext } from '../../utils/themeHelper'; // <--- import context
import { colorPalettes } from '../../utils/colors';

/**
 * We set the switch dimensions using vh units so it scales with the navbar (4vh tall).
 * The original pixel-based ratio was ~42px wide x 26px high => 1.615:1. 
 * This snippet keeps that ratio while shrinking or expanding if the navbar height changes.
 */
const IOSSwitch = styled((props: SwitchProps) => (
  <Switch focusVisibleClassName=".Mui-focusVisible" disableRipple {...props} />
))(({ theme }) => ({
  // Switch overall dimensions (scaled to fit inside a 4vh navbar).
  // Feel free to adjust these as desired for your layout.
  width: '4.2vh',   // (26px->2.6vh) * (42/26) ~ 4.2vh
  height: '2.6vh',  // scaled from the original 26px height
  padding: 0,
  '& .MuiSwitch-switchBase': {
    padding: 0,
    // The original had margin: 2px => ~ 2/26 => 0.0769 => ~0.2vh
    margin: '0.2vh',
    transitionDuration: '300ms',
    '&.Mui-checked': {
      // The original transform was 16px, which is 42 - 26 = 16 => ~1.6vh 
      // (4.2vh - 2.6vh = 1.6vh).
      transform: 'translateX(1.6vh)',
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
    // The thumb was originally 22px, close to 85% of the 26px height => 2.2vh
    boxSizing: 'border-box',
    width: '2.2vh',
    height: '2.2vh',
  },
  '& .MuiSwitch-track': {
    // The track radius was half its height => 13px (for 26px). Now it's half of 2.6vh => 1.3vh
    borderRadius: '1.3vh',
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
  const navRef = useRef<HTMLElement>(null);

  const isDarkMode = mode === 'dark';

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
      root.classList.add('dark');
    } else {
      document.body.classList.remove('dark-mode');
      root.classList.remove('dark');
    }
  }, [isDarkMode]);

  const handleThemeToggle = (event: React.ChangeEvent<HTMLInputElement>) => {
    toggleMode(event.target.checked); // direct context call
  };

  const toggleMenu = () => {
    setIsMenuOpen((prev) => !prev);
  };

  // Mouse move handler (for glow effect)
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
              onClick={() => setIsMenuOpen(false)}
            >
              Course Compare Tool
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
              Professor Scores
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
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
