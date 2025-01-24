const CACHE_NAME = 'qguideguide-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/favicon-16x16.png',
  '/favicon-32x32.png',
  '/apple-touch-icon.png'
];

// Helper function to determine if a request is an API call
const isApiRequest = (request) => {
  return request.url.includes('/api/');
};

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        // Only cache static assets, not API requests
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Error during service worker installation:', error);
      })
  );
});

self.addEventListener('fetch', event => {
  // Don't cache API requests
  if (isApiRequest(event.request)) {
    event.respondWith(fetch(event.request));
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }

        return fetch(event.request)
          .then(response => {
            // Don't cache non-successful responses or non-GET requests
            if (!response || response.status !== 200 || response.type !== 'basic' || event.request.method !== 'GET') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              })
              .catch(error => {
                console.error('Error caching response:', error);
              });

            return response;
          })
          .catch(error => {
            console.error('Error fetching:', error);
            throw error;
          });
      })
  );
});
