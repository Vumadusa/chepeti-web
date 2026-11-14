// Поява блоків під час прокрутки (IntersectionObserver, без слухача scroll) і лінія під шапкою після першого екрана.
// «Зменшити рух» обробляє CSS: там .reveal одразу видимий. Клас .js ставить рядок у <head>.
(() => {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  const bar = document.querySelector('.top');
  const hero = document.querySelector('.tour-intro');
  if (bar && hero) new IntersectionObserver(([e]) => bar.classList.toggle('scrolled', !e.isIntersecting),
    { rootMargin: '-80px 0px 0px 0px' }).observe(hero);

  // Тема: без вибору — як у системі; кнопка перемикає й запамʼятовує (localStorage може бути недоступний — тоді лише до перезавантаження).
  const btn = document.querySelector('.theme');
  if (btn) btn.addEventListener('click', () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch {}
  });
})();


// Сітка-слід на тлі (див. .grid-bg у CSS): клітинки на весь екран, рух миші вмикає одну й знімає попередню —
// 2 зміни на рух замість перемальовування всієї сітки. На сенсорних екранах наведення немає — сітки теж.
(() => {
  const svg = document.querySelector('.grid-bg');
  if (!svg || !matchMedia('(pointer: fine)').matches) return;
  document.documentElement.classList.add('has-grid');
  const C = 40, NS = 'http://www.w3.org/2000/svg';
  let cols = 0, cells = [], cur = null;
  function build() {
    cols = Math.ceil(innerWidth / C);
    const rows = Math.ceil(innerHeight / C);
    const frag = document.createDocumentFragment();
    cells = [];
    for (let i = 0; i < cols * rows; i++) {
      const r = document.createElementNS(NS, 'rect');
      r.setAttribute('x', (i % cols) * C); r.setAttribute('y', Math.floor(i / cols) * C);
      r.setAttribute('width', C); r.setAttribute('height', C);
      frag.appendChild(r); cells.push(r);
    }
    svg.replaceChildren(frag); cur = null;
  }
  build();
  let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(build, 150); });
  addEventListener('pointermove', e => {
    const c = cells[Math.floor(e.clientY / C) * cols + Math.floor(e.clientX / C)];
    if (c === cur) return;
    cur?.classList.remove('on'); c?.classList.add('on'); cur = c;
  }, { passive: true });
  document.addEventListener('pointerleave', () => { cur?.classList.remove('on'); cur = null; });
})();

// «Завантажити» в шапці: віконце закривається тапом повз нього та Esc.
(() => {
  const dl = document.querySelector('.dl');
  if (!dl) return;
  document.addEventListener('click', e => { if (dl.open && !dl.contains(e.target)) dl.open = false; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') dl.open = false; });
})();
