// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import Navbar from './components/nav/Nav.tsx';
import { StrictMode } from 'react';

// Render Navbar into its own root
const navbarRoot = document.getElementById('navbar-root');
if (navbarRoot) {
  createRoot(navbarRoot).render(
    <BrowserRouter>
        <Navbar />
    </BrowserRouter>
  );
}

// Render the main app into its own root
const appRoot = document.getElementById('root');
if (appRoot) {
  createRoot(appRoot).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}
