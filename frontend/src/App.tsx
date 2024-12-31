// App.tsx (simplified example)
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/nav/Nav';
import { ThemeContextProvider } from './utils/themeHelper';
import Courses from './components/courses/Courses.tsx';
import About from './components/about/About.tsx';
import Contact from './components/contact/Contact.tsx';
  

const App: React.FC = () => {
  return (
    <ThemeContextProvider>
      <Router>
        <Navbar />
          <Routes>
            <Route path="/" element={<Courses />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
      </Router>
    </ThemeContextProvider>
  );
};

export default App;
