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

