"""Builds plants.js: the large plants in 3D (yard domes, blast furnaces, gasholders, stack E312).

Positions surveyed on the 2023 orthophoto of Regione Puglia (BaseMaps/Ortofoto2023 service),
in EPSG:3857 coordinates. Sizes: ore yard domes 77 m high (EIA documentation, MASE); stack E312 210 m
(form B.6, AIA 2011, MASE document 260236). Other heights estimated.
Blast furnace numbering: AIA site plan B.20 (MASE doc. 260022) aligned to the photo; stacks
E111/E134 (AFO1), E112/E135 (AFO2), E114/E137 (AFO4), E116/E138 (AFO5) fall 23-108 m from the furnaces.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = 6378137
K = math.cos(math.radians(40.5))  # real metres per EPSG:3857 unit at this latitude


def lonlat(x, y):
    return [round(x / R * 180 / math.pi, 6), round((2 * math.atan(math.exp(y / R)) - math.pi / 2) * 180 / math.pi, 6)]


def from_crop(x0, ytop, scale, px, py):
    """Pixel of an orthophoto crop -> EPSG:3857."""
    return x0 + px * scale, ytop - py * scale


# crops used (EPSG:3857 bbox, 1400x1274 px or 800x800 px)
Q2 = (1916142, 4940626, 1.0336)
Q3 = (1916142, 4939308, 1.0336)
ZA = (1915469, 4939309, 0.65)
ZE = (1916016, 4939976, 0.65)

# domes: corners clockwise, from crops Q3 (ore yard) and Q2 (coal yard)
# which yard is which: PARCO FOSSILE / PARCO MINERALE captions on the aligned B.20; the third cover
# (north-east) is an open yard with grey piles in 2019 and covered in 2022: yard not identified
DOMES = [
    ('coal', 77, 2022, Q3, [(240, 548), (742, 205), (925, 478), (445, 828)]),
    ('ore', 77, 2020, Q3, [(445, 840), (950, 500), (1135, 770), (612, 1122)]),
    ('other', 45, 2022, Q2, [(630, 680), (755, 598), (1055, 1030), (930, 1100)]),
]
# blast furnaces: name, start year (AFO4 and AFO5 from the 1970-75 doubling), stop year, furnace, cowpers
# heights from the 2008-2010 laser survey (peak within 25 m of the furnace); AFO5: no attributable peak
H_AFO = {'AFO1': 83.9, 'AFO2': 82.7, 'AFO4': 90.3}
FURNACES = [('AFO1', 1965, 2026, ZA, (430, 450), (330, 505)), ('AFO2', 1965, 2026, ZA, (590, 320), (520, 370)),
            ('AFO4', 1975, 2026, ZE, (370, 440), (250, 428)), ('AFO5', 1975, 2015, ZE, (585, 150), (520, 125))]
# gasholder heights from the laser survey (peak within 25 m), same order
H_GASHOLDERS = [82.5, 57.9, 72.9, 80.1]
GASHOLDERS = [(ZE, (690, 580), 37), (Q2, (-215, 1003), 31), (ZA, (130, 575), 21), (ZA, (200, 660), 21)]
E312 = (Q2, (893, 288))


def merc(lon, lat):
    return lon * math.pi / 180 * R, math.log(math.tan(math.pi / 4 + lat * math.pi / 360)) * R


def axes(ring):
    """Length, width (m), orientation (degrees) and centre of a polygon, from its principal axes."""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    a = 0.5 * math.atan2(2 * sxy, sxx - syy)
    u = [(x - mx) * math.cos(a) + (y - my) * math.sin(a) for x, y in ring]
    v = [-(x - mx) * math.sin(a) + (y - my) * math.cos(a) for x, y in ring]
    return (max(u) - min(u)) * K, (max(v) - min(v)) * K, math.degrees(a), (mx, my)


def circle(cx, cy, r_m, n=18):
    r = r_m / K
    pts = [lonlat(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return [pts + [pts[0]]]


def polygon(pts):
    p = [lonlat(x, y) for x, y in pts]
    return [p + [p[0]]]


def f(geom, **props):
    return {'type': 'Feature', 'properties': props, 'geometry': {'type': 'Polygon', 'coordinates': geom}}


def vault(corners, high, eaves=14, slices=7):
    """Barrel vault approximated by ever narrower and higher bands."""
    a, b, c, d = corners  # a-d and b-c are the short sides (ends)
    for k in range(slices):
        x = 1 - k / slices  # fraction of the width
        h = max(eaves, high * math.sqrt(max(0.0, 1 - x * x)))
        t = (1 - x) / 2
        lerp = lambda p, q: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
        yield [lerp(a, d), lerp(b, c), lerp(c, b), lerp(d, a)], h


def convex_hull(pts):
    """Convex hull (monotone chain), counter-clockwise."""
    pts = sorted(set(pts))
    turn = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def clip(subject, convex):
    """Sutherland-Hodgman: `subject` (possibly non-convex) inside the counter-clockwise convex polygon `convex`."""
    inside = lambda p, a, b: (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
    def intersect(p, q, a, b):
        dx, dy, ex, ey = q[0] - p[0], q[1] - p[1], b[0] - a[0], b[1] - a[1]
        t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / (dx * ey - dy * ex)
        return (p[0] + t * dx, p[1] + t * dy)
    out = subject
    for a, b in zip(convex, convex[1:] + convex[:1]):
        entering, out = out, []
        for p, q in zip(entering, entering[1:] + entering[:1]):
            if inside(q, a, b):
                if not inside(p, a, b):
                    out.append(intersect(p, q, a, b))
                out.append(q)
            elif inside(p, a, b):
                out.append(intersect(p, q, a, b))
    return out


def hot_area(feats, geo, margin=60):
    """Yards, coke ovens, sinter plant and blast furnaces: hull of the plants widened by `margin` m, inside the perimeter."""
    k = math.cos(math.radians(40.5))
    pts = []
    for ft in feats:
        if ft['properties']['kind'] in ('furnace', 'cowper', 'casthouse', 'gasholder', 'battery', 'dome', 'e312'):
            g = ft['geometry']
            rings = [g['coordinates'][0]] if g['type'] == 'Polygon' else [p[0] for p in g['coordinates']]
            pts += [tuple(p) for a in rings for p in a]
    for z in geo['zones']['features']:
        if z['properties']['zone'] == 'yards':
            g = z['geometry']
            rings = [g['coordinates'][0]] if g['type'] == 'Polygon' else [p[0] for p in g['coordinates']]
            pts += [tuple(p) for a in rings for p in a]
    wide = [(x + margin * math.cos(t) / (111320 * k), y + margin * math.sin(t) / 111320)
            for x, y in convex_hull(pts) for t in (i * math.pi / 6 for i in range(12))]
    perimeter = [tuple(p) for p in geo['plant']['features'][0]['geometry']['coordinates'][0][0][:-1]]
    ring = [[round(x, 6), round(y, 6)] for x, y in clip(perimeter, convex_hull(wide))]
    return ring + [ring[0]]


def main():
    feats = []
    lidar = json.load(open(os.path.join(HERE, 'heights.json'), encoding='utf-8'))
    for yard, high, start, (x0, yt, s), px in DOMES:
        corners = [from_crop(x0, yt, s, *p) for p in px]
        for pts, h in vault(corners, high):
            feats.append(f(polygon(pts), kind='dome', yard=yard, h=round(h, 1), since=start, group='dome-' + yard))
        # the piles before the domes are measured on the LiDAR DTM: build_reliefs.py

    labels = []
    for name, start, stopped, (x0, yt, s), furnace, cowper in FURNACES:
        fx, fy = from_crop(x0, yt, s, *furnace)
        cx, cy = from_crop(x0, yt, s, *cowper)
        feats.append(f(circle(fx, fy, 11), kind='furnace', name=name, h=H_AFO.get(name, 85), measured=name in H_AFO,
                       since=start, stopped=stopped, group=name))
        feats.append(f(circle(fx, fy, 22), kind='casthouse', name=name, h=28, since=start, group=name))
        labels.append({'text': name, 'lonlat': lonlat(fx, fy), 'kind': 'unit', 'since': start})
        dx, dy = (cx - fx), (cy - fy)
        n = math.hypot(dx, dy) or 1
        px_, py_ = -dy / n, dx / n  # row perpendicular to the furnace -> cowper direction
        for i in range(4):
            off = (i - 1.5) * 16 / K
            feats.append(f(circle(cx + px_ * off, cy + py_ * off, 5.5), kind='cowper', name=name, h=50, since=start, group=name))

    for ((x0, yt, s), p, r), h in zip(GASHOLDERS, H_GASHOLDERS):
        x, y = from_crop(x0, yt, s, *p)
        feats.append(f(circle(x, y, r), kind='gasholder', h=h, measured=True))

    (x0, yt, s), p = E312
    x, y = from_crop(x0, yt, s, *p)
    feats.append(f(circle(x, y, 9), kind='e312', h=210, code='E312', process='agglomerazione linee D-E', official=True))

    # stacks of the AIA site plan with the height from form B.6 (sources/aia/build_stacks.py)
    stacks = json.load(open(os.path.join(HERE, 'sources', 'aia', 'stacks.json'), encoding='utf-8'))
    for k, c in enumerate(stacks):
        if (c['code'] or '').startswith('E312'):
            continue
        if (c['code'] or '').endswith('?'):
            c = {**c, 'code': None, 'h': None, 'process': None}
        peak = lidar['stacks'].get(str(k))
        lon, lat = c['lon'], c['lat']
        if peak and c['h'] and abs(peak['h'] - c['h']) <= 0.2 * c['h']:
            lon, lat = peak['lon'], peak['lat']  # the survey confirms the stack: use its exact position
        elif peak and not c['h'] and peak['h'] >= 15:
            lon, lat = peak['lon'], peak['lat']
            c = {**c, 'h_measured': peak['h']}
        cx, cy = merc(lon, lat)
        h = c['h'] or c.get('h_measured') or 30
        feats.append(f(circle(cx, cy, max(2.2, h / 22), 10), kind='stack', h=h, official=bool(c['h']),
                       code=c['code'] or '', process=c['process'] or '', since=c['since']))

    # coke oven batteries: long narrow OSM buildings, oriented like the batteries, near the coking stacks
    geo = open(os.path.join(HERE, 'map-data.js'), encoding='utf-8').read()
    geo = json.loads(geo[geo.index('=') + 1:geo.rindex(';')])
    cok = [merc(c['lon'], c['lat']) for c in stacks if (c['code'] or '').rstrip('?') in ('E422', 'E423', 'E424', 'E425', 'E426')]
    batteries = []
    for b in geo['factory']['features']:
        if b['geometry']['type'] != 'MultiPolygon':
            continue
        ring = [merc(*p) for p in b['geometry']['coordinates'][0][0]]
        L, W, ang, (mx, my) = axes(ring)
        near = min(math.hypot(mx - a, my - c) for a, c in cok) * K
        if near < 320 and L > 60 and 8 < W < 32 and L / W > 3 and abs(((ang - 35) + 90) % 180 - 90) < 15:
            batteries.append(b['properties']['id'])
            h = lidar['factory'].get(str(b['properties']['id']))
            feats.append({'type': 'Feature', 'properties': {'kind': 'battery', 'h': h if h and h >= 2.5 else 30,
                          'measured': bool(h and h >= 2.5), 'since': 1965}, 'geometry': b['geometry']})

    labels += [
        {'text': 'Camino E312 (210 m)', 'lonlat': lonlat(x, y), 'kind': 'unit'},
        {'text': 'Cokerie', 'lonlat': lonlat(*cok[1]), 'kind': 'unit'},
    ]
    hot_zone = hot_area(feats, geo)
    with open(os.path.join(HERE, 'plants.js'), 'w', encoding='utf-8') as fh:
        fh.write('// Generated by build_plants.py: positions from the 2023 orthophoto (Regione Puglia); heights estimated except ore yard domes (77 m) and E312 (210 m).\n')
        fh.write('window.PLANTS=' + json.dumps({'type': 'FeatureCollection', 'features': feats, 'labels': labels, 'batteries': batteries,
                                              'hot_zone': hot_zone}, separators=(',', ':'), ensure_ascii=False) + ';\n')
    print(len(feats), 'features,', len(batteries), 'batteries')


if __name__ == '__main__':
    main()
