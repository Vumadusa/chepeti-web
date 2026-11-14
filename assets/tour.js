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
  const imgs = $$('.tour-phone img'), texts = $$('.tour-texts > div'), sets = $$('.badge-set'), dots = $$('.tour-steps span');
  const n = imgs.length;
  const stops = []; // мітки «крок показано повністю» — точки прилипання

  // Верх картки визирає внизу першого екрана. На ПК — 95% висоти картки вниз; на телефоні песик менший і вище,
  // тож картку піднято, щоб вона заходила на низ песика й голова не «висіла» в повітрі (власник 14.11).
  const dog = $('.dog');
  const peek = () => {
    if (!dog || !matchMedia('(max-width: 860px)').matches) return card.offsetHeight * 0.95;
    const sr = $('.tour-stage').getBoundingClientRect(), dr = dog.getBoundingClientRect();
    // −20% висоти песика: зелене накриває підборіддя; −3% картки: стартовий масштаб 0,94 опускає її верх
    return Math.min(card.offsetHeight * 0.95, dr.bottom - sr.top - dr.height * 0.2 - card.offsetTop - card.offsetHeight * 0.03);
  };
  // Телефон / сенсорний екран: без 3D-повороту й розмиття — вони перемальовують кадр щоразу й гальмували прокрутку (власник 14.11).
  const lite = matchMedia('(max-width: 860px), (pointer: coarse)').matches;
  if (lite) tour.classList.add('lite');
  g.set(phone, lite ? { y: 80, scale: 0.92, autoAlpha: 0 } : { y: 220, rotationX: 38, rotationY: -18, scale: 0.72, autoAlpha: 0, transformPerspective: 1200 });
  g.set(imgs.slice(1), { autoAlpha: 0 });

  // Крапки кроків — від часу самої анімації (scrub доганяє прокрутку із запізненням, тож не від події прокрутки).
  const tl = g.timeline({
    defaults: { ease: 'power2.inOut' },
    onUpdate: () => {
      const t = tl.time();
      let on = 0;
      for (let i = 0; i < n; i++) if (t >= tl.labels['s' + i] - 0.3) on = i;
      dots.forEach((d, i) => d.classList.toggle('on', i === on));
      tour.dataset.step = on; // зони аналізів у телефоні активні лише на своєму кроці
    },
    scrollTrigger: {
      // Шлях довший (~1,3 екрана на крок), згладжування мʼякше, а після прокрутки — прилипання до найближчого кроку
      // в напрямку руху: інерційний трекпад Mac інакше проскакував 2–3 кроки за жест і зупинявся посеред переходу.
      trigger: tour, start: 'top top', end: () => '+=' + innerHeight * (n + 1) * 1.3,
      pin: $('.tour-stage'), scrub: 1, anticipatePin: 1, invalidateOnRefresh: true,
      snap: {
        snapTo: (v, self) => ST.snapDirectional([0, ...stops.map(l => tl.labels[l] / tl.duration()), 1])(v, self.direction),
        duration: { min: 0.3, max: 0.9 }, delay: 0.12, ease: 'power2.inOut', inertia: false,
      },
    },
  });

  tl.to(intro, lite ? { y: -40, autoAlpha: 0, duration: 1 } : { scale: 1.08, filter: 'blur(12px)', autoAlpha: 0, duration: 1 }, 0)
    .fromTo(card, { y: peek, scale: 0.94 }, { y: 0, scale: 1, duration: 1 }, 0)
    .to(phone, lite ? { y: 0, scale: 1, autoAlpha: 1, duration: 1.1, ease: 'expo.out' } : { y: 0, rotationX: 0, rotationY: 0, scale: 1, autoAlpha: 1, duration: 1.1, ease: 'expo.out' })
    .addLabel('s0', '-=0.6')
    .fromTo(texts[0], { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.6 }, 's0')
    .fromTo(sets[0].children, { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.5, stagger: 0.08, ease: 'back.out(1.5)' }, 's0+=0.15')
    .addLabel('v0');
  stops.push('v0');

  for (let i = 1; i < n; i++) {
    tl.to({}, { duration: 0.7 })
      .addLabel('s' + i)
      .to(texts[i - 1], { autoAlpha: 0, y: -24, duration: 0.45 }, 's' + i)
      .to(sets[i - 1].children, { autoAlpha: 0, scale: 0.9, duration: 0.35, stagger: 0.03 }, 's' + i)
      .to(imgs[i], { autoAlpha: 1, duration: 0.6 }, 's' + i)
      .fromTo(texts[i], { autoAlpha: 0, y: 28 }, { autoAlpha: 1, y: 0, duration: 0.5 }, 's' + i + '+=0.2')
      .fromTo(sets[i].children, { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.45, stagger: 0.07, ease: 'back.out(1.5)' }, 's' + i + '+=0.3')
      .addLabel('v' + i);
    stops.push('v' + i);
  }
  tl.to({}, { duration: 0.8 });

  // «Можливості» в шапці: не на верх секції (там ще песик), а одразу на перший крок, коли картка вже піднялась.
  document.querySelectorAll('a[href="#features"]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const st = tl.scrollTrigger;
    scrollTo({ top: st.start + (st.end - st.start) * tl.labels.v0 / tl.duration(), behavior: 'smooth' });
  }));

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

// «Доглядайте разом»: телефон спершу відхилений назад і трохи менший, під час прокрутки випрямляється
// (ідея — PhoneScrollHero, переписано на GSAP, власник 14.11). «Зменшити рух» — стоїть рівно.
(() => {
  const g = window.gsap, ST = window.ScrollTrigger;
  const phone = document.querySelector('.fam-visual .phone');
  if (!phone || !g || !ST || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  g.registerPlugin(ST);
  g.fromTo(phone, { rotationX: 22, scale: 0.94, y: 40, transformPerspective: 1200, transformOrigin: '50% 100%' },
    { rotationX: 0, scale: 1, y: 0, ease: 'none',
      scrollTrigger: { trigger: phone, start: 'top bottom', end: 'center center', scrub: 0.6 } });
})();
