const config = {
  apiBaseUrl: import.meta.env.PROD 
    ? 'https://qguideguide.com'  // Production API URL (HTTPS)
    : 'http://127.0.0.1:8000',   // Development API URL (HTTP)
};

export default config;