// Підвал: коробка, з якої визирає улюбленець (власник 18.11). Вибір виду — тварина ховається, коробка хитається, вискакує нова.
// Поки ніхто не обрав — види міняються самі, лише коли блок на екрані.
(() => {
  const box = document.querySelector('.pb');
  if (!box) return;
  const pet = box.querySelector('.pb-pet'), cast = box.querySelector('.pb-cast img'), shade = box.querySelector('.pb-shade'), bx = box.querySelector('.pb-box'), kinds = [...box.querySelectorAll('.pb-kinds button')];
  const src = sp => pet.src.replace(/[a-z]+\.webp/, sp + '.webp');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cur = 0, busy = false, auto = true, seen = false, timer;
  const show = i => {
    if (busy || i === cur) return;
    busy = true; cur = i;
    kinds.forEach((b, k) => b.setAttribute('aria-checked', String(k === i)));
    const next = new Image(); next.src = src(kinds[i].dataset.sp);
    bx.classList.remove('up'); bx.classList.add('down');
    setTimeout(async () => {
      await next.decode().catch(() => {});
      pet.src = cast.src = next.src;
      bx.dataset.sp = kinds[i].dataset.sp;
      shade.style.setProperty('--src', `url(${next.src})`);
      bx.classList.remove('wob'); void bx.offsetWidth; bx.classList.add('wob', 'up');
      bx.classList.remove('down');
      setTimeout(() => { busy = false; }, 550);
    }, still ? 0 : 320);
  };
  // Кільце зірочок: дві комети по 9 іскор, голова найбільша, хвіст тьмяніє. Крутиться лише коли блок на екрані.
  const orb = ['back', 'front'].map(c => { const d = document.createElement('div'); d.className = 'pb-orbit ' + c; bx.append(d); return d; });
  const stars = [];
  // Розкид, щоб іскри летіли роєм, а не по лінії: кожна зі своїм зсувом від еліпса, нерівним кроком і повільним погойдуванням.
  const rnd = (a, b) => a + Math.random() * (b - a);
  for (let c = 0; c < 2; c++) for (let k = 0, lag = 0; k < 11; k++, lag += rnd(0.06, 0.2)) {
    const el = document.createElement('i');
    el.className = 'pb-star' + (Math.random() < 0.4 ? ' dot' : '');
    el.style.setProperty('--s', `${Math.max(4, rnd(11, 16) - k * 1.1)}px`);
    stars.push({ el, c, k, lag, dr: rnd(-7, 7), dy: rnd(-6, 6), ph: rnd(0, 6.3), sp: rnd(0.0007, 0.0016), front: null });
  }
  const TILT = -0.12, cosT = Math.cos(TILT), sinT = Math.sin(TILT);
  const draw = t => {
    const a0 = t * 0.0006;
    for (const s of stars) {
      const a = a0 + s.c * Math.PI - s.lag, w = Math.sin(t * s.sp + s.ph);
      const ex = (55 + s.dr + 3 * w) * Math.cos(a), ey = 12 * Math.sin(a) + s.dy + 2.5 * Math.cos(t * s.sp * 1.3 + s.ph);
      const front = Math.sin(a) > 0;
      if (front !== s.front) { s.front = front; orb[+front].append(s.el); }
      s.el.style.left = `${50 + ex * cosT - ey * sinT}%`;
      s.el.style.top = `${58 + ex * sinT + ey * cosT}%`;
      s.el.style.opacity = ((1 - s.k / 12) * (0.65 + 0.35 * Math.sin(t * 0.008 + s.k * 1.7)) * (front ? 1 : 0.6)).toFixed(2);
    }
  };
  let raf = 0;
  const spin = on => { cancelAnimationFrame(raf); if (on) { const f = t => { draw(t); raf = requestAnimationFrame(f); }; raf = requestAnimationFrame(f); } };
  draw(0);
  kinds.forEach((b, k) => b.addEventListener('click', () => { auto = false; show(k); }));
  bx.addEventListener('click', () => { auto = false; show((cur + 1) % kinds.length); });
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting && !seen) { seen = true; kinds.forEach(b => { new Image().src = src(b.dataset.sp); }); }
    clearInterval(timer);
    if (!still) spin(e.isIntersecting);
    if (e.isIntersecting && auto && !still) timer = setInterval(() => auto ? show((cur + 1) % kinds.length) : clearInterval(timer), 2600);
  }).observe(box);
})();
