const config = {
  apiBaseUrl: import.meta.env.PROD 
    ? 'https://qguideguide.onrender.com'  // Production API URL
    : 'http://127.0.0.1:8000',   // Development API URL (HTTP)
};

export default config;