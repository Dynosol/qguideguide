const config = {
  apiBaseUrl: import.meta.env.PROD 
    ? 'https://api.qguideguide.com'  // Production API URL
    : 'http://localhost:8000',        // Development API URL
};

export default config; 