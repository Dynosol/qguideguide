const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.qguideguide.com',
  apiKey: import.meta.env.VITE_API_KEY || '', // Only used once to get initial JWT tokens
};

export default config;