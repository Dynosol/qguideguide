import { createRoot } from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');
if (rootElement) {
    createRoot(rootElement).render(
        <App />
    );
}

// Service worker registration temporarily disabled due to performance concerns
// if ('serviceWorker' in navigator && import.meta.env.PROD) {
//   window.addEventListener('load', () => {
//     navigator.serviceWorker.register('/service-worker.js')
//       .then(registration => {
//         console.log('SW registered:', registration);
//       })
//       .catch(error => {
//         console.log('SW registration failed:', error);
//       });
//   });
// }
