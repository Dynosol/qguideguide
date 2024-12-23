import React from 'react';
import {
    Routes,
    Route
} from 'react-router-dom';
import Courses from './components/courses/Courses.tsx';
import About from './components/about/About.tsx';
import Contact from './components/contact/Contact.tsx';

const App: React.FC = () => (
    <Routes>
      <Route path="/" element={<Courses />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
);  

export default App;