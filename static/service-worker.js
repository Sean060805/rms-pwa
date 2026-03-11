const CACHE_NAME = "rms-pwa-v1";
const urlsToCache = [
  "/",
  "/login",
  "/dashboard",
  "/static/css/login.css",
  "/static/css/dashboard.css",
  "/static/js/script.js",
  "/static/js/pwa.js",
  "/static/img/logo.png",
  "/static/img/icon-192.png",
  "/static/img/icon-512.png",
  "/manifest.json"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});