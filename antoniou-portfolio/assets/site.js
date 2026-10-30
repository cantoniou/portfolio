/* Renders index.html from data/*.json. Nothing here needs editing to change content; edit the JSON. */
(async function () {
  const load = async (n) => (await fetch(`data/${n}.json`, { cache: 'no-cache' })).json();
  const [profile, metrics, projects, people, timeline] = await Promise.all(['profile', 'metrics', 'projects', 'people', 'timeline'].map(load));
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (n) => typeof n === 'number' ? n.toLocaleString('en-US') : n;
  const year = new Date().getFullYear();
  const ox = metrics.openalex, sc = metrics.scopus, pm = metrics.people;
  const NS = 'http://www.w3.org/2000/svg';
  const el = (p, n, a, t) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (t != null) e.textContent = t; p.appendChild(e); return e; };
  const C = { coral: '#F97B4F', coralDeep: '#C24F1E', plum: '#584053', grey: '#CFC3C9', ink: '#3D2C38', ink2: '#84727E' };

  /* Hero */
  document.title = `${profile.name} · ${profile.chair_name}`;
  $('hero-eye').textContent = `${profile.chair_name} · TUM`;
  $('hero-name').textContent = profile.name;
  $('hero-bio').textContent = profile.bio;
  $('hero-roles').innerHTML = profile.roles.map((r) => `<span class="chip">${esc(r.role)} · ${esc(r.where)}${r.since ? ' · since ' + r.since : ''}</span>`).join('');
  $('card-title').textContent = `TSE · since ${profile.founded.slice(0, 4)}`;
  $('card-asof').textContent = `as of ${metrics.as_of}`;
  const stat = (n, l, cls = '') => `<div class="stat"><div class="n ${cls}">${fmt(n)}</div><div class="l">${esc(l)}</div></div>`;
  $('hero-stats').innerHTML = stat(sc.publications, 'publications (Scopus)') + stat(sc.citations, 'citations (Scopus)', 'c') + stat(sc.h_index, 'h-index (Scopus)', 't') + stat(pm.partner_countries, 'partner countries', 'g');
  $('hero-foot').innerHTML = `${pm.researchers_today} researchers today · ${pm.alumni} alumni · ${pm.doctorates_completed} doctorates · ${pm.theses_supervised} theses`;

  /* Numbers */
  const tile = (n, l) => `<div class="tile"><div class="big">${fmt(n)}</div><p>${esc(l)}</p></div>`;
  $('scopus-tiles').innerHTML = tile(sc.publications, 'scientific publications') + tile(sc.journal_articles, 'journal articles') + tile(sc.conference_papers, 'conference papers') + tile(sc.book_chapters, 'book chapters') + tile(sc.books, 'books') + tile(sc.coauthors, 'co-authors') + tile(sc.journals, 'different journals') + tile(sc.research_topics, 'research topics');
  $('chart-src').textContent = `OpenAlex · ${ox.as_of}`;
  $('numbers-note').textContent = `Career totals are Scopus (${sc.as_of}); Google Scholar counts ${metrics.scholar.citations} citations and h-index ${metrics.scholar.h_index}. The per-year chart is OpenAlex, which also indexes preprints and reports: ${fmt(ox.tum_era.works)} works and ${fmt(ox.tum_era.citations)} citations since ${ox.tum_era.from_year}, ${ox.tum_era.works_over_100_citations} papers above 100 citations, ${Math.round(ox.tum_era.open_access_share * 100)}% open access.`;
  (() => {
    const s = $('cWorks'), rows = ox.by_year, L = 10, R = 10, T = 34, B = 30, W = 900, H = 280, pw = W - L - R, ph = H - T - B, band = pw / rows.length, bw = band * .6, max = Math.max(...rows.map((r) => r.works)) * 1.08, y = (v) => T + ph - v / max * ph;
    rows.forEach((r, i) => { const x = L + i * band + (band - bw) / 2, hot = i === 0 || i === rows.length - 1; el(s, 'rect', { x, y: y(r.works), width: bw, height: T + ph - y(r.works), rx: 6, fill: hot ? C.coral : C.plum }); el(s, 'text', { x: x + bw / 2, y: y(r.works) - 10, 'text-anchor': 'middle', class: 'lab' }, r.works); el(s, 'text', { x: x + bw / 2, y: T + ph + 20, 'text-anchor': 'middle' }, r.year + (r.year === year ? '*' : '')); });
    el(s, 'text', { x: W - R, y: H - 4, 'text-anchor': 'end', 'font-size': 10.5 }, `* ${year} to date`);
  })();

  /* Research pillars + top papers */
  const pillars = [
    ['Modeling & Simulation', 'Micro and mesoscopic simulation in SUMO, PTV VISUM, MATSim, SimMobility and Aimsun, extended with graph neural networks and transfer learning.'],
    ['Calibration & Optimization', 'Calibrating stochastic, noisy, large-scale transport models offline and online; W-SPSA, PCA-GLS, PCA-EKF, PC-SPSA.'],
    ['Road Safety & Human Factors', 'Driving simulator and eye tracking, naturalistic driving data at scale, acceptance of emerging transport modes.'],
    ['Big Data & Machine Learning', 'Data-driven, interpretable models of driving behaviour and traffic dynamics, and which data are worth collecting.'],
  ];
  $('pillars').innerHTML = pillars.map((p, i) => `<div class="tile"><div class="k">Pillar <b>0${i + 1}</b></div><h3>${p[0]}</h3><p>${p[1]}</p></div>`).join('');
  (() => {
    const s = $('cTop'), P = ox.top_papers.slice(0, 12), L = 320, R = 60, T = 4, W = 900, pw = W - L - R, rh = 27, max = Math.max(...P.map((p) => p.citations));
    s.setAttribute('viewBox', `0 0 900 ${T + P.length * rh + 6}`);
    P.forEach((p, i) => { const yy = T + i * rh; el(s, 'text', { x: L - 12, y: yy + 17, 'text-anchor': 'end', 'font-size': 12.5, 'font-family': 'Plus Jakarta Sans, sans-serif', 'font-weight': p.tse ? 700 : 500, fill: p.tse ? C.ink : C.ink2 }, `${p.first_author} · ${p.year}`); el(s, 'rect', { x: L, y: yy + 4, width: p.citations / max * pw, height: 19, rx: 6, fill: p.tse ? C.plum : C.grey }); el(s, 'text', { x: L + p.citations / max * pw + 10, y: yy + 18, class: 'lab' }, p.citations); });
  })();

  /* Projects */
  const P = projects.projects.map((p) => ({ ...p, status: p.status || (p.end >= year ? 'ongoing' : 'finished') }));
  const groups = ['EU', 'DFG', 'German ministries', 'TUM IGSSE', 'DAAD', 'Other'];
  let counts = {};
  const ov = projects.funder_counts_override;
  if (ov) { groups.forEach((g) => { if (ov[g]) counts[g] = { ...ov[g] }; }); }
  else { groups.forEach((g) => { counts[g] = { ongoing: P.filter((p) => p.funder_group === g && p.status === 'ongoing').length, finished: P.filter((p) => p.funder_group === g && p.status === 'finished').length }; }); }
  const total = Object.values(counts).reduce((a, c) => a + c.ongoing + c.finished, 0), onTot = Object.values(counts).reduce((a, c) => a + c.ongoing, 0);
  $('projects-h2').innerHTML = `${total} funded projects since ${Math.min(...P.map((p) => p.start))}. <em>${onTot} running today.</em>`;
  const af = projects.active_funding_tum_share_eur, eur = (v) => v >= 1e6 ? `€${(v / 1e6).toFixed(1)}M` : `€${Math.round(v / 1e3)}k`;
  $('funding-stats').innerHTML = Object.entries(af).map(([k, v], i) => stat(eur(v), `${k} · TUM share of active projects`, ['', 'c', 't'][i % 3])).join('') + stat(eur(Object.values(af).reduce((a, b) => a + b, 0)), 'active TUM share in total');
  (() => {
    const s = $('cFund'), F = groups.filter((g) => counts[g]).sort((a, b) => (counts[b].ongoing + counts[b].finished) - (counts[a].ongoing + counts[a].finished)), L = 180, R = 60, T = 6, W = 900, pw = W - L - R, rh = 36, max = Math.max(...F.map((g) => counts[g].ongoing + counts[g].finished)), x = (v) => L + v / max * pw;
    s.setAttribute('viewBox', `0 0 900 ${T + F.length * rh}`);
    F.forEach((g, i) => { const yy = T + i * rh, on = counts[g].ongoing, fin = counts[g].finished, tot = on + fin; el(s, 'text', { x: L - 14, y: yy + 20, 'text-anchor': 'end', 'font-size': 14, 'font-family': 'Plus Jakarta Sans, sans-serif', 'font-weight': 700, fill: C.ink }, g); if (on) el(s, 'rect', { x: L, y: yy + 5, width: x(on) - L, height: 22, rx: 6, fill: C.coral }); if (fin) el(s, 'rect', { x: x(on) + (on ? 3 : 0), y: yy + 5, width: x(tot) - x(on) - (on ? 3 : 0), height: 22, rx: 6, fill: C.grey }); el(s, 'text', { x: x(tot) + 10, y: yy + 21, class: 'lab', 'font-size': 16 }, tot); if (on) el(s, 'text', { x: L + 8, y: yy + 20, 'font-size': 11.5, 'font-weight': 600, fill: C.ink }, `${on} ongoing`); });
  })();
  (() => {
    const s = $('cProj'), rows = [...P].sort((a, b) => a.start - b.start || a.end - b.end), L = 150, R = 16, T = 30, W = 900, rh = 15.5, lo = Math.min(...rows.map((r) => r.start)) - .3, hi = Math.max(...rows.map((r) => r.end)) + 1, pw = W - L - R, x = (v) => L + (v - lo) / (hi - lo) * pw, bot = T + rows.length * rh;
    s.setAttribute('viewBox', `0 0 900 ${bot + 30}`);
    for (let yr = Math.ceil(lo); yr <= hi; yr++) { el(s, 'line', { x1: x(yr), x2: x(yr), y1: T - 4, y2: bot, class: 'grid' }); el(s, 'text', { x: x(yr), y: bot + 20, 'text-anchor': 'middle', 'font-size': 11.5 }, yr); }
    rows.forEach((p, i) => { const yy = T + i * rh + rh / 2; el(s, 'text', { x: L - 10, y: yy + 4, 'text-anchor': 'end', 'font-size': 11, fill: C.ink, 'font-family': 'Plus Jakarta Sans, sans-serif', 'font-weight': 600 }, p.name); el(s, 'rect', { x: x(p.start), y: yy - 5, width: Math.max(8, x(p.end + 1) - x(p.start)), height: 10, rx: 5, fill: p.funder_group === 'EU' ? C.coral : p.funder_group === 'DFG' ? C.plum : C.grey }); });
  })();
  $('projlist').innerHTML = P.filter((p) => p.status === 'ongoing').map((p) => `<div class="proj"><div class="k on">${esc(p.funder)} <span>${p.start}–${p.end}</span></div><h4>${esc(p.name)}</h4>${p.full_name ? `<p><b>${esc(p.full_name)}</b></p>` : ''}${p.summary ? `<p>${esc(p.summary)}</p>` : ''}</div>`).join('');

  /* People */
  const team = people.team, n = (t) => team.filter((p) => p.type === t).length;
  $('people-h2').innerHTML = `We are <em>${pm.researchers_today}</em> today. <em>${pm.alumni}</em> alumni, ${pm.alumni_in_faculty_positions} of them in faculty positions.`;
  $('people-stats').innerHTML = stat(n('doctoral') + n('external'), `doctoral researchers, ${n('external')} in industry`) + stat(n('postdoc'), 'postdoctoral researchers') + stat(pm.doctorates_completed, 'doctorates completed', 'c') + stat(pm.theses_supervised, 'theses supervised', 't') + stat(pm.industrial_collaborations, 'industrial collaborations', 'g');
  $('team-list').innerHTML = team.map((p) => `<li><b>${esc(p.name)}</b>${p.role ? ' · ' + esc(p.role) : ''}${p.employer ? ' · external, ' + esc(p.employer) : ''}${p.note ? ' · ' + esc(p.note) : ''}</li>`).join('');
  $('alumni-chips').innerHTML = people.alumni.filter((a) => a.where).map((a) => `<span class="chip sans ${a.kind === 'faculty' ? 't' : a.kind === 'industry' ? 'c' : ''}" title="${esc(a.name)} · ${esc(a.now)}">${esc(a.where)}</span>`).join('');
  $('visiting-list').innerHTML = people.visiting_professors.map((v) => `<li><b>${esc(v.name)}</b>, ${esc(v.from)} (${esc(v.when)})</li>`).join('');

  /* Timeline, conferences, honours */
  const byYear = {};
  timeline.events.forEach((e) => { (byYear[e.date.slice(0, 4)] ||= []).push(e); });
  $('tl').innerHTML = Object.keys(byYear).sort().map((y) => `<div class="yr"><div class="y">${y}</div><div class="dot ${byYear[y].some((e) => e.kind === 'honour') ? 'hot' : ''}"></div>${byYear[y].sort((a, b) => a.date.localeCompare(b.date)).map((e) => `<div class="ev"><b>${esc(e.title)}</b><span>${esc(e.detail || '')}</span></div>`).join('')}</div>`).join('');
  $('conf-chips').innerHTML = timeline.conferences_organised.map((c) => `<span class="chip sans">${esc(c.name)} · ${esc(c.where)}${c.with ? ' · with ' + esc(c.with) : ''}</span>`).join('');
  $('honours').innerHTML = profile.honours.map((h) => `<div class="row"><span class="y">${h.year}</span><span class="e">${esc(h.what)}${h.by ? `<small>${esc(h.by)}</small>` : ''}</span></div>`).join('');
  $('next-tiles').innerHTML = profile.next_decade.map((d, i) => `<div class="tile"><div class="k">0${i + 1}</div><h3>${esc(d.title)}</h3><p>${esc(d.text)}</p></div>`).join('');

  /* Footer */
  $('contact').innerHTML = `<b>${esc(profile.name)}</b> · ${esc(profile.chair_name)}, ${esc(profile.institution)}<br>${esc(profile.address)} · <a href="mailto:${esc(profile.email)}">${esc(profile.email)}</a> · <a href="${esc(profile.website)}">chair website</a> · <a href="https://orcid.org/${esc(profile.orcid)}">ORCID</a>`;
  $('sources').textContent = `Scopus and Google Scholar figures as of ${sc.as_of}; OpenAlex figures as of ${ox.as_of}; people and projects as of ${people.as_of}.`;
})().catch((e) => { document.body.insertAdjacentHTML('beforeend', `<p style="padding:24px;color:#C24F1E">Could not load site data: ${e.message}. If you opened index.html from your disk, serve the folder instead (python3 -m http.server) or view it on GitHub Pages.</p>`); });
