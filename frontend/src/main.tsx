import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.tsx';
import Navbar from './components/nav/Nav.tsx';

const rootElement = document.getElementById('root');
if (rootElement) {
    createRoot(rootElement).render(
        <BrowserRouter>
            <Navbar />
            <App />
        </BrowserRouter>
    );
}
