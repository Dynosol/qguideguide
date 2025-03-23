// App.tsx (simplified example)
import React, { Suspense, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';

import Navbar from './components/nav/Nav';
import { ThemeContextProvider } from './utils/themeHelper';
import ErrorBoundary from './components/ErrorBoundary';
import { initGA, pageView } from './utils/analytics';

// Lazy load components
const Courses = React.lazy(() => import('./components/courses/Courses'));
const About = React.lazy(() => import('./components/about/About'));
const Prof = React.lazy(() => import('./components/professors/Prof'));

// Track page views component
const RouteTracker = () => {
  const location = useLocation();
  
  useEffect(() => {
    pageView(location.pathname + location.search);
  }, [location]);
  
  return null;
};

const App: React.FC = () => {
  useEffect(() => {
    // Initialize Google Analytics with your tracking ID
    const trackingId = import.meta.env.VITE_GA_TRACKING_ID as string;
    if (trackingId) {
      initGA(trackingId);
    }
  }, []);

  return (
    <ErrorBoundary>
      <ThemeContextProvider>
          <Router>
            <RouteTracker />
            <Navbar />
            <Suspense fallback={<div>Loading...</div>}>
              <Routes>
                <Route path="/" element={<Courses />} />
                <Route path="/professors" element={<Prof />}/>
                <Route path="/about" element={<About />} />
              </Routes>
            </Suspense>
          </Router>
      </ThemeContextProvider>
    </ErrorBoundary>
  );
};

export default App;
