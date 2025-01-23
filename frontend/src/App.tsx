// App.tsx (simplified example)
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/Nav/Nav';
import Courses from './components/courses/Courses';
import About from './components/about/About';
import Prof from './components/professors/Prof';
import { ThemeContextProvider } from './utils/themeHelper';
import { ProfessorsProvider } from './utils/professorsContext';

const App: React.FC = () => {
  return (
    <ThemeContextProvider>
      <ProfessorsProvider>
        <Router>
          <Navbar />
            <Routes>
              <Route path="/" element={<Courses />} />
              <Route path="/professors" element={<Prof />}/>
              <Route path="/about" element={<About />} />
            </Routes>
        </Router>
      </ProfessorsProvider>
    </ThemeContextProvider>
  );
};

export default App;
