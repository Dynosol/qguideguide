// App.tsx (simplified example)
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/nav/Nav.tsx';
import { ThemeContextProvider } from './utils/themeHelper';
import { ProfessorsProvider } from './utils/professorsContext';
import Courses from './components/courses/Courses.tsx';
import About from './components/about/About.tsx';
import Prof from './components/professors/Prof.tsx'
  

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
