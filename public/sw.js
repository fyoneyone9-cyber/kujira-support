// Service Worker - cache disabled, force reload on update
const CACHE_VERSION = 'v' + Date.now()

self.addEventListener('install', () => {
  self.skipWaiting()
})

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.claim())
      .then(() => self.clients.matchAll({ type: 'window' }))
      .then(clients => clients.forEach(c => c.navigate(c.url)))
  )
})

self.addEventListener('fetch', e => {
  e.respondWith(fetch(e.request))
})
