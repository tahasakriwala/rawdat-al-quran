/* Rawdat — Jaguar Type 01 · Fatemi edition. Vanilla JS, no dependencies. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const html = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} },
  };

  /* ---------- loader ---------- */
  const loader = $('#loader');
  const hideLoader = () => { loader && loader.classList.add('done'); try { sessionStorage.setItem('rq-seen', 1); } catch (e) {} };
  if (html.classList.contains('seen')) { loader && loader.remove(); }
  else { window.addEventListener('load', () => setTimeout(hideLoader, 450)); setTimeout(hideLoader, 2600); }

  /* ---------- header: solid after the hero, hides on scroll down ---------- */
  const hdr = $('#hdr'), bar = $('#nav-bar');
  let lastY = scrollY;
  const onHeader = () => {
    const y = scrollY;
    const heroEnd = $('.hero') ? $('.hero').offsetHeight - innerHeight * 1.05 : 20;
    hdr.classList.toggle('solid', y > heroEnd);
    hdr.classList.toggle('hide', y > lastY && y > 400 && !document.body.classList.contains('menu-open'));
    lastY = y;
    const h = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = h > 0 ? (100 * y / h) + '%' : 0;
  };

  /* ---------- menu sheet & look popover ---------- */
  const sheet = $('#sheet'), look = $('#look');
  $$('[data-menu]').forEach(b => b.addEventListener('click', () => {
    const open = !sheet.classList.contains('open');
    sheet.classList.toggle('open', open); sheet.setAttribute('aria-hidden', !open);
    document.body.classList.toggle('menu-open', open); document.body.style.overflow = open ? 'hidden' : '';
  }));
  $$('[data-look]').forEach(b => b.addEventListener('click', e => { e.stopPropagation(); look.classList.toggle('open'); }));
  document.addEventListener('click', e => { if (look && !look.contains(e.target)) look.classList.remove('open'); });
  const syncLook = () => {
    $$('[data-theme-set]').forEach(d => d.classList.toggle('on', d.dataset.themeSet === (html.dataset.theme || 'rawdat')));
    const m = store.get('rq-mode') || 'auto';
    $$('[data-mode-set]').forEach(d => d.classList.toggle('on', d.dataset.modeSet === m));
  };
  $$('[data-theme-set]').forEach(d => d.addEventListener('click', () => { html.dataset.theme = d.dataset.themeSet; store.set('rq-theme', d.dataset.themeSet); syncLook(); }));
  $$('[data-mode-set]').forEach(d => d.addEventListener('click', () => {
    const m = d.dataset.modeSet; store.set('rq-mode', m);
    const dark = m === 'dark' || (m === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
    if (dark) html.dataset.mode = 'dark'; else delete html.dataset.mode; syncLook();
  }));
  syncLook();

  /* ---------- reveal on view ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  $$('[data-reveal], .fan').forEach(el => io.observe(el));

  /* ---------- gold-leaf counters ---------- */
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, t0 = performance.now(), dur = reduce ? 1 : 2200;
    const tick = t => { const k = clamp((t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - k, 4))); if (k < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  }), { threshold: .4 });
  $$('[data-count]').forEach(el => cio.observe(el));

  /* ---------- hero arch frame: a flat SVG cut-out redrawn per frame; the photo is a separate GPU layer ---------- */
  const heroFrame = (() => {
    const svg = $('.hero-frame'); if (!svg) return null;
    const hole = $('.hf-hole', svg), r1 = $('.hf-ring1', svg), r2 = $('.hf-ring2', svg);
    let W = 0, H = 0, aw = 0, ah = 0, ay = 0, K = 1;
    const arch = (cx, cy, w, h) => {
      const x = cx - w / 2, y = cy - h / 2, f = n => n.toFixed(1);
      return `M${f(x)} ${f(y + h)}V${f(y + .414 * h)}C${f(x)} ${f(y + .229 * h)} ${f(x + .2 * w)} ${f(y + .1 * h)} ${f(x + .42 * w)} ${f(y + .039 * h)}L${f(cx)} ${f(y)}L${f(x + .58 * w)} ${f(y + .039 * h)}C${f(x + .8 * w)} ${f(y + .1 * h)} ${f(x + w)} ${f(y + .229 * h)} ${f(x + w)} ${f(y + .414 * h)}V${f(y + h)}Z`;
    };
    const api = {
      resize() {
        W = innerWidth; H = innerHeight;
        aw = Math.min(W * .32, H * .36, 300); if (W <= 760) aw = Math.min(W * .56, H * .34);
        ah = aw * 1.4; ay = H * .05;
        K = Math.max(W / aw, H / ah) * 3.2;
        svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
        api.draw(api.p || 0);
      },
      draw(p) {
        api.p = p;
        const e = Math.pow(p, 1.7); // starts slow, then opens with growing momentum
        const s = 1 + e * K, cx = W / 2, cy = H / 2 + ay * (1 - p);
        hole.setAttribute('d', `M-10 -10H${W + 10}V${H + 10}H-10Z` + arch(cx, cy, aw * s, ah * s));
        const ro = Math.max(0, 1 - p * 4);
        r1.setAttribute('d', arch(cx, cy - 2, aw * s * 1.08, ah * s * 1.036)); r1.style.opacity = ro;
        r2.setAttribute('d', arch(cx, cy - 4, aw * s * 1.18, ah * s * 1.07)); r2.style.opacity = ro * .45;
        svg.style.opacity = p > .985 ? 0 : 1;
      },
    };
    return api;
  })();

  /* ---------- smooth wheel scrolling (inertial, Lenis-style) ---------- */
  const fine = matchMedia('(pointer: fine)').matches;
  const sm = { on: fine && !reduce, target: scrollY, cur: scrollY, running: false, last: 0 };
  const maxScroll = () => document.documentElement.scrollHeight - innerHeight;
  const scrollableParent = el => {
    for (; el && el !== document.body; el = el.parentElement) {
      if (el.matches && el.matches('.cmdk, .lb, .sheet, .look, textarea, select, iframe')) return true;
      const st = getComputedStyle(el);
      if (/(auto|scroll)/.test(st.overflowY) && el.scrollHeight > el.clientHeight + 1) return true;
    }
    return false;
  };
  const smLoop = now => {
    const dt = Math.min(.05, (now - (sm.last || now)) / 1000 || .016); sm.last = now;
    sm.cur += (sm.target - sm.cur) * (1 - Math.exp(-dt * 9));
    if (Math.abs(sm.target - sm.cur) < .4) { sm.cur = sm.target; sm.running = false; }
    window.scrollTo(0, sm.cur);
    if (sm.running) requestAnimationFrame(smLoop); else sm.last = 0;
  };
  if (sm.on) {
    addEventListener('wheel', e => {
      if (e.ctrlKey || document.body.style.overflow === 'hidden' || scrollableParent(e.target)) return;
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      e.preventDefault();
      const d = e.deltaY * (e.deltaMode === 1 ? 32 : e.deltaMode === 2 ? innerHeight : 1);
      if (!sm.running) sm.cur = scrollY;
      sm.target = clamp(sm.target + d, 0, maxScroll());
      if (!sm.running) { sm.running = true; requestAnimationFrame(smLoop); }
    }, { passive: false });
    // keyboard, scrollbar drag, anchors: follow the real position
    addEventListener('scroll', () => { if (!sm.running) { sm.target = sm.cur = scrollY; } }, { passive: true });
  }

  /* =====================================================================
     SIGNATURE SCENES — each page has its own scroll motif. Every scene exposes
     el.__measure() (layout, on resize) and el.__onP(p) (0→1 progress, eased by the engine).
     ===================================================================== */
  const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const easeOut = x => 1 - Math.pow(1 - x, 3);
  const SVGNS = 'http://www.w3.org/2000/svg';

  // 1. Silsila stem — a golden vine grows down the page and flowers at each milestone (About, Admissions)
  $$('.stem').forEach(st => {
    const svg = $('.stem-svg', st), path = $('.stem-path', svg), ghost = $('.stem-ghost', svg), tip = $('.stem-tip', svg);
    const leaves = $('.stem-leaves', svg), items = $$('.stem-item', st);
    let H = 1, L = 1, nodesY = [];
    path.setAttribute('pathLength', 1);
    st.__measure = () => {
      const W = st.clientWidth; H = st.offsetHeight;
      const mobile = W < 760, cx = mobile ? 22 : W / 2, sway = mobile ? 9 : +(st.dataset.sway || 54);
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      const top0 = st.getBoundingClientRect().top;
      nodesY = items.map(it => { const r = $('.stem-node', it).getBoundingClientRect(); return r.top + r.height / 2 - top0; });
      let d = `M${cx} 0`, py = 0;
      nodesY.forEach((y, i) => { const sw = (i % 2 ? 1 : -1) * sway, dy = y - py; d += ` C${cx + sw} ${py + dy * .3} ${cx + sw} ${py + dy * .7} ${cx} ${y}`; py = y; });
      d += ` C${cx} ${py + (H - py) * .4} ${cx} ${H - 10} ${cx} ${H}`;
      path.setAttribute('d', d); ghost.setAttribute('d', d);
      L = path.getTotalLength() || 1;
      leaves.innerHTML = '';
      nodesY.forEach((y, i) => {
        [[-1, -34], [1, -18], [-1, 22]].forEach(([side, off], k) => {
          if (mobile && side < 0) return;
          const g = document.createElementNS(SVGNS, 'path');
          const x0 = cx, y0 = y + off, dir = (i + k) % 2 ? 1 : -1, s = side * (mobile ? .7 : 1) * (k === 1 ? 1.15 : 1);
          g.setAttribute('d', `M${x0} ${y0} q${18 * s} ${-14 * dir} ${36 * s} ${-4 * dir} q${-14 * s} ${14 * dir} ${-36 * s} ${4 * dir}z`);
          g.setAttribute('class', 'stem-leaf'); g.dataset.i = i; g.style.transitionDelay = (k * 120) + 'ms';
          leaves.appendChild(g);
        });
      });
      st.__leaves = $$('.stem-leaf', leaves);
      if (st.__p !== undefined) st.__onP(st.__p, true);
    };
    st.__onP = (p, force) => {
      st.__p = p;
      path.style.strokeDashoffset = (1 - p).toFixed(4);
      const pt = path.getPointAtLength(L * p);
      tip.setAttribute('transform', `translate(${pt.x.toFixed(1)} ${pt.y.toFixed(1)})`);
      tip.style.opacity = p > .002 && p < .998 ? 1 : 0;
      const tipY = pt.y;
      let last = -1;
      items.forEach((it, i) => { const on = tipY >= nodesY[i] - 6; it.classList.toggle('on', on); if (on) last = i; });
      (st.__leaves || []).forEach(l => l.classList.toggle('on', +l.dataset.i <= last));
      st.classList.toggle('done', p > .985);
    };
  });

  // 2. R.E.L.A.X flower — five petals open one by one
  $$('.flower-scene').forEach(fs => {
    const petals = $$('.petal', fs), panels = $$('.flower-panel', fs), core = $('.flower-core', fs);
    let cur = -1;
    fs.__onP = p => {
      petals.forEach((pt, i) => {
        const k = easeOut(clamp(p * 6.2 - i * 1.05));
        pt.style.setProperty('--s', (.15 + .85 * k).toFixed(3));
        pt.style.setProperty('--o', k.toFixed(3));
      });
      const i = Math.min(4, Math.max(0, Math.floor(p * 6.2 / 1.05 - .35)));
      if (i !== cur) { panels.forEach((pn, k) => pn.classList.toggle('on', k === i)); petals.forEach((pt, k) => pt.classList.toggle('on', k === i)); cur = i; }
      core.style.setProperty('--r', (p * 72).toFixed(2) + 'deg');
      fs.classList.toggle('bloom', p > .9);
    };
  });

  // 3. Campus — walk through a sequence of keel-arch doorways
  $$('.tunnel').forEach(tn => {
    const doors = $$('.door', tn), caps = $$('.door-cap', tn), dots = $$('.door-dots i', tn);
    const n = doors.length;
    // decode every doorway photo up front so the zoom never waits on an image
    doors.forEach(d => { const im = $('img', d); if (im && im.decode) im.decode().catch(() => {}); });
    let cur = -1;
    tn.__onP = p => {
      const x = p * (n - 1);
      doors.forEach((d, i) => {
        const t = x - i;
        let s, o;
        if (t <= 0) { s = Math.pow(2.3, t); o = clamp((t + 1.7) / 1.1); }
        else { s = Math.pow(5.5, t); o = clamp(1 - t * 1.9); }
        d.style.transform = `translate(-50%, -50%) scale(${s.toFixed(4)})`;
        d.style.opacity = o.toFixed(3);
        d.style.visibility = o < .01 ? 'hidden' : 'visible';
      });
      const i = Math.round(x);
      if (i !== cur) { caps.forEach((c, k) => c.classList.toggle('on', k === i)); dots.forEach((dt, k) => dt.classList.toggle('on', k <= i)); cur = i; }
    };
  });

  // 4. People — a halaqa (teaching circle) slowly turning around the Principal
  $$('.halaqa').forEach(hq => {
    const seats = $$('.seat', hq), n = seats.length;
    let R = 400, ry = .3;
    hq.__measure = () => { const W = innerWidth, Hh = innerHeight; R = Math.min(W * (W < 760 ? .42 : .38), 560, Hh * .7); ry = W < 760 ? .5 : .3; };
    hq.__onP = p => {
      const spin = -90 + p * 110;
      seats.forEach((st, i) => {
        const a = (spin + i * 360 / n) * Math.PI / 180;
        const x = Math.cos(a) * R, z = Math.sin(a), y = z * R * ry;
        const appear = easeOut(clamp(p * 3.2 - i * .16));
        const sc = (.66 + .34 * (z + 1) / 2) * (.6 + .4 * appear);
        st.style.transform = `translate(${x.toFixed(1)}px, ${(y + (1 - appear) * 60).toFixed(1)}px) translate(-50%, -50%) scale(${sc.toFixed(3)})`;
        st.style.opacity = (appear * (.45 + .55 * (z + 1) / 2)).toFixed(3);
        st.style.zIndex = z > 0 ? 3 : 1;
      });
      hq.style.setProperty('--ring', clamp(p * 2.5).toFixed(3));
    };
  });

  // 5. Students — the Ascent: twelve Arabic-named classes as steps toward the dome
  $$('.ascent').forEach(as => {
    const steps = $$('.step', as), panels = $$('.ascent-panel', as), mark = $('.ascent-mark', as), track = $('.steps', as);
    let pts = [];
    as.__measure = () => {
      const tr = track.getBoundingClientRect();
      pts = steps.map(s => { const r = s.getBoundingClientRect(); return [r.left - tr.left + r.width / 2, r.top - tr.top]; });
      if (as.__p !== undefined) as.__onP(as.__p);
    };
    let cur = -1;
    as.__onP = p => {
      as.__p = p;
      if (!pts.length) return;
      const x = clamp(p * 1.08) * (pts.length - 1), i = Math.floor(x), f = x - i, j = Math.min(pts.length - 1, i + 1);
      const fx = pts[i][0] + (pts[j][0] - pts[i][0]) * f;
      const hop = Math.sin(f * Math.PI) * 26;
      const fy = pts[i][1] + (pts[j][1] - pts[i][1]) * ease(f) - hop;
      mark.style.transform = `translate(${fx.toFixed(1)}px, ${(fy - 18).toFixed(1)}px) translate(-50%, -50%)`;
      const k = Math.round(x);
      if (k !== cur) { steps.forEach((s, m) => { s.classList.toggle('on', m === k); s.classList.toggle('past', m < k); }); panels.forEach((pn, m) => pn.classList.toggle('on', m === k)); cur = k; }
      as.classList.toggle('summit', p > .96);
    };
  });

  // 6. Gallery — album covers fly in to form a keel-arch mosaic
  $$('.mosaic').forEach(ms => {
    const tiles = $$('.tile', ms), ring = $('.mosaic-ring', ms);
    let plan = [];
    const rnd = (i, k) => { const x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
    ms.__measure = () => {
      const W = innerWidth, H = innerHeight, mobile = W < 760;
      const ah = mobile ? Math.min(H * .46, W * 1.05) : Math.min(H * .74, 820), aw = ah / 1.4;
      const cx = mobile ? W / 2 : W * .66, cy = mobile ? H * .36 : H * .54;
      const cols = mobile ? 9 : 11, c = aw / cols, rows = Math.round(ah / c);
      const cells = [];
      for (let r = rows - 1; r >= 0; r--) for (let q = 0; q < cols; q++) {
        const u = (q + .5) / cols, v = (r + .5) / rows;
        // keel-arch silhouette: straight sides below 41%, then curving in to a point
        const half = v >= .414 ? .5 : .5 * Math.sqrt(1 - Math.pow(1 - v / .414, 2)) * (.86 + .14 * v / .414);
        if (Math.abs(u - .5) <= half - .25 / cols) cells.push([cx - aw / 2 + (q + .5) * c, cy - ah / 2 + (r + .5) * c]);
      }
      plan = tiles.map((t, i) => {
        const cell = cells[i % cells.length];
        t.style.width = t.style.height = (c - 2).toFixed(1) + 'px';
        t.style.display = i < cells.length ? '' : 'none';
        return { tx: cell[0], ty: cell[1], sx: rnd(i, 1) * W, sy: rnd(i, 2) * H * 1.3 - H * .15, r: (rnd(i, 3) - .5) * 60, d: rnd(i, 4) * .38 };
      });
      if (ring) { ring.style.width = aw + 'px'; ring.style.height = ah + 'px'; ring.style.left = cx + 'px'; ring.style.top = cy + 'px'; }
      if (ms.__p !== undefined) ms.__onP(ms.__p);
    };
    ms.__onP = p => {
      ms.__p = p;
      plan.forEach((pl, i) => {
        const k = ease(clamp((p - pl.d) / .5));
        const x = pl.sx + (pl.tx - pl.sx) * k, y = pl.sy + (pl.ty - pl.sy) * k;
        tiles[i].style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -50%) rotate(${(pl.r * (1 - k)).toFixed(1)}deg) scale(${(.55 + .45 * k).toFixed(3)})`;
        tiles[i].style.opacity = (.35 + .65 * k).toFixed(3);
      });
      if (ring) ring.style.opacity = clamp((p - .78) * 5).toFixed(3);
      ms.style.setProperty('--m', clamp((p - .55) * 2.2).toFixed(3));
    };
  });

  /* ---------- scroll scenes: geometry cached, progress eased toward the scroll target ---------- */
  const scenes = $$('.scrolly, .flowy').map(el => ({ el, flow: el.classList.contains('flowy'), top: 0, span: 1, p: 0, target: 0, shown: -1 }));
  const words = $$('.ayah-en .w');
  const tree = $('.tree-scene');
  const tiers = tree ? $$('.tier', tree) : [];
  const nodes = tree ? $$('.node', tree) : [];
  const progs = tree ? $$('.tier-prog i', tree) : [];
  const rail = $('.rail');
  const measure = () => {
    if (rail) rail.closest('.scrolly').style.setProperty('--rail-x', Math.max(0, rail.scrollWidth - innerWidth) + 'px');
    scenes.forEach(sc => { const r = sc.el.getBoundingClientRect(); sc.top = r.top + scrollY; sc.span = Math.max(1, sc.flow ? sc.el.offsetHeight : sc.el.offsetHeight - innerHeight); if (sc.el.__measure) sc.el.__measure(); sc.shown = -1; });
    if (heroFrame) heroFrame.resize();
  };
  let lastLit = -1, lastTier = -1;
  const apply = sc => {
    const p = sc.p;
    if (Math.abs(p - sc.shown) < .0002) return;
    sc.shown = p;
    sc.el.style.setProperty('--p', p.toFixed(4));
    if (sc.el.__onP) sc.el.__onP(p);
    if (sc.el.classList.contains('hero') && heroFrame) heroFrame.draw(p);
    if (sc.el.classList.contains('ayah') && words.length) {
      const lit = Math.floor(clamp((p - .08) / .8) * (words.length + 1));
      if (lit !== lastLit) { words.forEach((w, i) => w.classList.toggle('lit', i < lit)); lastLit = lit; }
    }
    if (sc.el === tree) {
      sc.el.style.setProperty('--tp', clamp(p * 1.15).toFixed(4));
      const i = Math.min(tiers.length - 1, Math.floor(p * tiers.length * .999));
      if (i !== lastTier) {
        tiers.forEach((t, k) => t.classList.toggle('on', k === i));
        nodes.forEach(n => n.classList.toggle('on', +n.dataset.at <= i));
        progs.forEach((g, k) => g.classList.toggle('on', k <= i));
        lastTier = i;
      }
    }
  };
  let sceneRaf = 0, sceneLast = 0;
  const sceneLoop = now => {
    const dt = Math.min(.05, (now - (sceneLast || now)) / 1000 || .016); sceneLast = now;
    const k = window.RQ_NO_EASE ? 1 : 1 - Math.exp(-dt * 14);
    let moving = false;
    const y = scrollY, vh = innerHeight;
    for (const sc of scenes) {
      sc.target = sc.flow ? clamp((y + vh * .62 - sc.top) / sc.span) : clamp((y - sc.top) / sc.span);
      if (y + vh < sc.top - vh || y > sc.top + sc.span + 2 * vh) { if (sc.p !== sc.target) { sc.p = sc.target; apply(sc); } continue; }
      sc.p += (sc.target - sc.p) * k;
      if (Math.abs(sc.target - sc.p) < .0004) sc.p = sc.target; else moving = true;
      apply(sc);
    }
    sceneRaf = moving ? requestAnimationFrame(sceneLoop) : 0;
    if (!moving) sceneLast = 0;
  };
  const kickScenes = () => { if (!sceneRaf && !reduce) sceneRaf = requestAnimationFrame(sceneLoop); };
  let ticking = false;
  const onScroll = () => { kickScenes(); if (ticking) return; ticking = true; requestAnimationFrame(() => { onHeader(); ticking = false; }); };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { measure(); onScroll(); });
  addEventListener('load', () => { measure(); kickScenes(); });
  if (document.fonts) document.fonts.ready.then(() => { measure(); kickScenes(); });
  new ResizeObserver(() => measure()).observe(document.body);
  measure(); onHeader(); kickScenes();
  if (reduce) { words.forEach(w => w.classList.add('lit')); tiers.forEach(t => t.classList.add('on')); nodes.forEach(n => n.classList.add('on')); scenes.forEach(sc => { if (sc.el.__onP) sc.el.__onP(sc.flow ? 1 : .999); }); }
  $$('.tree-svg .draw').forEach(p => p.setAttribute('pathLength', 1));

  /* ---------- hero slideshow inside the arch ---------- */
  const slides = $$('.hero-media .slide');
  if (slides.length > 1 && !reduce && !window.RQ_STILL) { let k = 0; setInterval(() => { slides[k].classList.remove('on'); k = (k + 1) % slides.length; slides[k].classList.add('on'); }, 5200); }

  /* ---------- command palette ---------- */
  const cmdk = $('#cmdk'), q = $('#cmdk-q'), list = $('#cmdk-list');
  let index = null, sel = 0, hits = [];
  const norm = s => (s || '').toLowerCase().normalize('NFKD').replace(/[ً-ٟ]/g, '');
  const render = () => {
    const v = norm(q.value.trim());
    hits = !v ? index.filter(x => x.k === 'Page').slice(0, 10)
      : index.map(x => { const t = norm(x.t), s = norm(x.s); const sc = t.startsWith(v) ? 3 : t.includes(v) ? 2 : s.includes(v) ? 1 : v.split(/\s+/).every(w => t.includes(w) || s.includes(w)) ? .5 : 0; return [sc, x]; })
        .filter(a => a[0]).sort((a, b) => b[0] - a[0]).slice(0, 14).map(a => a[1]);
    sel = 0;
    list.innerHTML = hits.length ? hits.map((x, i) => `<li><a href="${x.u}" class="${i ? '' : 'sel'}"${x.k === 'Link' ? ' target="_blank" rel="noopener"' : ''}><span><b${/[؀-ۿ]/.test(x.t) ? ' class="ar" style="font-size:19px"' : ''}>${x.t.replace(/</g, '&lt;')}</b>${x.s ? `<br><small>${x.s.replace(/</g, '&lt;')}</small>` : ''}</span><span class="k">${x.k}</span></a></li>`).join('')
      : '<div class="cmdk-empty">Nothing found. Try “admission”, “robotics” or “Tajweed”.</div>';
  };
  const openK = async () => {
    cmdk.classList.add('open'); q.value = ''; q.focus();
    if (!index) { list.innerHTML = '<div class="cmdk-empty">Loading…</div>'; index = await fetch(RQ.searchUrl).then(r => r.json()); }
    render();
  };
  $$('[data-cmdk]').forEach(b => b.addEventListener('click', openK));
  q && q.addEventListener('input', render);
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); cmdk.classList.contains('open') ? cmdk.classList.remove('open') : openK(); }
    if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openK(); }
    if (!cmdk.classList.contains('open')) return;
    const as = $$('a', list);
    if (e.key === 'Escape') cmdk.classList.remove('open');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length; as.forEach((a, i) => a.classList.toggle('sel', i === sel)); as[sel] && as[sel].scrollIntoView({ block: 'nearest' }); }
    if (e.key === 'Enter' && as[sel]) { e.preventDefault(); as[sel].click(); }
  });
  cmdk && cmdk.addEventListener('click', e => { if (e.target === cmdk) cmdk.classList.remove('open'); });

  /* ---------- lightbox: any [data-lb] inside a [data-lb-group] ---------- */
  const lb = $('#lb'), lbImg = $('#lb-img'), lbThumbs = $('#lb-thumbs');
  let group = [], gi = 0, gTitle = '';
  const show = i => {
    gi = (i + group.length) % group.length; lbImg.src = group[gi]; lbImg.alt = gTitle;
    $('#lb-count').textContent = `${gi + 1} / ${group.length}`;
    $$('button', lbThumbs).forEach((b, k) => b.classList.toggle('on', k === gi));
    const on = $$('button', lbThumbs)[gi]; on && on.scrollIntoView({ inline: 'center', block: 'nearest' });
    new Image().src = group[(gi + 1) % group.length];
  };
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-lb]'); if (!a) return; e.preventDefault();
    const g = a.closest('[data-lb-group]');
    const items = g ? $$('[data-lb]', g) : [a];
    group = items.map(x => x.getAttribute('href') || x.dataset.lb); gTitle = g ? (g.dataset.lbGroup || '') : '';
    $('#lb-title').textContent = gTitle;
    lbThumbs.innerHTML = group.map((s, k) => `<button data-k="${k}"><img src="${s}" loading="lazy" alt=""></button>`).join('');
    lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden';
    show(items.indexOf(a));
  });
  const closeLb = () => { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; };
  lb && lb.addEventListener('click', e => {
    if (e.target.closest('[data-lb-close]')) closeLb();
    else if (e.target.closest('[data-lb-prev]')) show(gi - 1);
    else if (e.target.closest('[data-lb-next]')) show(gi + 1);
    else if (e.target.closest('[data-k]')) show(+e.target.closest('[data-k]').dataset.k);
  });
  document.addEventListener('keydown', e => { if (!lb.classList.contains('open')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowRight') show(gi + 1); if (e.key === 'ArrowLeft') show(gi - 1); });
  let sx = null;
  lb && lb.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  lb && lb.addEventListener('touchend', e => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(gi + (dx < 0 ? 1 : -1)); sx = null; });

  /* ---------- filters (gallery, staff, students) ---------- */
  $$('[data-filter-group]').forEach(grp => {
    const target = $(grp.dataset.filterGroup);
    grp.addEventListener('click', e => {
      const b = e.target.closest('[data-filter]'); if (!b) return;
      $$('[data-filter]', grp).forEach(x => x.classList.toggle('on', x === b));
      const f = b.dataset.filter;
      $$('[data-tags]', target).forEach(el => { el.style.display = (f === '*' || el.dataset.tags.split('|').includes(f)) ? '' : 'none'; });
    });
  });
  $$('[data-search]').forEach(inp => {
    const target = $(inp.dataset.search);
    inp.addEventListener('input', () => { const v = inp.value.toLowerCase().trim(); $$('[data-name]', target).forEach(el => { el.style.display = el.dataset.name.toLowerCase().includes(v) ? '' : 'none'; }); });
  });

  /* ---------- lite YouTube ---------- */
  document.addEventListener('click', e => {
    const v = e.target.closest('[data-yt]'); if (!v) return;
    v.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${v.dataset.yt}?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Video"></iframe>`;
  });

  /* ---------- "right now at Rawdat" ---------- */
  const nowEls = $$('[data-now]');
  const refreshNow = () => fetch(RQ.nowUrl).then(r => r.json()).then(d => {
    nowEls.forEach(el => {
      el.innerHTML = d.current ? `<i></i><span>Now at Rawdat · <b>${d.current.title}</b> until ${d.current.until} <span class="muted">(${d.time} IST)</span></span>`
        : `<i style="background:var(--gold)"></i><span>${d.weekday}, ${d.time} in Mumbai · ${d.open ? 'school in session' : 'campus is resting'}</span>`;
    });
    $$('[data-slot]').forEach(s => s.classList.toggle('now', !!d.current && s.dataset.slot === d.current.title));
  }).catch(() => {});
  if (nowEls.length) { refreshNow(); setInterval(refreshNow, 60000); }

  /* ---------- admission eligibility ---------- */
  $$('[data-elig]').forEach(f => {
    const out = $('[data-elig-out]', f.parentElement) || $('[data-elig-out]');
    const run = () => {
      const dob = f.dob.value, year = f.year.value; if (!dob) return;
      fetch(`${RQ.eligUrl}?dob=${encodeURIComponent(dob)}&year=${encodeURIComponent(year)}`).then(r => r.json()).then(d => {
        if (d.error) { out.innerHTML = `<p class="muted">${d.error}</p>`; return; }
        out.innerHTML = `<div class="caps muted">Age on 1st June · ${d.age_years} yrs ${d.age_months} mo</div>` + (d.eligible
          ? `<div class="cls" style="margin-top:12px">${d.cls.label}<span class="ar">${d.cls.ar}</span></div><p class="muted" style="margin:10px 0 0">${d.cls.name} · ${d.cls.phase}</p>`
          : `<p style="margin-top:12px;font-size:18px">${d.message}</p>`);
        const sel = $('select[name=class_slug]'); if (sel && d.eligible) sel.value = d.cls.slug;
      });
    };
    f.addEventListener('input', run); f.addEventListener('submit', e => { e.preventDefault(); run(); });
  });

  /* ---------- audio stories ---------- */
  const player = $('[data-player]');
  if (player) {
    const audio = new Audio(); audio.preload = 'none';
    const items = $$('.tracks li'); let cur = -1;
    const title = $('[data-p-title]'), num = $('[data-p-num]'), btn = $('[data-p-play]'), scrub = $('[data-p-scrub]'), time = $('[data-p-time]'), rate = $('[data-p-rate]');
    const fmt = s => isFinite(s) ? `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}` : '0:00';
    const load = (i, play = true) => {
      cur = (i + items.length) % items.length; const li = items[cur];
      audio.src = li.dataset.src; audio.playbackRate = +(rate && rate.value || 1);
      title.textContent = li.dataset.title; num.textContent = `Story ${li.dataset.n} of ${items.length}`;
      items.forEach((x, k) => x.classList.toggle('on', k === cur));
      if (play) audio.play();
      history.replaceState(null, '', '#t' + li.dataset.n);
    };
    items.forEach((li, i) => $('button', li).addEventListener('click', () => (i === cur ? (audio.paused ? audio.play() : audio.pause()) : load(i))));
    btn.addEventListener('click', () => { if (cur < 0) load(0); else audio.paused ? audio.play() : audio.pause(); });
    $('[data-p-prev]').addEventListener('click', () => load(cur - 1));
    $('[data-p-next]').addEventListener('click', () => load(cur + 1));
    rate && rate.addEventListener('change', () => { audio.playbackRate = +rate.value; });
    audio.addEventListener('play', () => { player.classList.remove('paused'); btn.innerHTML = '<svg width="22" height="22"><use href="#pause"/></svg>'; });
    audio.addEventListener('pause', () => { player.classList.add('paused'); btn.innerHTML = '<svg width="22" height="22"><use href="#play"/></svg>'; });
    audio.addEventListener('timeupdate', () => { scrub.value = audio.duration ? 1000 * audio.currentTime / audio.duration : 0; time.textContent = `${fmt(audio.currentTime)} / ${fmt(audio.duration)}`; });
    audio.addEventListener('ended', () => load(cur + 1));
    scrub.addEventListener('input', () => { if (audio.duration) audio.currentTime = scrub.value / 1000 * audio.duration; });
    const m = location.hash.match(/^#t(\d+)/);
    if (m) { const i = items.findIndex(li => li.dataset.n === m[1]); if (i >= 0) { load(i, false); items[i].scrollIntoView({ block: 'center' }); } }
  }

  /* ---------- reader keyboard paging ---------- */
  const pages = $$('.reader-page');
  if (pages.length) {
    const ctr = $('[data-page-ctr]');
    const pio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && ctr) ctr.textContent = `${+e.target.dataset.i + 1} / ${pages.length}`; }), { threshold: .5 });
    pages.forEach(p => pio.observe(p));
    document.addEventListener('keydown', e => {
      if (!/ArrowRight|ArrowLeft|PageDown|PageUp/.test(e.key) || lb.classList.contains('open')) return;
      const i = pages.findIndex(p => p.getBoundingClientRect().top > 10);
      const t = /Right|Down/.test(e.key) ? pages[Math.max(0, i)] : pages[Math.max(0, i - 2)];
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
    });
  }

  /* ---------- misc ---------- */
  const fl = $('.flash'); if (fl) setTimeout(() => fl.remove(), 4200);
  $$('form[data-confirm]').forEach(f => f.addEventListener('submit', e => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));
  if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
})();

