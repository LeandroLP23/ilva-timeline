const $ = s => document.querySelector(s);
// model estimates stay in events.js but are not shown for now: too easy to dispute
window.PERIODS = PERIODS.filter(p => p.kind !== 'estimate');
const MIN = 1955, MAX = 2026;
const COLORS = { history: '#8e979c', environment: '#8fa05a', health: '#c4553b', justice: '#5b8db3', work: '#d39233' };
const CATEGORIES = { history: 'Storia', environment: 'Ambiente', health: 'Salute', justice: 'Giustizia', work: 'Lavoro' };
const KIND_LABELS = { estimate: 'stima da modello', measurement: 'dato misurato', count: 'conteggio' };
const capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);
const ERAS = [
  [1955, 'countryside', 'Campagna', 'Campagna: uliveti e masserie'],
  [1960, 'construction', 'Cantiere', 'Cantiere Italsider (Stato, IRI-Finsider)'],
  [1965, 'active', 'Italsider, gestione pubblica', 'Italsider, a gestione pubblica'],
  [1995, 'active', 'Gruppo Riva', 'Ilva, gruppo Riva'],
  [2013, 'active', 'Comm.', 'Amministrazione straordinaria'],
  [2018, 'active', 'Mittal', 'ArcelorMittal'],
  [2021, 'active', 'AdI', 'Acciaierie d\'Italia, Stato e ArcelorMittal'],
  [2024, 'active', 'Comm.', 'Di nuovo in amministrazione straordinaria'],
];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
// event-driven scale: every year with events gets the same space, empty years are compressed
// (at most 1.5 event-years per gap, however long)
const EVENT_YEARS = new Set(EVENTS.map(e => e.year));
const WEIGHT = {};
for (let y = MIN; y <= MAX; ) {
  if (EVENT_YEARS.has(y)) { WEIGHT[y] = 1; y++; continue; }
  let end = y; while (end + 1 <= MAX && !EVENT_YEARS.has(end + 1)) end++;
  const n = end - y + 1, w = Math.min(0.3, 1.5 / n);
  for (let k = y; k <= end; k++) WEIGHT[k] = w;
  y = end + 1;
}
const START = {}; let TOTAL = 0;
for (let y = MIN; y <= MAX; y++) { START[y] = TOTAL; TOTAL += WEIGHT[y]; }
const pct = t => {  // also takes fractional years (t = year ± 0.5 is the year's edge)
  const y = Math.min(MAX, Math.max(MIN, Math.round(t)));
  const f = Math.min(1, Math.max(0, t - y + 0.5));
  return (START[y] + f * WEIGHT[y]) / TOTAL * 100;
};
const era = y => ERAS.filter(e => e[0] <= y).pop();
let year = MIN;

// map: a single MapLibre map, tilted for the 3D view
const mapEl = $('#map');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const FACTORY_COLOR = ['match', ['get', 'kind'], 'canopy', '#9aa1a7', 'shed', '#4a5056', 'silo', '#c3c8cb', 'tank', '#b3b9bd', '#353a3f'];
const VIEW_2D = { bounds: [[17.165, 40.472], [17.242, 40.528]], padding: 10 };  // south down to the concession piers
// default view from the Tamburi side: the district's houses in front give the plant its scale
const VIEW_3D = innerWidth < 860 ? { center: [17.219, 40.4985], zoom: 13.9, pitch: 66, bearing: -52 }
  : { center: [17.222, 40.497], zoom: 14.9, pitch: 72, bearing: -52 };
(function addVolumes() {
  const k = Math.cos(40.5 * Math.PI / 180), M = 111320;
  const g = RELIEFS.grid;
  for (const { props, rows } of RELIEFS.groups) {
    for (const [i, i2, j, h] of rows) {
      const x0 = g.lon0 + i * g.dlon, x1 = g.lon0 + i2 * g.dlon, y1 = g.lat1 - j * g.dlat, y0 = y1 - g.dlat;
      PLANTS.features.push({ type: 'Feature', properties: { ...props, h, ...(props.kind === 'hill' ? { since: 1975 } : {}) },
        geometry: { type: 'Polygon', coordinates: [[[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]] } });
    }
  }
  PORT.volumes.features.forEach(f => PLANTS.features.push(f));
  PLANTS.labels.push({ text: 'Collinette ecologiche', lonlat: [17.2235, 40.4962], kind: 'unit', since: 1975 },
    { text: '5° sporgente', lonlat: PORT.volumes.features.find(f => f.properties.kind === 'quay').geometry.coordinates[0][0], kind: 'unit', since: 1980 },
    { text: 'Moli dello stabilimento', lonlat: [17.2095, 40.4728], kind: 'unit', since: 1964 });
})();
const zoneGeo = n => GEO.zones.features.find(f => f.properties.zone === n);
const centroid = f => { const r = f.geometry.coordinates[0][0]; return r.slice(1).reduce((a, p) => [a[0] + p[0] / (r.length - 1), a[1] + p[1] / (r.length - 1)], [0, 0]); };

const labelMarkers = [];
const map = new maplibregl.Map({
  container: 'map-gl',
  style: { version: 8, sources: {}, layers: [{ id: 'land', type: 'background', paint: { 'background-color': '#c5c9bb' } }] },
  ...VIEW_3D,
  maxBounds: GEO.bounds,
  maxPitch: 80,
  maxZoom: 17.5,  // beyond this the data (1 m survey, OSM buildings) adds no detail
  attributionControl: false,
  antialias: true,
});
map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');
// at eye level MapLibre still draws markers that are behind the camera, mirrored: hide them
map.on('move', () => {
  const eye = map.getPitch() > 80 && map.transform.getCameraPosition().lngLat, k = Math.cos(40.5 * Math.PI / 180);
  for (const mk of labelMarkers) {
    let behind = false;
    if (eye) {
      const p = mk.getLngLat(), dir = Math.atan2((p.lng - eye.lng) * k, p.lat - eye.lat) * 180 / Math.PI;
      behind = Math.abs(((dir - map.getBearing()) % 360 + 540) % 360 - 180) > 75;
    }
    mk.getElement().classList.toggle('behind', behind);
  }
});
map.on('zoom', () => $('#map').classList.toggle('zoomed-in', map.getZoom() >= 14.5));
map.addControl({
  onAdd: () => Object.assign(document.createElement('div'), { className: 'maplibregl-ctrl maplibregl-ctrl-group',
    innerHTML: '<button id="full-map" type="button" aria-controls="panel" aria-expanded="true"></button>' }),
  onRemove: () => {},
}, 'top-right');
let mapReady = false;

function oliveGrove() {
  const c = document.createElement('canvas'); c.width = 28; c.height = 24;
  const g = c.getContext('2d');
  g.fillStyle = '#a9b07f'; g.fillRect(0, 0, 28, 24);
  g.fillStyle = '#5f6b38';
  for (const [x, y] of [[8, 8], [22, 20]]) { g.beginPath(); g.arc(x, y, 4.8, 0, 7); g.fill(); }
  return g.getImageData(0, 0, 28, 24);
}

map.on('load', () => {
  map.addImage('olive-grove', oliveGrove(), { pixelRatio: 2 });
  map.setLight({ anchor: 'map', position: [1.4, 230, 35], intensity: .45, color: '#ffffff' });
  GEO.concessions = PORT.concessions;
  // the concession piers are also a zone: events with zone 'port' highlight them
  GEO.zones.features.push(...PORT.concessions.features.map(f => ({ ...f, properties: { zone: 'port' } })));
  // hot area derived from the plants, inside the perimeter (build_plants.py)
  GEO.zones.features.forEach(z => { if (z.properties.zone === 'hot') z.geometry = { type: 'Polygon', coordinates: [PLANTS.hot_zone] }; });
  for (const k of ['sea', 'islands', 'plant', 'concessions', 'factory', 'stacks', 'rail', 'roads', 'city', 'zones']) map.addSource(k, { type: 'geojson', data: GEO[k], generateId: k === 'factory' || k === 'concessions' });
  const zoneIs = n => ['==', ['get', 'zone'], n];
  const noZone = ['in', ['get', 'zone'], ['literal', []]];
  [
    { id: 'sea', type: 'fill', source: 'sea', paint: { 'fill-color': '#2c4a54' } },
    { id: 'islands', type: 'fill', source: 'islands', paint: { 'fill-color': '#c5c9bb' } },
    { id: 'roads', type: 'line', source: 'roads', paint: { 'line-color': '#eceee6',
      'line-width': ['interpolate', ['linear'], ['zoom'], 12, ['case', ['==', ['get', 'major'], 1], 1.6, .7], 17, ['case', ['==', ['get', 'major'], 1], 9, 4]] } },
    { id: 'countryside', type: 'fill', source: 'plant', paint: { 'fill-pattern': 'olive-grove' } },
    { id: 'grounds', type: 'fill', source: 'plant', paint: { 'fill-color': '#80868b' } },
    { id: 'concessions', type: 'fill', source: 'concessions', paint: { 'fill-color': '#80868b' } },
    { id: 'yards', type: 'fill', source: 'zones', filter: zoneIs('yards'), paint: { 'fill-color': '#c2b393' } },
    { id: 'rail', type: 'line', source: 'rail', paint: { 'line-color': ['case', ['has', 'conveyor'], '#b9a46a', '#5f666c'],
      'line-width': ['interpolate', ['linear'], ['zoom'], 12, .3, 15, .8, 18, 2] } },
    { id: 'zones-highlight', type: 'fill', source: 'zones', filter: noZone, paint: { 'fill-color': '#a3402a', 'fill-opacity': .35 } },
    { id: 'city', type: 'fill-extrusion', source: 'city', paint: { 'fill-extrusion-color': '#a4a99b', 'fill-extrusion-height': ['get', 'h'] } },
    { id: 'city-tint', type: 'fill-extrusion', source: 'city', layout: { visibility: 'none' }, paint: { 'fill-extrusion-color': '#a4a99b', 'fill-extrusion-height': ['get', 'h'] } },
    { id: 'factory', type: 'fill-extrusion', source: 'factory', filter: ['!', ['in', ['get', 'id'], ['literal', PLANTS.batteries]]], paint: { 'fill-extrusion-color': highlight(FACTORY_COLOR), 'fill-extrusion-height': ['get', 'h'] } },
    { id: 'outline', type: 'line', source: 'plant', paint: { 'line-color': '#2b2f33', 'line-width': 1 } },
    { id: 'concessions-outline', type: 'line', source: 'concessions', paint: { 'line-color': '#2b2f33', 'line-width': 1, 'line-dasharray': [3, 2] } },
    { id: 'zones-outline', type: 'line', source: 'zones', filter: noZone, paint: { 'line-color': '#a3402a', 'line-width': 3 } },
  ].forEach(l => map.addLayer(l));


  map.addSource('plants', { type: 'geojson', data: PLANTS, generateId: true });
  map.addLayer({ id: 'plants', type: 'fill-extrusion', source: 'plants', paint: {
    'fill-extrusion-color': highlight(plantColors(year)),
    'fill-extrusion-height': ['get', 'h'], 'fill-extrusion-base': ['coalesce', ['get', 'base'], 0] } }, 'outline');
  // seen from above, hills and piles are shaded images; the cell volumes stay for 3D
  RELIEFS.images.forEach(({ url, coordinates }, k) => {
    map.addSource('relief-' + k, { type: 'image', url, coordinates });
    map.addLayer({ id: 'relief-' + k, type: 'raster', source: 'relief-' + k, paint: { 'raster-fade-duration': 0, 'raster-resampling': 'linear' } }, 'plants');
  });
  map.addLayer({ id: 'reliefs-hover', type: 'fill', source: 'plants', filter: ['in', ['get', 'kind'], ['literal', ['pile', 'hill']]],
    paint: { 'fill-opacity': 0 } }, 'plants');
  map.addLayer({ id: 'projector', type: 'custom', renderingMode: '3d', render: (gl, matrix) => { projection = matrix; } });
  map.on('pitchend', () => updateMap(year, EVENTS.filter(e => e.year === year)));
  map.addSource('port-lines', { type: 'geojson', data: PORT.lines });
  map.addLayer({ id: 'port-lines', type: 'line', source: 'port-lines', paint: { 'line-color': '#6d7276', 'line-width': ['interpolate', ['linear'], ['zoom'], 12, .6, 17, 3] } }, 'plants');
  for (const { text, lonlat, kind, since } of PLANTS.labels) {
    const el = document.createElement('div');
    el.className = 'label ' + kind;
    if (since) el.dataset.since = since;
    el.textContent = text;
    labelMarkers.push(new maplibregl.Marker({ element: el }).setLngLat(lonlat).addTo(map));
  }
  for (const { text, lat, lon, kind } of GEO.labels) {
    const el = document.createElement('div');
    el.className = 'label ' + kind;
    el.textContent = text;
    labelMarkers.push(new maplibregl.Marker({ element: el }).setLngLat([lon, lat]).addTo(map));
  }
  const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, maxWidth: '260px', className: 'feature-popup' });
  // parts of the same structure (bands of a dome, rows of piles, blast furnace with cowpers and casthouse)
  const GROUPS = {};
  PLANTS.features.forEach((f, i) => { const g = f.properties.group; if (g) (GROUPS[g] = GROUPS[g] || []).push(i); });
  let hovered = [];
  const brighten = (k, on) => map.setPaintProperty('relief-' + k, 'raster-brightness-min', on ? .25 : 0);
  const clearHover = () => { hovered.forEach(x => map.setFeatureState(x, { hover: false })); hovered = []; RELIEFS.images.forEach((_, k) => brighten(k, false)); };
  const inspect = e => {
    const layers = ['plants', 'reliefs-hover', 'factory', 'concessions'].filter(l => map.getLayoutProperty(l, 'visibility') !== 'none');
    // stacks are thin: search a 7 px neighbourhood for them, everything else exactly under the pointer
    const { x, y } = e.point;
    const f = map.queryRenderedFeatures([[x - 7, y - 7], [x + 7, y + 7]], { layers })
      .find(c => ['stack', 'e312'].includes(c.properties.kind)) || map.queryRenderedFeatures(e.point, { layers })[0];
    clearHover();
    if (!f) { popup.remove(); map.getCanvas().style.cursor = ''; return; }
    const source = f.source;
    const ids = source === 'plants' && f.properties.group ? GROUPS[f.properties.group] : [f.id];
    hovered = ids.map(id => ({ source, id }));
    hovered.forEach(x => map.setFeatureState(x, { hover: true }));
    if (f.layer.id === 'reliefs-hover')
      RELIEFS.images.forEach((im, k) => brighten(k, im.kind === f.properties.kind && im.yard === f.properties.yard));
    // one popup per structure: the main part's
    if (f.properties.group && ['cowper', 'casthouse'].includes(f.properties.kind)) f.properties.kind = 'furnace';
    map.getCanvas().style.cursor = 'help';
    const [title, detail, credit] = describe(f.properties, f.layer.id);
    popup.setLngLat(e.lngLat).setHTML(`<strong>${esc(title)}</strong><br>${esc(capitalize(detail))}<br><small>${esc(credit)}</small>`).addTo(map);
  };
  map.on('mousemove', inspect);
  map.on('click', inspect);  // phones have no hover
  map.getCanvas().addEventListener('mouseleave', () => { clearHover(); popup.remove(); });
  for (const [area, lonlat, label, anchor] of AREAS) {
    const el = document.createElement('div');
    el.className = 'map-data';
    el.hidden = true;
    el.addEventListener('click', () => {
      const first = document.querySelector(`.period[data-area="${area}"]`);
      if (!first) return;
      showPanel(true);
      first.scrollIntoView({ block: 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
      document.querySelectorAll(`.period[data-area="${area}"]`).forEach(x => { x.classList.remove('flash'); void x.offsetWidth; x.classList.add('flash'); });
    });
    areaMarkers[area] = { el, label, m: new maplibregl.Marker({ element: el, anchor }).setLngLat(lonlat).addTo(map) };
  }
  mapReady = true;
  updateMap(year, EVENTS.filter(e => e.year === year));
});


const highlight = color => ['case', ['boolean', ['feature-state', 'hover'], false], '#f0b429', color];
// where the health and environment data of the panel refer to
const AREAS = [['tamburi', [17.2335, 40.4985], 'Tamburi', 'bottom-right'], ['city', [17.2245, 40.4915], 'Taranto e Statte', 'top-right'], ['plant', [17.1935, 40.5115], 'Dentro lo stabilimento', 'bottom']];
const areaMarkers = {};
function updateAreas(y) {
  const active = PERIODS.filter(p => y >= p.from && y <= p.to && p.area);
  const has = a => active.some(p => p.area === a);
  for (const [area, { el, label }] of Object.entries(areaMarkers)) {
    const here = active.filter(p => p.area === area);
    el.hidden = !here.length;
    el.innerHTML = `<div class="where">${label}</div>` + here.map(p => `<div class="row ${p.kind}"><span class="v">${esc(p.value)}</span>` +
      `<span class="t">${esc(p.short)}${p.kind === 'estimate' ? ' <small>(stima)</small>' : ''}</span></div>`).join('');
  }
  // Tamburi in full red, the rest of the city lighter
  const color = ['case', ['all', has('tamburi'), ['==', ['get', 'tamburi'], 1]], '#c4553b', has('city') ? '#d9a091' : '#a4a99b'];
  map.setLayoutProperty('city-tint', 'visibility', (has('tamburi') || has('city')) ? 'visible' : 'none');
  map.setPaintProperty('city-tint', 'fill-extrusion-color', color);
  return has('plant');
}
const YARDS = { ore: 'parco minerale', coal: 'parco del carbone (fossile)', other: 'parco minerario secondario', open: 'parchi non coperti' };
const OSM_KINDS = { industrial: 'Capannone o impianto', shed: 'Capannone', canopy: 'Tettoia', silo: 'Silo', tank: 'Serbatoio' };
function describe(p, layer) {
  const LIDAR = 'rilievo laser del Ministero dell’Ambiente, 2008–2010';
  if (layer === 'factory')
    return [p.name ? `${p.name} (${(OSM_KINDS[p.kind] || 'edificio').toLowerCase()})` : OSM_KINDS[p.kind] || 'Edificio',
      `${Number(p.area).toLocaleString('it')} m² di pianta, ${p.hsource === 'lidar' ? '' : 'circa '}${Math.round(p.h)} m di altezza`,
      p.hsource === 'lidar' ? `Forma: OpenStreetMap; altezza: ${LIDAR}` : 'Forma: OpenStreetMap; altezza ricostruita'];
  switch (p.kind) {
    case 'stack': case 'e312':
      return p.official ? [`Camino ${p.code}`, `${p.h} m, ${p.process}`, 'Fonte: planimetria e scheda B.6, AIA 2011']
        : ['Camino', p.h !== 30 ? `${Math.round(p.h)} m, punto di emissione autorizzato` : 'punto di emissione autorizzato',
           p.h !== 30 ? `Posizione: planimetria AIA 2011; altezza: ${LIDAR}` : 'Fonte: planimetria AIA 2011'];
    case 'dome':
      return [`Copertura del ${YARDS[p.yard]}`, p.yard === 'other' ? 'costruita tra il 2019 e il 2022'
        : `completata nel ${p.since}; navata di 700 × 254 m, alta 77 m`, p.yard === 'other' ? 'Ricostruzione su base cartografica' : 'Fonte: documentazione VIA, ministero dell\'Ambiente; ISPRA'];
    case 'pile':
      return p.yard === 'open' ? ['Cumuli dei parchi non coperti', 'materie prime all’aperto, fuori dalle coperture; forma rilevata nel 2008–2010', `Fonte: ${LIDAR}`]
        : [`Cumuli del ${YARDS[p.yard]}`, `a cielo aperto fino al ${p.until}; forma rilevata nel 2008–2010`, `Fonte: ${LIDAR}`];
    case 'conveyor':
      return ['Nastro trasportatore del porto', `collega le banchine allo stabilimento, a circa ${Math.round(p.h)} m da terra`, `Tracciato: OpenStreetMap; quota: ${LIDAR}`];
    case 'hill':
      return ['Collinette ecologiche', 'rilievi artificiali di circa 9,5 ettari costruiti negli anni Settanta tra lo stabilimento e i Tamburi; sequestrati nel 2019 come deposito di rifiuti industriali',
        `Forma: ${LIDAR}; sequestro: Il Fatto Quotidiano, 05/02/2019`];
    case 'quay':
    case 'concession':
      return [p.name, 'molo del porto di Taranto: area demaniale in concessione allo stabilimento, dove si scaricano minerali e carbone e si spediscono i prodotti',
        'Concessione: nota ILVA del 11/11/2013 agli atti della Camera dei deputati; nomi dei moli: Piano regolatore portuale; contorni: OpenStreetMap'];
    case 'furnace':
      return [`Altoforno ${p.name}`, `${p.measured ? Math.round(p.h) + ' m; ' : ''}${p.stopped === 2015 ? 'fermo dal 2015' : 'trasforma minerale e coke in ghisa liquida'}`,
        `Numerazione: planimetria AIA 2011; altezza: ${p.measured ? LIDAR : 'ricostruita'}`];
    case 'casthouse': return [`Campo di colata ${p.name}`, 'dove si spilla la ghisa liquida', 'Altezza ricostruita'];
    case 'cowper': return [`Cowper ${p.name}`, 'torri che preriscaldano l\'aria soffiata nell\'altoforno', 'Altezza ricostruita'];
    case 'gasholder': return ['Gasometro', `serbatoio del gas di processo, alto ${Math.round(p.h)} m`, `Altezza: ${LIDAR}`];
    case 'battery': return ['Batteria di forni a coke', `distilla il carbone per produrre coke; alta circa ${Math.round(p.h)} m`,
      p.measured ? `Forma: OpenStreetMap; altezza: ${LIDAR}` : 'Fonte: OpenStreetMap; altezza ricostruita'];
  }
  return ['Impianto', '', ''];
}
const plantColors = y => ['match', ['get', 'kind'],
    'dome', '#e6e3da', 'pile', ['get', 'tint'],
    'furnace', ['case', ['<=', ['get', 'stopped'], y], '#7d8285', '#5b3a2e'],
    'casthouse', '#6e4a3a', 'cowper', '#9a9a94', 'gasholder', '#a9aeb2', 'e312', '#d6dde3',
    'stack', ['case', ['get', 'official'], '#8a3b26', '#9a9a94'], 'battery', '#3b2f2a',
    'conveyor', '#8fa6b5', 'hill', '#7d8752', 'quay', '#6d7276', '#555'];

// area of a lon/lat ring in km² (local projection, good enough at this scale)
const km2 = ring => {
  const k = Math.cos(40.48 * Math.PI / 180) * 111.32, M = 111.32;
  let a = 0;
  for (let i = 0; i < ring.length - 1; i++) a += ring[i][0] * k * ring[i + 1][1] * M - ring[i + 1][0] * k * ring[i][1] * M;
  return Math.abs(a) / 2;
};
function updateMap(y, ev) {
  if (!mapReady) return;
  const [, phase] = era(y);
  const vis = (id, on) => map.setLayoutProperty(id, 'visibility', on ? 'visible' : 'none');
  // legend: only the items on the map in this year
  const inYear = q => q.kind === 'dome' ? q.since <= y : q.kind === 'pile' ? q.until >= y : (q.since || 0) <= y;
  const present = new Set(phase === 'active' ? PLANTS.features.map(x => x.properties).filter(inYear).map(q => q.kind) : []);
  if (phase !== 'countryside') present.add('factory');
  if (phase !== 'countryside' && PORT.concessions.features.some(c => c.properties.since <= y)) present.add('concession');
  if (phase === 'active' && (y < 2020 || present.has('pile'))) present.add('yards');
  if (y < 2026 && production(y) > 0) present.add('dust').add('smoke');
  document.querySelectorAll('#legend [data-item]').forEach(el => { el.hidden = !el.dataset.item.split(' ').some(t => present.has(t)); });
  vis('countryside', phase === 'countryside');
  vis('grounds', phase !== 'countryside');
  vis('rail', phase !== 'countryside');
  vis('factory', phase !== 'countryside');
  vis('yards', phase === 'active' && y < 2020);
  vis('plants', phase === 'active');
  // domes from their completion year, open-air piles until the year before
  const byYear = ['any',
    ['all', ['==', ['get', 'kind'], 'dome'], ['<=', ['get', 'since'], y]],
    ['all', ['==', ['get', 'kind'], 'pile'], ['>=', ['get', 'until'], y]],
    ['all', ['!', ['in', ['get', 'kind'], ['literal', ['dome', 'pile']]]], ['<=', ['coalesce', ['get', 'since'], 0], y]]];
  const relief = ['in', ['get', 'kind'], ['literal', ['pile', 'hill']]];
  const flat = map.getPitch() < 15;
  map.setFilter('plants', flat ? ['all', byYear, ['!', relief]] : byYear);
  map.setFilter('reliefs-hover', ['all', byYear, relief]);
  vis('reliefs-hover', phase === 'active' && flat);
  RELIEFS.images.forEach((im, k) => vis('relief-' + k, phase === 'active' && flat && (im.kind === 'pile' ? y <= im.until : y >= im.since)));
  // stopped blast furnaces in grey (AFO5 from 2015, all from November 2026)
  map.setPaintProperty('plants', 'fill-extrusion-color', highlight(plantColors(y)));
  document.querySelectorAll('.label[data-since]').forEach(el => { el.style.display = y < +el.dataset.since ? 'none' : ''; });
  const m = GEO.measures;
  const kmPiers = PORT.concessions.features.filter(c => c.properties.since <= y).reduce((t, c) => t + km2(c.geometry.coordinates[0]), 0);
  const km2Text = String(m.area_km2).replace('.', ',');
  $('#measures').hidden = y < 1960;
  $('#measures summary').innerHTML = `<strong>${km2Text} km²</strong><span class="wide"> · ${Math.round(m.area_km2 / m.old_town_km2)} volte la Città vecchia</span>`;
  $('#measures p').innerHTML = `${km2Text} km² è il perimetro a terra dello stabilimento, ${Math.round(m.area_km2 / m.old_town_km2)} volte la Città vecchia (le <a href="https://www.ilpost.it/2026/10/18/ex-ilva-storia/" target="_blank" rel="noopener">fonti ufficiali</a> parlano di circa 15 km²)` +
    `${kmPiers ? `, a cui si aggiungono <strong>${kmPiers.toFixed(1).replace('.', ',')} km²</strong> di moli in concessione nel porto` : ''}. Dentro corrono <strong>${m.rail_km} km</strong> di binari.`;
  map.setPaintProperty('grounds', 'fill-color', phase === 'construction' ? '#b4ae9c' : '#80868b');
  map.setPaintProperty('outline', 'line-dasharray', phase === 'construction' ? [3, 2] : [1, 0]);
  vis('concessions', phase !== 'countryside');
  vis('concessions-outline', phase !== 'countryside');
  map.setFilter('concessions', ['<=', ['get', 'since'], y]);
  map.setFilter('concessions-outline', ['<=', ['get', 'since'], y]);
  map.setPaintProperty('factory', 'fill-extrusion-opacity', phase === 'construction' ? .3 : 1);
  const lit = [...new Set(ev.map(e => e.zone).filter(z => z && z !== 'all'))];
  const filter = ['in', ['get', 'zone'], ['literal', lit]];
  map.setFilter('zones-highlight', filter);
  map.setFilter('zones-outline', filter);
  const plantData = updateAreas(y);
  const whole = (ev.some(e => e.zone === 'all') || plantData) && y >= 1960;
  map.setPaintProperty('outline', 'line-color', whole ? '#a3402a' : '#2b2f33');
  map.setPaintProperty('outline', 'line-width', whole ? 4 : 1);
  map.setPaintProperty('concessions-outline', 'line-color', whole ? '#a3402a' : '#2b2f33');
  map.setPaintProperty('concessions-outline', 'line-width', whole ? 3 : 1);
}

let view = '3d';  // '3d' | 'top'
function showPanel(open) {
  document.body.classList.toggle('map-only', !open);
  const b = $('#full-map'), text = open ? 'Mappa a schermo intero' : 'Mostra i dettagli';
  b.title = text; b.setAttribute('aria-label', text); b.setAttribute('aria-expanded', open);
  b.innerHTML = `<svg viewBox="0 0 20 20" aria-hidden="true"><path d="${open ? 'M3 8V3h5M17 8V3h-5M3 12v5h5M17 12v5h-5' : 'M8 3v5H3M12 3v5h5M8 17v-5H3M12 17v-5h5'}"/></svg>`;
  // the map follows the column during the animation
  const end = performance.now() + (reducedMotion ? 0 : 500);
  // resize clears the canvas: redrawing synchronously avoids a blank frame
  (function step() { map.resize(); map.redraw(); if (performance.now() < end) requestAnimationFrame(step); })();
}
showPanel(true);
$('#full-map').addEventListener('click', () => showPanel(document.body.classList.contains('map-only')));

function setView(v) {
  view = v;
  const duration = reducedMotion ? 0 : 1800;
  if (v === 'top') map.easeTo({ ...map.cameraForBounds(VIEW_2D.bounds, { padding: VIEW_2D.padding, bearing: 0 }), pitch: 0, bearing: 0, duration });
  else map.easeTo({ ...VIEW_3D, duration });
  $('#view').textContent = v === 'top' ? 'Vista 3D' : 'Vista dall\'alto';
  updateMap(year, EVENTS.filter(e => e.year === year));
}
$('#view').addEventListener('click', () => setView(view === 'top' ? '3d' : 'top'));

function production(y) {
  const p = PRODUCTION;
  if (y <= p[0][0]) return 0;
  for (let i = 1; i < p.length; i++)
    if (y <= p[i][0]) return p[i - 1][1] + (p[i][1] - p[i - 1][1]) * (y - p[i - 1][0]) / (p[i][0] - p[i - 1][0]);
  return 0;
}

// dust: from the ore yards towards the south-east (wind from the north-west), intensity ∝ production
const canvas = $('#dust'), ctx = canvas.getContext('2d');
const grain = (() => {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d'), r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, 'rgba(150,72,40,1)'); r.addColorStop(.5, 'rgba(150,72,40,.45)'); r.addColorStop(1, 'rgba(150,72,40,0)');
  g.fillStyle = r; g.fillRect(0, 0, 64, 64);
  return c;
})();
const [PX, PY] = centroid(zoneGeo('yards'));
const MLAT = 1 / 111320, MLON = 1 / (111320 * Math.cos(40.49 * Math.PI / 180));
let particles = [], intensity = 0;

function animateDust() {
  const dpr = devicePixelRatio || 1, w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== w * dpr) { canvas.width = w * dpr; canvas.height = h * dpr; }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  const count = Math.round(intensity * 260);
  while (particles.length < count) particles.push({ t: Math.random(), dx: Math.random() * 400 - 200, dy: Math.random() * 300 - 150 });
  particles.length = count;
  const scale = 2 ** (map.getZoom() - 14);
  // at eye level ground particles next to the camera would fill the screen: keep them a few hundred metres away
  const eye = map.getPitch() > 80 && map.transform.getCameraPosition().lngLat;
  for (const p of particles) {
    if (!reducedMotion) p.t = (p.t + 0.003) % 1;
    // ~1.4 km south-east in one cycle
    const lng = PX + (p.dx + p.t * 1300) * MLON, lat = PY + (p.dy - p.t * 600) * MLAT;
    if (eye && Math.hypot((lng - eye.lng) / MLON, (lat - eye.lat) / MLAT) < 450) continue;
    const q = map.project([lng, lat]);
    // appears quickly, thins out as it spreads; size capped at every zoom
    ctx.globalAlpha = 0.7 * Math.min(1, p.t * 8) * (1 - p.t);
    const r = Math.min(70, Math.max(6, (5 + p.t * 14) * scale));
    ctx.drawImage(grain, q.x - r, q.y - r, 2 * r, 2 * r);
  }
  drawSmoke(scale);
  if (!reducedMotion) requestAnimationFrame(animateDust);
}

// smoke from the stacks with a documented height; illustrative like the dust, same intensity
const smokeSprite = (() => {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d'), r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, 'rgba(228,226,220,.9)'); r.addColorStop(.55, 'rgba(214,212,206,.4)'); r.addColorStop(1, 'rgba(214,212,206,0)');
  g.fillStyle = r; g.fillRect(0, 0, 64, 64);
  return c;
})();
const EMITTERS = PLANTS.features
  .filter(f => f.properties.kind === 'e312' || f.properties.kind === 'furnace'
    || (f.properties.kind === 'stack' && f.properties.official && /^E42[2-5]$/.test(f.properties.code)))
  .map(f => ({ ...f.properties, at: centroid({ geometry: { coordinates: [f.geometry.coordinates] } }), puffs: [] }));
// MapLibre projects only ground points: a no-op custom layer hands over the 3D matrix of every frame
let projection = null;
const project3d = (lng, lat, metres) => {
  const m = projection, c = maplibregl.MercatorCoordinate.fromLngLat([lng, lat], metres);
  const w = m[3] * c.x + m[7] * c.y + m[11] * c.z + m[15];
  if (w <= 0) return null;
  return { x: ((m[0] * c.x + m[4] * c.y + m[8] * c.z + m[12]) / w + 1) / 2 * canvas.clientWidth,
           y: (1 - (m[1] * c.x + m[5] * c.y + m[9] * c.z + m[13]) / w) / 2 * canvas.clientHeight };
};
function drawSmoke() {
  if (!projection) return;
  const phase = era(year)[1];
  for (const e of EMITTERS) {
    const on = phase === 'active' && (e.since || 1965) <= year && !(e.stopped <= year);
    const count = on ? Math.round(intensity * 22) : 0;
    while (e.puffs.length < count) e.puffs.push({ t: Math.random(), jx: Math.random() * 40 - 20, jy: Math.random() * 40 - 20 });
    e.puffs.length = count;
    for (const p of e.puffs) {
      if (!reducedMotion) p.t = (p.t + 0.0025) % 1;
      // rises ~250 m above the top while the wind carries it ~800 m south-east
      const lng = e.at[0] + (p.jx + p.t * 700) * MLON, lat = e.at[1] + (p.jy - p.t * 330) * MLAT, z = e.h + 10 + p.t * 250;
      const q = project3d(lng, lat, z), q2 = q && project3d(lng + (12 + p.t * 90) * MLON, lat, z);
      if (!q2) continue;
      const r = Math.min(140, Math.max(3, Math.hypot(q2.x - q.x, q2.y - q.y)));
      ctx.globalAlpha = 0.55 * Math.min(1, p.t * 6) * (1 - p.t);
      ctx.drawImage(smokeSprite, q.x - r, q.y - r, 2 * r, 2 * r);
    }
  }
}
if (reducedMotion) map.on('render', animateDust);

// panel
function sourcesHtml(f) {
  return `<div class="sources">Fonte: ${f.map(([t, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)}</a>`).join(' · ')}</div>`;
}

// year-by-year data in the band, on the same scale as the timeline
const counts = {};
WORK_DEATHS.forEach(m => { counts[m.year] = (counts[m.year] || 0) + 1; });
const NISTRI = { 1961: 18, 1962: 28, 1963: 23, 1964: 32 };
const num = (v, d = 1) => v.toLocaleString('it', { maximumFractionDigits: d });
const ROWS = [
  // scaled to recent years: the construction-site bars (up to 32) are cut, the value is in the label
  { name: 'Morti sul lavoro', cap: 4, total: 'in tutto 208', detail: `208 dal 1961 al 2019 secondo la stampa; ${WORK_DEATHS.length} nell'elenco nominativo dal 2003`,
    values: { ...NISTRI, ...counts }, fmt: v => v === 1 ? '1 morto' : v + ' morti',
    empty: a => a >= 2003 ? 'nessuno' : 'nessun elenco', note: a => NISTRI[a] ? ', secondo lo storico R. Nistri' : '' },
  { name: 'PM10 ai Tamburi', values: AIR.series['machiavelli|PM10'], fmt: v => num(v) + ' µg/m³' },
  { name: 'PM10 a Talsano', values: AIR.series['talsano|PM10'], fmt: v => num(v) + ' µg/m³' },
  { name: 'Polveri emesse', values: EMISSIONS.pm10.values, fmt: v => num(v, 0) + ' t' },
  { name: 'Diossine emesse', values: EMISSIONS.dioxins.values, fmt: v => num(v) + ' g TEQ' },
  { name: 'Acciaio prodotto', values: Object.fromEntries(PRODUCTION.filter(p => p[1] > 0)), fmt: v => num(v) + ' Mt' },
];
// the two PM10 stations on the same scale, to compare them
const MAX_PM10 = Math.max(...Object.values(ROWS[1].values), ...Object.values(ROWS[2].values));
function drawData() {
  const H = 22;
  $('#data-rows').innerHTML = ROWS.map((r, i) => {
    const max = r.cap || (i === 1 || i === 2 ? MAX_PM10 : Math.max(...Object.values(r.values)));
    const bars = Object.entries(r.values).map(([a, v]) => {
      const x0 = pct(+a - 0.5) * 10, x1 = pct(+a + 0.5) * 10, w = Math.max(2, (x1 - x0) * 0.7), h = Math.max(1.5, Math.min(1, v / max) * H);
      const cut = v > max ? `<rect class="cut" x="${(x0 + x1 - w) / 2 - 1}" y="4" width="${w + 2}" height="2"/>` : '';
      return `<rect data-year="${a}" x="${(x0 + x1 - w) / 2}" y="${H - h}" width="${w}" height="${h}"${r.note && r.note(+a) ? ' class="other"' : ''}><title>${a}: ${r.fmt(v)}${r.note ? r.note(+a) : ''}</title></rect>` + cut;
    }).join('');
    return `<div class="row"><span class="name"${r.detail ? ` title="${r.detail}"` : ''}>${r.name}${r.total ? ` <span class="total">(${r.total})</span>` : ''}</span><span class="value"></span></div>
      <svg class="strip" viewBox="0 0 1000 ${H}" preserveAspectRatio="none" aria-hidden="true"><line x1="0" x2="1000" y1="${H}" y2="${H}"/>${bars}</svg>`;
  }).join('');
}
function updateData(y) {
  $('#data-year').textContent = `Valori del ${y}`;
  document.querySelectorAll('#data-rows .value').forEach((el, i) => {
    const r = ROWS[i], v = r.values[y];
    el.textContent = v != null ? r.fmt(v) : r.empty ? r.empty(y) : 'nessun dato';
    el.classList.toggle('missing', v == null);
  });
  document.querySelectorAll('#data-rows rect').forEach(el => el.classList.toggle('selected', +el.dataset.year === y));
}

// the column keeps only the names, in the years that have them
function deathNames(y) {
  const deaths = WORK_DEATHS.filter(m => m.year === y);
  $('#deaths-title').hidden = !deaths.length;
  return deaths.length ? `<ul class="names">${deaths.map(m => `<li><strong>${esc(m.name)}</strong>${m.age ? ', ' + m.age + ' anni' : ''}, ${esc(m.date)}${m.contractor ? ', ditta esterna' : ''}. ${esc(m.circumstances)}${sourcesHtml(m.sources)}</li>`).join('')}</ul>${sourcesHtml([WORK_DEATHS_SOURCE])}` : '';
}

function lastBefore(y) {
  const e = EVENTS.filter(e => e.year < y).pop();
  return `<p class="empty">Nessun evento in elenco per il ${y}.${e ? ` L'ultimo prima: ${esc(e.date)}, «${esc(e.title)}».` : ''}</p>`;
}

function show(y) {
  year = y;
  const [, phase, , long] = era(y);
  mapEl.dataset.phase = phase;
  $('#big-year').textContent = y;
  $('#phase').innerHTML = `${y}<small>${esc(y >= 2026 ? 'Area a caldo ferma per ordine dei giudici' : long)}</small>`;

  const ev = EVENTS.filter(e => e.year === y);
  $('#events').innerHTML = ev.length ? ev.map(e => `<article class="event" id="ev-${EVENTS.indexOf(e)}" tabindex="-1" style="--c:${COLORS[e.category]}">
      <div class="date">${esc(e.date)}</div><h3>${esc(e.title)}</h3><p>${esc(e.text)}</p>${sourcesHtml(e.sources)}</article>`).join('')
    : lastBefore(y);

  const per = PERIODS.filter(p => y >= p.from && y <= p.to && !p.mapOnly);
  $('#periods').innerHTML = per.length ? per.map(p => `<div class="period" data-kind="${p.kind}" data-area="${p.area || ''}">
      <div class="value">${esc(p.value)}</div>
      <div class="title">${esc(capitalize(p.title))} <span class="kind">${KIND_LABELS[p.kind]}</span></div>
      <div class="note">${p.from === p.to ? p.from : p.from + '–' + p.to}. ${esc(p.note)}</div>${sourcesHtml(p.sources)}</div>`).join('') : '';
  $('#periods-title').hidden = !per.length;

  $('#deaths').innerHTML = deathNames(y);
  updateData(y);

  updateMap(y, ev);
  intensity = y >= 2026 ? 0 : production(y) / 10 * (y >= 2020 ? 0.35 : 1);
  if (reducedMotion) map.triggerRepaint();

  // timeline
  const axis = $('#axis');
  axis.setAttribute('aria-valuenow', y);
  axis.setAttribute('aria-valuetext', `${y}, ${ev.length} eventi`);
  $('#indicator').style.left = pct(y) + '%';
  // at the ends the tag stays inside the axis; its tip stays on the year
  const tag = $('#indicator span'), W = $('#axis').clientWidth, x = pct(y) / 100 * W, w = tag.offsetWidth || 40;
  const shift = Math.min(Math.max(x - w / 2, 0), W - w) - (x - w / 2);
  tag.style.transform = `translateX(calc(-50% + ${shift}px))`;
  $('#indicator span').textContent = y;
  // the red tag already shows the selected year: hide the grey label below it
  document.querySelectorAll('#ticks span').forEach(el => { el.style.opacity = +el.dataset.year === y ? 0 : ''; });
  document.querySelectorAll('.mark').forEach(m => m.classList.toggle('active', +m.dataset.year === y));
  history.replaceState(null, '', '#' + y);
}

// building the timeline
const preview = $('#preview');
function showPreview(el, html, color) {
  preview.innerHTML = html;
  preview.style.setProperty('--c', color);
  preview.hidden = false;
  const r = el.getBoundingClientRect(), box = $('#timeline').getBoundingClientRect();
  const x = Math.min(Math.max(r.left + r.width / 2 - box.left - 150, 8), box.width - 308);
  preview.style.left = x + 'px';
  preview.style.top = (r.bottom - box.top + 10) + 'px';
}
const hidePreview = () => { preview.hidden = true; };
const firstSentence = t => t.split(/(?<=\.)\s/)[0];

// one mark per year: a coloured stripe per event, stacked from the bottom
const eventYears = [...new Set(EVENTS.map(e => e.year))];
for (const y of eventYears) {
  const ev = EVENTS.filter(e => e.year === y);
  const b = document.createElement('button');
  b.className = 'mark';
  b.type = 'button';
  b.dataset.year = y;
  b.style.left = pct(y) + '%';
  b.style.height = (ev.length * 6 - 1) + 'px';  // ends with the last stripe, so the focus ring stays even
  b.style.background = `linear-gradient(to top, ${ev.map((e, k) => `${COLORS[e.category]} ${k * 6}px ${k * 6 + 5}px, var(--bar) ${k * 6 + 5}px ${k * 6 + 6}px`).join(', ')})`;
  b.setAttribute('aria-label', `${y}: ` + ev.map(e => e.title).join('; '));
  const html = ev.length === 1
    ? `<div class="cat" style="color:${COLORS[ev[0].category]}">${CATEGORIES[ev[0].category]}</div><div class="date">${esc(ev[0].date)}</div>
       <h3>${esc(ev[0].title)}</h3><p>${esc(firstSentence(ev[0].text))}</p><div class="action">Clicca per aprire</div>`
    : `<div class="date">${y}: ${ev.length} eventi</div><ul class="list">${ev.map(e =>
        `<li style="--c:${COLORS[e.category]}"><span>${esc(e.date)}</span>${esc(e.title)}</li>`).join('')}</ul><div class="action">Clicca per aprire l'anno</div>`;
  const open = () => showPreview(b, html, COLORS[ev[0].category]);
  b.addEventListener('pointerenter', open);
  b.addEventListener('focus', open);
  b.addEventListener('pointerleave', hidePreview);
  b.addEventListener('blur', hidePreview);
  b.addEventListener('click', e => {
    e.stopPropagation();
    hidePreview();
    show(y);
    showPanel(true);
    const art = document.querySelector('.event');
    art.scrollIntoView({ block: 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
    document.querySelectorAll('.event').forEach(x => { x.classList.remove('flash'); void x.offsetWidth; x.classList.add('flash'); });
  });
  $('#marks').append(b);
}

ERAS.forEach(([from, , short, long], i) => {
  const to = (ERAS[i + 1] ? ERAS[i + 1][0] : MAX + 1);
  $('#eras').insertAdjacentHTML('beforeend',
    `<div class="era" style="left:${pct(from - 0.5)}%;width:${pct(to - 0.5) - pct(from - 0.5)}%" title="${esc(long)}, ${from}–${to - 1}">${esc(short)}</div>`);
});


// labels: the years with events; long gaps show how many years they skip
for (const y of [...EVENT_YEARS].sort()) $('#ticks').insertAdjacentHTML('beforeend', `<span data-year="${y}" style="left:${pct(y)}%">${y}</span>`);
// on narrow screens, labels touching the previous one are hidden
function thinTicks() {
  let end = -Infinity;
  for (const el of document.querySelectorAll('#ticks span')) {
    el.style.visibility = '';
    const r = el.getBoundingClientRect();
    if (r.left < end + 4) el.style.visibility = 'hidden'; else end = r.right;
  }
}
thinTicks();
addEventListener('resize', thinTicks);
for (let y = MIN; y <= MAX; ) {
  if (EVENT_YEARS.has(y)) { y++; continue; }
  let end = y; while (end + 1 <= MAX && !EVENT_YEARS.has(end + 1)) end++;
  if (end - y + 1 >= 5)
    $('#marks').insertAdjacentHTML('beforeend', `<span class="gap" style="left:${(pct(y - 0.5) + pct(end + 0.5)) / 2}%" title="${y}–${end}: nessun evento in elenco">${end - y + 1} anni</span>`);
  y = end + 1;
}

// dragging and keyboard on the axis
const axis = $('#axis');
const yearFromX = x => {
  const r = axis.getBoundingClientRect(), u = (x - r.left) / r.width * TOTAL;
  for (let y = MIN; y <= MAX; y++) if (u < START[y] + WEIGHT[y]) return y;
  return MAX;
};
let dragging = false;
drawData();
updateData(year);
$('#expand').addEventListener('click', () => {
  const expanded = $('#timeline').classList.toggle('expanded');
  $('#expand').setAttribute('aria-expanded', expanded);
});
// on the rows: values of the year under the pointer, click to select it
$('#data-rows').addEventListener('pointermove', e => { if (e.target.closest('.strip')) updateData(yearFromX(e.clientX)); });
$('#data-rows').addEventListener('pointerleave', () => updateData(year));
$('#data-rows').addEventListener('click', e => { if (e.target.closest('.strip')) show(yearFromX(e.clientX)); });
axis.addEventListener('pointerdown', e => {
  if (e.target.closest('.mark')) return;
  dragging = true; axis.setPointerCapture(e.pointerId); show(yearFromX(e.clientX));
});
axis.addEventListener('pointermove', e => { if (dragging && yearFromX(e.clientX) !== year) show(yearFromX(e.clientX)); });
axis.addEventListener('pointerup', () => { dragging = false; });
axis.addEventListener('keydown', e => {
  const steps = { ArrowLeft: -1, ArrowRight: 1, ArrowDown: -1, ArrowUp: 1, PageDown: -10, PageUp: 10 };
  let y = e.key === 'Home' ? MIN : e.key === 'End' ? MAX : steps[e.key] ? year + steps[e.key] : null;
  if (y === null) return;
  e.preventDefault();
  show(Math.min(MAX, Math.max(MIN, y)));
});

// without a year in the address, open on the first year of the working plant
show(Math.min(MAX, Math.max(MIN, +location.hash.slice(1) || 1965)));
if (!reducedMotion) animateDust();
