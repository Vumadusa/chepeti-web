// Тур застосунком (ідея — блок «Cinematic hero» з 21st.dev, переписано під статичний сайт і стиль Chepeti):
// заголовок розмивається, знизу виїжджає картка, у ній зʼявляється телефон, далі під час прокрутки змінюються екрани,
// підписи й плашки. GSAP + ScrollTrigger (pin, scrub). «Зменшити рух» чи немає GSAP — лишається статичний варіант з CSS.
(() => {
  const tour = document.querySelector('.tour');
  const g = window.gsap, ST = window.ScrollTrigger;
  if (!tour || !g || !ST || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  g.registerPlugin(ST);
  tour.classList.add('anim');

  const $ = s => tour.querySelector(s), $$ = s => [...tour.querySelectorAll(s)];
  const intro = $('.tour-intro'), card = $('.tour-card'), phone = $('.tour-phone'), tilt = $('.tour-tilt');
  const imgs = $$('.tour-phone img'), texts = $$('.tour-texts > div'), badges = $$('.badge'), dots = $$('.tour-steps span');
  const n = imgs.length;

  g.set(card, { yPercent: 118, scale: 0.94 });
  g.set(phone, { y: 220, rotationX: 38, rotationY: -18, scale: 0.72, autoAlpha: 0, transformPerspective: 1200 });
  g.set(imgs.slice(1), { autoAlpha: 0 });

  // Крапки кроків — від часу самої анімації (scrub доганяє прокрутку із запізненням, тож не від події прокрутки).
  const tl = g.timeline({
    defaults: { ease: 'power2.inOut' },
    onUpdate: () => {
      const t = tl.time();
      let on = 0;
      for (let i = 0; i < n; i++) if (t >= tl.labels['s' + i] - 0.3) on = i;
      dots.forEach((d, i) => d.classList.toggle('on', i === on));
    },
    scrollTrigger: {
      trigger: tour, start: 'top top', end: () => '+=' + innerHeight * (n + 1.6),
      pin: $('.tour-stage'), scrub: 0.8, anticipatePin: 1, invalidateOnRefresh: true,
    },
  });

  tl.to(intro, { scale: 1.08, filter: 'blur(12px)', autoAlpha: 0, duration: 1 }, 0)
    .to(card, { yPercent: 0, scale: 1, duration: 1 }, 0)
    .to(phone, { y: 0, rotationX: 0, rotationY: 0, scale: 1, autoAlpha: 1, duration: 1.1, ease: 'expo.out' })
    .addLabel('s0', '-=0.6')
    .fromTo(texts[0], { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.6 }, 's0')
    .fromTo(badges[0], { autoAlpha: 0, y: 30, scale: 0.9 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.6, ease: 'back.out(1.4)' }, 's0+=0.15');

  for (let i = 1; i < n; i++) {
    tl.to({}, { duration: 0.7 })
      .addLabel('s' + i)
      .to(texts[i - 1], { autoAlpha: 0, y: -24, duration: 0.45 }, 's' + i)
      .to(badges[i - 1], { autoAlpha: 0, y: -18, duration: 0.4 }, 's' + i)
      .to(imgs[i], { autoAlpha: 1, duration: 0.6 }, 's' + i)
      .fromTo(texts[i], { autoAlpha: 0, y: 28 }, { autoAlpha: 1, y: 0, duration: 0.5 }, 's' + i + '+=0.2')
      .fromTo(badges[i], { autoAlpha: 0, y: 28, scale: 0.9 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.4)' }, 's' + i + '+=0.3');
  }
  tl.to({}, { duration: 0.8 });

  // Легкий нахил телефона за курсором — лише з мишею, на окремій обгортці (прокрутка керує самим телефоном).
  if (tilt && matchMedia('(pointer: fine)').matches) {
    const rx = g.quickTo(tilt, 'rotationX', { duration: 1, ease: 'power3.out' });
    const ry = g.quickTo(tilt, 'rotationY', { duration: 1, ease: 'power3.out' });
    g.set(tilt, { transformPerspective: 1000 });
    tour.addEventListener('pointermove', e => {
      ry(((e.clientX / innerWidth) - 0.5) * 14);
      rx(-((e.clientY / innerHeight) - 0.5) * 10);
    });
  }
})();
