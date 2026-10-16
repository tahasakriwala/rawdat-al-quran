/* Rawdat service worker: app shell cached, pages network-first with an offline page, media cache-first. */
const V = 'rawdat-v2';
const SHELL = ['/', '/offline', '/static/img/crest.png', '/static/fonts/Kanz-al-Marjaan.ttf'];

self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin || u.pathname.startsWith('/portal') || u.pathname.startsWith('/api')) return;
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then(res => { const c = res.clone(); caches.open(V).then(x => x.put(r, c)); return res; })
      .catch(() => caches.match(r).then(m => m || caches.match('/offline'))));
    return;
  }
  if (u.pathname.startsWith('/static/')) {
    // CSS/JS URLs carry ?v=<mtime>, so cache-first is safe for everything under /static
    e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => {
      if (res.ok && !u.pathname.endsWith('.mp3')) { const c = res.clone(); caches.open(V).then(x => x.put(r, c)); }
      return res;
    })));
  }
});
