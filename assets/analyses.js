// Блок «Аналізи на графіку»: невидимі зони поверх справжнього скриншота списку; наведення (миша) чи дотик (телефон) —
// підказка з графіком показника. Дані — ті самі демо-аналізи, що в застосунку (src/dev/demo.ts addYearOfAnalyses),
// передані збирачем у data-an. Графік — SVG у стилі застосунку: смуга норми, точки, остання точка виділена.
(() => {
  const box = document.querySelector('[data-an]');
  if (!box) return;
  const D = JSON.parse(box.dataset.an);
  const tip = box.querySelector('.an-tip');
  const spots = [...box.querySelectorAll('.an-spot')];
  const fmt = n => String(n).replace('.', D.dec);

  function chart(m, upto) {
    const W = 300, H = 150, P = { l: 30, r: 10, t: 10, b: 22 };
    const vals = m.v.slice(0, upto + 1), all = [...m.v, m.ref[0], m.ref[1]];
    const lo = Math.min(...all) * 0.9, hi = Math.max(...all) * 1.05;
    const x = i => P.l + (W - P.l - P.r) * i / (m.v.length - 1);
    const y = v => P.t + (H - P.t - P.b) * (1 - (v - lo) / (hi - lo));
    const pts = vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
    const dots = vals.map((v, i) => {
      const out = v < m.ref[0] || v > m.ref[1], last = i === vals.length - 1;
      return `<circle cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="${last ? 5 : 3.2}" fill="${out ? '#D49A3C' : 'var(--accent-deep)'}"${last ? ' stroke="#fff" stroke-width="2"' : ''}/>`;
    }).join('');
    const ticks = [0, 4, 8, 12, m.v.length - 1].filter(i => i <= m.v.length - 1)
      .map(i => `<text x="${x(i).toFixed(1)}" y="${H - 5}" text-anchor="middle">${D.dates[i]}</text>`).join('');
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${m.name}">
      <rect x="${P.l}" y="${y(m.ref[1]).toFixed(1)}" width="${W - P.l - P.r}" height="${(y(m.ref[0]) - y(m.ref[1])).toFixed(1)}" rx="6" fill="var(--accent)" opacity=".14"/>
      <text x="${P.l - 5}" y="${(y(m.ref[1]) + 4).toFixed(1)}" text-anchor="end">${fmt(m.ref[1])}</text>
      <text x="${P.l - 5}" y="${(y(m.ref[0]) + 4).toFixed(1)}" text-anchor="end">${fmt(m.ref[0])}</text>
      <polyline points="${pts}" fill="none" stroke="var(--accent-deep)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="1" class="an-line"/>
      ${dots}${ticks}</svg>`;
  }

  let cur = 0, metric = 0;
  function show(i) {
    cur = i;
    const r = D.rows[i];
    spots.forEach((s, k) => s.classList.toggle('on', k === i));
    tip.style.setProperty('--top', spots[i].style.top);
    let body;
    if (r.series != null) {
      const m = D.metrics[metric], v = m.v[r.series], prev = m.v[r.series - 1];
      body = `<div class="an-tabs" role="tablist">${D.metrics.map((x, k) => `<button type="button" role="tab" aria-selected="${k === metric}" data-m="${k}">${x.name}</button>`).join('')}</div>
        <p class="an-now"><b>${fmt(v)}</b> ${m.unit}<span>${D.prev}: ${fmt(prev)}</span></p>${chart(m, r.series)}
        <p class="an-norm">${D.norm}: ${fmt(m.ref[0])}–${fmt(m.ref[1])} ${m.unit}</p>`;
    } else {
      body = `<ul class="an-vals">${r.vals.map(([n, v]) => `<li><span>${n}</span><b>${v}</b></li>`).join('')}</ul><p class="an-note">${r.note}</p>`;
    }
    tip.innerHTML = `<p class="an-title">${r.title}<span>${r.date}</span></p>${body}`;
    tip.querySelectorAll('[data-m]').forEach(b => b.addEventListener('click', e => { e.stopPropagation(); metric = +b.dataset.m; show(cur); }));
    tip.classList.remove('pop'); void tip.offsetWidth; tip.classList.add('pop');
  }
  spots.forEach((s, i) => {
    s.addEventListener('mouseenter', () => { if (cur !== i) show(i); });
    s.addEventListener('focus', () => show(i));
    s.addEventListener('click', () => show(i));
  });
  show(0);
})();
