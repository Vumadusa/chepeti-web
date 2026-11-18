// Підвал: «Спробуйте: ваш улюбленець у Chepeti» (власник 18.11). Імʼя й вид — наживо в картці, як у застосунку; мордочки й
// кольори — ті самі, що в застосунку (assets/ava = src/ui/art/avatars.ts, SPECIES_FILL). Нічого не надсилається й не зберігається.
(() => {
  const box = document.querySelector('.pc');
  if (!box) return;
  const FILL = { cat: '#56B9AB', dog: '#F29E55', rabbit: '#E898B1', rodent: '#D7B153', bird: '#64B1E4', reptile: '#72C06A', other: '#B399E2' };
  const VARIANTS = 6;
  const input = box.querySelector('input'), nameEl = box.querySelector('.pc-name'), spEl = box.querySelector('.pc-sp');
  const ava = box.querySelector('.pc-ava'), img = ava.querySelector('img'), kinds = [...box.querySelectorAll('.pc-kinds button')];
  const ph = box.dataset.ph;
  let sp = 'cat', v = 1;
  const pop = () => { ava.classList.remove('pop'); void ava.offsetWidth; ava.classList.add('pop'); };
  const draw = () => {
    img.src = `/assets/ava/${sp}-${v}.svg`;
    ava.style.setProperty('--fill', FILL[sp]);
    pop();
  };
  input.addEventListener('input', () => {
    const n = input.value.trim();
    nameEl.textContent = n || ph; // textContent — без розмітки з поля
    nameEl.classList.toggle('ph', !n);
  });
  nameEl.classList.add('ph');
  kinds.forEach(b => b.addEventListener('click', () => {
    kinds.forEach(x => x.setAttribute('aria-checked', String(x === b)));
    sp = b.dataset.sp; v = 1;
    spEl.textContent = b.textContent;
    draw();
  }));
  box.querySelectorAll('.pc-arrow').forEach(b => b.addEventListener('click', () => {
    v = ((v - 1 + Number(b.dataset.d)) % VARIANTS + VARIANTS) % VARIANTS + 1;
    draw();
  }));
})();
