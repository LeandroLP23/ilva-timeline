"""Builds map-data.js (window.GEO, GeoJSON for MapLibre) from the OSM data in osm.json and osm-city.json."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
LON0, LON1, LAT0, LAT1 = 17.140, 17.310, 40.440, 40.545
COSL = math.cos(math.radians(40.49))
M_PER_DEG = 111_320

PLANT = 11843712
SEA = {8692680, 16846869, 149577191, 173656994}
ISLANDS = {16846864, 16846866, 10272008}
ZONE_WAYS = {177628163: 'yards', 383684811: 'steelshop', 383684829: 'steelshop', 6251142: 'mills',
             383685754: 'mills', 383685847: 'mills'}
# ponytail: outlines traced by hand on the 2019 orthophoto (SIT Puglia) and from Nominatim; indicative, not cadastral
MANUAL = {
    'hot': [(40.5111, 17.2134), (40.5108, 17.2217), (40.4972, 17.2237), (40.4911, 17.2138),
            (40.4985, 17.2060), (40.5040, 17.2044), (40.5095, 17.2115)],
    'tamburi': [(40.4990, 17.2250), (40.4990, 17.2330), (40.4900, 17.2360), (40.4845, 17.2300),
                (40.4850, 17.2215), (40.4920, 17.2200)],
}
LABELS = [('Tamburi', 40.4948, 17.2290, 'place'), ('Paolo VI', 40.5235, 17.2780, 'place'),
          ('Mar Piccolo', 40.4930, 17.2620, 'water'), ('Mar Grande', 40.4640, 17.2050, 'water'),
          ('Città vecchia', 40.4745, 17.2420, 'place'), ('Statte', 40.5300, 17.2050, 'place'),
          # plant units: OSM names (ACC/1, ACC/2, TNA/1, Parchi Minerali); hot area at the centre of the manual outline
          ('Acciaieria 1', 40.5032, 17.2067, 'unit'), ('Acciaieria 2', 40.5199, 17.2079, 'unit'),
          ('Laminatoi', 40.5104, 17.2038, 'unit'), ('Parchi minerali', 40.4988, 17.2203, 'unit'),
          ('Area a caldo', 40.5055, 17.2165, 'unit')]


def clip(ring):
    """Sutherland-Hodgman against the view rectangle, in lon/lat."""
    edges = [(lambda p: p[0] >= LON0, lambda a, b: (LON0, a[1] + (b[1] - a[1]) * (LON0 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[0] <= LON1, lambda a, b: (LON1, a[1] + (b[1] - a[1]) * (LON1 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[1] >= LAT0, lambda a, b: (a[0] + (b[0] - a[0]) * (LAT0 - a[1]) / (b[1] - a[1]), LAT0)),
             (lambda p: p[1] <= LAT1, lambda a, b: (a[0] + (b[0] - a[0]) * (LAT1 - a[1]) / (b[1] - a[1]), LAT1))]
    for inside, cut in edges:
        if not ring:
            break
        out, prev = [], ring[-1]
        for cur in ring:
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
            prev = cur
        ring = out
    return ring


def ring(pts, clipped=False):
    r = [(round(p['lon'], 6), round(p['lat'], 6)) for p in pts]
    if clipped:
        r = [(round(x, 6), round(y, 6)) for x, y in clip(r)]
    if len(r) < 3:
        return None
    if r[0] != r[-1]:
        r.append(r[0])
    return r


def area_m2(r):
    s = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(r, r[1:]))
    return abs(s) / 2 * (M_PER_DEG ** 2) * COSL


def circle(lat, lon, radius_m, n=10):
    dlat, dlon = radius_m / M_PER_DEG, radius_m / (M_PER_DEG * COSL)
    r = [(round(lon + dlon * math.cos(2 * math.pi * i / n), 6), round(lat + dlat * math.sin(2 * math.pi * i / n), 6)) for i in range(n)]
    return r + [r[0]]


def join_ways(ways):
    segs = [list(w) for w in ways if w]
    rings = []
    while segs:
        r = segs.pop()
        changed = True
        while changed and (r[0]['lat'], r[0]['lon']) != (r[-1]['lat'], r[-1]['lon']):
            changed = False
            end = (r[-1]['lat'], r[-1]['lon'])
            for i, s in enumerate(segs):
                if (s[0]['lat'], s[0]['lon']) == end:
                    r += s[1:]
                elif (s[-1]['lat'], s[-1]['lon']) == end:
                    r += s[::-1][1:]
                else:
                    continue
                segs.pop(i)
                changed = True
                break
        rings.append(r)
    return rings


def rings_of(e):
    if e['type'] == 'way':
        return [e['geometry']]
    return join_ways([m['geometry'] for m in e.get('members', []) if m['type'] == 'way' and 'geometry' in m])


def poly(rings, props, clipped=False):
    rs = [r for r in (ring(x, clipped) for x in rings) if r]
    if not rs:
        return None
    # the OSM multipolygons here have outer rings only: each becomes a polygon
    return {'type': 'Feature', 'properties': props, 'geometry': {'type': 'MultiPolygon', 'coordinates': [[r] for r in rs]}}


def line(pts, props):
    return {'type': 'Feature', 'properties': props,
            'geometry': {'type': 'LineString', 'coordinates': [(round(p['lon'], 6), round(p['lat'], 6)) for p in pts]}}


def factory_height(kind, area):
    # ponytail: OSM has no heights for the plant; estimates by kind and footprint, to replace with real data
    if kind == 'silo':
        return 30
    if kind == 'tank':
        return 16
    if kind == 'canopy':
        return 10
    if area > 20000:
        return 32
    if area > 5000:
        return 24
    if area > 1000:
        return 15
    return 8


def city_height(t):
    try:
        if 'height' in t:
            return float(str(t['height']).replace('m', '').strip())
        if 'building:levels' in t:
            return float(t['building:levels']) * 3.2
    except ValueError:
        pass
    return 12 if t.get('building') in ('apartments', 'residential', 'yes') else 6


def load_lidar():
    """Heights measured by build_heights.py (2008-2010 laser survey), if already computed."""
    p = os.path.join(HERE, 'heights.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'factory': {}, 'city': {}}


def choose(lidar, estimate):
    # below 2.5 m the survey does not see the building (built after 2010 or covered): keep the estimate
    return (lidar, 'lidar') if lidar is not None and lidar >= 2.5 else (estimate, 'estimate')


def main():
    LIDAR = load_lidar()
    base = json.load(open(os.path.join(HERE, 'osm.json'), encoding='utf-8'))['elements']
    city = json.load(open(os.path.join(HERE, 'osm-city.json'), encoding='utf-8'))['elements']
    seen = {e['id'] for e in base}
    G = {k: [] for k in ['sea', 'islands', 'plant', 'factory', 'stacks', 'rail', 'roads', 'city', 'zones']}

    for e in base:
        t, i = e.get('tags', {}), e['id']
        if i in SEA:
            G['sea'].append(poly(rings_of(e), {}, clipped=True))
        elif i in ISLANDS:
            G['islands'].append(poly(rings_of(e), {}))
        elif i == PLANT:
            G['plant'].append(poly(rings_of(e), {}))
        elif t.get('man_made') == 'chimney':
            lat, lon = (e['lat'], e['lon']) if e['type'] == 'node' else (e['geometry'][0]['lat'], e['geometry'][0]['lon'])
            G['stacks'].append({'type': 'Feature', 'properties': {'h': 90},
                                'geometry': {'type': 'Polygon', 'coordinates': [circle(lat, lon, 4)]}})
        elif 'building' in t or t.get('man_made') in ('silo', 'storage_tank', 'water_tower', 'cooling'):
            mm = t.get('man_made')
            kind = {'silo': 'silo', 'storage_tank': 'tank', 'water_tower': 'tank', 'cooling': 'tank'}.get(mm) \
                or {'roof': 'canopy', 'shed': 'shed'}.get(t.get('building'), 'industrial')
            if e['type'] == 'node':
                r = circle(e['lat'], e['lon'], 6)
                f = {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [r]}}
                a = area_m2(r)
            else:
                f = poly(rings_of(e), {})
                if not f:
                    continue
                a = area_m2(f['geometry']['coordinates'][0][0])
            h, h_source = choose(LIDAR['factory'].get(str(e['id'])), factory_height(kind, a))
            f['properties'] = {'kind': kind, 'h': h, 'hsource': h_source, 'id': e['id'], 'name': t.get('name', ''),
                               'area': round(a)}
            G['factory'].append(f)
        elif e['type'] == 'way' and t.get('railway') == 'rail':
            G['rail'].append(line(e['geometry'], {}))
        elif e['type'] == 'way' and t.get('man_made') == 'goods_conveyor':
            G['rail'].append(line(e['geometry'], {'conveyor': 1}))
        elif e['type'] == 'way' and 'highway' in t:
            G['roads'].append(line(e['geometry'], {'major': int(t['highway'] in ('motorway', 'trunk', 'primary'))}))
        if i in ZONE_WAYS:
            G['zones'].append(poly(rings_of(e), {'zone': ZONE_WAYS[i]}))

    tamburi = [(b, a) for a, b in MANUAL['tamburi']]

    def inside(x, y, polygon):
        d = False
        for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                d = not d
        return d

    for e in city:
        if e['id'] not in seen and e['type'] == 'way':
            h, h_source = choose(LIDAR['city'].get(str(e['id'])), round(city_height(e.get('tags', {})), 1))
            f = poly([e['geometry']], {'h': h, 'hsource': h_source, 'id': e['id']})
            if f:
                r = f['geometry']['coordinates'][0][0]
                cx, cy = sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r)
                f['properties']['tamburi'] = int(inside(cx, cy, tamburi))
                G['city'].append(f)

    for name, pts in MANUAL.items():
        G['zones'].append(poly([[{'lat': a, 'lon': b} for a, b in pts]], {'zone': name}))

    out = {k: {'type': 'FeatureCollection', 'features': [f for f in v if f]} for k, v in G.items()}
    rail_m = sum(math.hypot((b[0] - a[0]) * M_PER_DEG * COSL, (b[1] - a[1]) * M_PER_DEG)
                 for f in out['rail']['features'] if 'conveyor' not in f['properties']
                 for a, b in zip(f['geometry']['coordinates'], f['geometry']['coordinates'][1:]))
    surface = sum(area_m2(p[0]) for f in out['plant']['features'] for p in f['geometry']['coordinates'])
    borgo = next(e for e in base if e['id'] == 10272008)
    old_town = area_m2(ring(borgo['geometry']))
    out['measures'] = {'area_km2': round(surface / 1e6, 1), 'rail_km': round(rail_m / 1000),
                       'old_town_km2': round(old_town / 1e6, 2)}
    out['labels'] = [{'text': n, 'lat': a, 'lon': b, 'kind': k} for n, a, b, k in LABELS]
    out['bounds'] = [[LON0, LAT0], [LON1, LAT1]]
    with open(os.path.join(HERE, 'map-data.js'), 'w', encoding='utf-8') as fh:
        fh.write('// Generated by build_map.py. Data © OpenStreetMap contributors (ODbL). Plant heights estimated.\n')
        fh.write('window.GEO=' + json.dumps(out, separators=(',', ':'), ensure_ascii=False) + ';\n')
    print('map-data.js', os.path.getsize(os.path.join(HERE, 'map-data.js')) // 1024, 'KB;',
          {k: len(v['features']) for k, v in out.items() if isinstance(v, dict) and 'features' in v}, out['measures'])


if __name__ == '__main__':
    main()
