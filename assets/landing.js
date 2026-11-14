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

// «Доглядайте разом»: тап на роль показує приклад прав — рівень і відкриті розділи, як в аркуші прав застосунку.
(() => {
  const tabs = [...document.querySelectorAll('.family .who button')];
  const box = document.querySelector('.family .rights');
  if (!box || !tabs.length) return;
  const lv = [...box.querySelectorAll('.rights-level span')], rows = [...box.querySelectorAll('.rights-list li')], note = box.querySelector('.rights-note');
  tabs.forEach(b => b.addEventListener('click', () => {
    tabs.forEach(x => x.setAttribute('aria-selected', String(x === b)));
    lv.forEach((x, k) => x.classList.toggle('on', k === +b.dataset.lv));
    rows.forEach((x, k) => x.classList.toggle('on', b.dataset.on[k] === '1'));
    note.textContent = b.dataset.note;
  }));
})();
