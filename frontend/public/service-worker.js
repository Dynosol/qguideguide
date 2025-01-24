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

// Helper function to check if URL is cacheable
const isCacheableUrl = (url) => {
  return url.startsWith('http:') || url.startsWith('https:');
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
  // Skip non-cacheable URLs (like chrome-extension://)
  if (!isCacheableUrl(event.request.url)) {
    return;
  }

  // Don't cache API requests
  if (isApiRequest(event.request)) {
    // Don't handle API requests at all, let the browser handle them normally
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

            // Only cache if URL is cacheable
            if (isCacheableUrl(event.request.url)) {
              // Clone the response
              const responseToCache = response.clone();

              caches.open(CACHE_NAME)
                .then(cache => {
                  try {
                    cache.put(event.request, responseToCache);
                  } catch (error) {
                    console.error('Error caching response:', error);
                  }
                })
                .catch(error => {
                  console.error('Error opening cache:', error);
                });
            }

            return response;
          })
          .catch(error => {
            console.error('Error fetching:', error);
            throw error;
          });
      })
  );
});
