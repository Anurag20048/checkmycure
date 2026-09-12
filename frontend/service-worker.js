// Version 2 - Updated to fix caching issues
const CACHE_VERSION = 'mycure-cache-v3';

self.addEventListener("push", function (event) {
  const data = event.data.json();

  self.registration.showNotification(data.title, {
    body: data.body,
    icon: "logo.png",
    badge: "logo.png",
    vibrate: [200, 100, 200],
    tag: "health-alert"
  });
});

// Clear old caches on activation
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          return cacheName !== CACHE_VERSION;
        }).map(cacheName => {
          console.log('Deleting old cache:', cacheName);
          return caches.delete(cacheName);
        })
      );
    })
  );
});

self.addEventListener("install", e => {
  // Skip waiting to activate immediately
  self.skipWaiting();
  
  e.waitUntil(
    caches.open(CACHE_VERSION).then(cache => {
      return cache.addAll([
        "index.html",
        "chatbot.html",
        "dashboard.html",
        "style.css",
        "app.js"
      ]);
    })
  );
});

// Network-first strategy: always try network first, fall back to cache
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Update cache with fresh response
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(CACHE_VERSION).then(cache => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request);
      })
  );
});
