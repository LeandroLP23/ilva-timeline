"""heights.json: heights measured by the laser survey (LiDAR) of the Ministry of the Environment, 2008-2010 flights.

Data: DSM First and DTM at 1 m, Extraordinary remote sensing plan (PST database, CC BY 4.0 licence),
tiles in sources/lidar/. Height of an object = DSM - DTM.
Buildings take the 85th percentile of the pixel heights inside the polygon (robust to edges
and single spikes); stacks take the maximum within a few metres of the point.
"""
import glob, json, math, os, re
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = 1e-5  # degrees per pixel
TILES = {}  # (lat0, lon0) in hundredths of a degree -> (dsm, dtm), nan where data is missing


def load():
    for f in glob.glob(os.path.join(HERE, 'sources', 'lidar', '*_DSMFirst.tiff')):
        m = re.search(r'D(\d{4})(\d{4})_', f)
        lat0, lon0 = int(m.group(1)), int(m.group(2))
        dtm_f = f.replace('_DSMFirst', '_DTM')
        if not os.path.exists(dtm_f):
            continue
        a = [np.array(Image.open(x), dtype=np.float32) for x in (f, dtm_f)]
        for x in a:
            x[x <= -9998] = np.nan
        TILES[(lat0, lon0)] = a


def height(lon, lat):
    """Height above ground in the pixel containing (lon, lat); nan if not covered."""
    k = (int(math.floor(lat * 100)), int(math.floor(lon * 100)))
    t = TILES.get(k)
    if t is None:
        return math.nan
    x = int((lon - k[1] / 100) / STEP)
    y = int(((k[0] + 1) / 100 - lat) / STEP)
    if not (0 <= x < 1000 and 0 <= y < 1000):
        return math.nan
    return float(t[0][y, x] - t[1][y, x])


def heights_vec(lon, lat):
    """Vectorised height() for arrays of points."""
    lon, lat = np.asarray(lon, np.float64), np.asarray(lat, np.float64)
    out = np.full(lon.shape, np.nan, np.float32)
    klat, klon = np.floor(lat * 100).astype(int), np.floor(lon * 100).astype(int)
    for a, b in set(zip(klat.tolist(), klon.tolist())):
        t = TILES.get((a, b))
        if t is None:
            continue
        m = (klat == a) & (klon == b)
        x = np.clip(((lon[m] - b / 100) / STEP).astype(int), 0, 999)
        y = np.clip((((a + 1) / 100 - lat[m]) / STEP).astype(int), 0, 999)
        out[m] = t[0][y, x] - t[1][y, x]
    return out


def sample_polygon(ring, max_points=4000):
    """Heights of the pixels (or of a regular grid) inside the polygon [(lon, lat), ...]."""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    nx, ny = max(1, int((x1 - x0) / STEP)), max(1, int((y1 - y0) / STEP))
    step = max(1, int(math.sqrt(nx * ny / max_points)))
    gx = x0 + (np.arange(0, nx, step) + 0.5) * STEP
    gy = y0 + (np.arange(0, ny, step) + 0.5) * STEP
    X, Y = np.meshgrid(gx, gy)
    inside = np.zeros(X.shape, bool)
    for (ax, ay), (bx, by) in zip(ring, ring[1:] + ring[:1]):
        c = ((ay > Y) != (by > Y)) & (X < ax + (Y - ay) * (bx - ax) / ((by - ay) or 1e-12))
        inside ^= c
    return heights_vec(X[inside], Y[inside])


def building_height(ring):
    v = sample_polygon(ring)
    v = v[~np.isnan(v)]
    if len(v) < 4:
        return None
    return round(float(np.percentile(v, 85)), 1)


def nearby_peak(lon, lat, radius_m=6):
    """Highest peak within radius_m: (height, lon, lat) or None."""
    r = int(radius_m)
    dlat, dlon = 1 / 111320, 1 / (111320 * math.cos(math.radians(lat)))
    i, j = np.meshgrid(np.arange(-r, r + 1), np.arange(-r, r + 1))
    m = i * i + j * j <= r * r
    lons, lats = lon + i[m] * dlon, lat + j[m] * dlat
    v = heights_vec(lons, lats)
    if np.all(np.isnan(v)):
        return None
    k = int(np.nanargmax(v))
    return round(float(v[k]), 1), round(float(lons[k]), 6), round(float(lats[k]), 6)


def main():
    load()
    print(len(TILES), 'tiles loaded')
    geo = open(os.path.join(HERE, 'map-data.js'), encoding='utf-8').read()
    geo = json.loads(geo[geo.index('=') + 1:geo.rindex(';')])
    out = {'factory': {}, 'city': {}, 'stacks': {}}
    for key in ('factory', 'city'):
        for i, f in enumerate(geo[key]['features']):
            g = f['geometry']
            ring = g['coordinates'][0][0] if g['type'] == 'MultiPolygon' else g['coordinates'][0]
            h = building_height([tuple(p) for p in ring[:-1]])
            if h is not None:
                out[key][str(f['properties']['id'])] = h
        print(key, len(out[key]), 'buildings measured out of', len(geo[key]['features']))
    stacks = json.load(open(os.path.join(HERE, 'sources', 'aia', 'stacks.json'), encoding='utf-8'))
    for k, c in enumerate(stacks):
        # the aligned site plan is off by ~10 m: look for the peak within 15 m and move there
        peak = nearby_peak(c['lon'], c['lat'], 15)
        if peak is not None:
            out['stacks'][str(k)] = {'h': peak[0], 'lon': peak[1], 'lat': peak[2]}
    json.dump(out, open(os.path.join(HERE, 'heights.json'), 'w', encoding='utf-8'))
    return out, stacks


if __name__ == '__main__':
    out, stacks = main()
    comparison = [(c['code'], c['h'], (out['stacks'].get(str(k)) or {}).get('h')) for k, c in enumerate(stacks) if c['h'] and (c['code'] or '')[-1:] != '?']
    print('stacks: code, AIA height, LiDAR maximum within 15 m')
    for r in sorted(comparison, key=lambda r: -r[1])[:15]:
        print('  ', r)
