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
      shade.style.setProperty('--src', `url(${next.src})`);
      bx.classList.remove('wob'); void bx.offsetWidth; bx.classList.add('wob', 'up');
      bx.classList.remove('down');
      setTimeout(() => { busy = false; }, 550);
    }, still ? 0 : 320);
  };
  kinds.forEach((b, k) => b.addEventListener('click', () => { auto = false; show(k); }));
  bx.addEventListener('click', () => { auto = false; show((cur + 1) % kinds.length); });
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting && !seen) { seen = true; kinds.forEach(b => { new Image().src = src(b.dataset.sp); }); }
    clearInterval(timer);
    if (e.isIntersecting && auto && !still) timer = setInterval(() => auto ? show((cur + 1) % kinds.length) : clearInterval(timer), 2600);
  }).observe(box);
})();
