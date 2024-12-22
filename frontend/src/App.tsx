import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Navbar from './components/nav/Nav.tsx';
import Home from './components/courses/Courses.tsx';
import About from './components/about/About.tsx';
// import Contact from '../contact/contact';

const App: React.FC = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      {/* <Route path="/contact" element={<Contact />} /> */}
    </Routes>
  </Router>
);  

export default App;