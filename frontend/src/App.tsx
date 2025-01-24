// App.tsx (simplified example)
import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/nav/Nav';
import { ThemeContextProvider } from './utils/themeHelper';
import { ProfessorsProvider } from './utils/professorsContext';
import ErrorBoundary from './components/ErrorBoundary';

// Lazy load components
const Courses = React.lazy(() => import('./components/courses/Courses'));
const About = React.lazy(() => import('./components/about/About'));
const Prof = React.lazy(() => import('./components/professors/Prof'));

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <ThemeContextProvider>
        <ProfessorsProvider>
          <Router>
            <Navbar />
            <Suspense fallback={<div>Loading...</div>}>
              <Routes>
                <Route path="/" element={<Courses />} />
                <Route path="/professors" element={<Prof />}/>
                <Route path="/about" element={<About />} />
              </Routes>
            </Suspense>
          </Router>
        </ProfessorsProvider>
      </ThemeContextProvider>
    </ErrorBoundary>
  );
};

export default App;
