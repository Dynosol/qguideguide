import { createRoot } from 'react-dom/client';
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";
import App from './App.tsx';

// Initialize Sentry
// Note: Replace 'YOUR_DSN' with your actual Sentry DSN
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN || 'YOUR_DSN',
  integrations: [new BrowserTracing()],
  tracesSampleRate: 1.0,
  enabled: import.meta.env.PROD, // Only enable in production
});

const rootElement = document.getElementById('root');
if (rootElement) {
    createRoot(rootElement).render(
        <App />
    );
}

// Register service worker
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('SW registered:', registration);
      })
      .catch(error => {
        console.log('SW registration failed:', error);
      });
  });
}
