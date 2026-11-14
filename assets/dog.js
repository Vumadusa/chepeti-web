// Песик на першому екрані: очі (під головою, видно крізь отвори) стежать за курсором з невеликою амплітудою.
// Без миші (телефон) — зрідка сам поглядає в різні боки. «Зменшити рух» — дивиться прямо.
(() => {
  const dog = document.querySelector('.dog');
  const g = window.gsap;
  if (!dog || !g || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const eyes = [...dog.querySelectorAll('.eye')];
  const MAX = 11; // % від розміру ока: білок більший за отвір, тож край не відкривається
  const mv = eyes.map(e => ({ e, x: g.quickTo(e, 'xPercent', { duration: 0.6, ease: 'power3.out' }), y: g.quickTo(e, 'yPercent', { duration: 0.6, ease: 'power3.out' }) }));

  function look(px, py) {
    for (const m of mv) {
      const r = m.e.getBoundingClientRect();
      const dx = px - (r.left + r.width / 2), dy = py - (r.top + r.height / 2);
      const d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 260);
      m.x((dx / d) * MAX * k);
      m.y((dy / d) * MAX * 0.8 * k);
    }
  }

  if (matchMedia('(pointer: fine)').matches) {
    addEventListener('pointermove', e => look(e.clientX, e.clientY), { passive: true });
  } else {
    const wander = () => {
      const r = dog.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) look(r.left + Math.random() * r.width, r.top + Math.random() * r.height * 1.4);
      setTimeout(wander, 2200 + Math.random() * 2600);
    };
    setTimeout(wander, 1200);
  }
})();
