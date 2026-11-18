"""conveyors.js: conveyor belts and elevated pipelines detected in the 2008-2010 laser survey.

Method, on a 2 m grid inside the plant perimeter (height = DSM - DTM):
1. thin ridge: a cell at least 3 m high that, in at least one of the 4 directions, has both cells
   4-6 m away lower by at least 3 m (wide sheds and their edges do not pass);
2. contiguous ridges are split into straight segments (RANSAC), at least 40 m long;
3. each segment is divided into 20 m stretches with the measured median height.
"""
import json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_heights as BH  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LON0, LON1, LAT0, LAT1 = 17.165, 17.232, 40.484, 40.528
C = 2.0
MLAT = 1 / 111320
MLON = 1 / (111320 * math.cos(math.radians(40.505)))
CACHE = os.path.join(HERE, 'sources', 'lidar', 'ndsm_2m.npy')


def ndsm():
    if os.path.exists(CACHE):
        return np.load(CACHE)
    BH.load()
    nx, ny = int((LON1 - LON0) / MLON / C), int((LAT1 - LAT0) / MLAT / C)
    out = np.full((ny, nx), np.nan, np.float32)
    xs = LON0 + (np.arange(nx) + 0.25) * C * MLON
    for j in range(ny):
        lat = LAT1 - (j + 0.25) * C * MLAT
        rows = np.vstack([BH.heights_vec(xs + dx * MLON, np.full(nx, lat - dy * MLAT)) for dx in (0, 1) for dy in (0, 1)])
        with np.errstate(all='ignore'):
            out[j] = np.nanmax(rows, axis=0)
    np.save(CACHE, out)
    return out


def inside_polygon(shape, ring):
    ny, nx = shape
    xs = np.array([(p[0] - LON0) / MLON / C for p in ring])
    ys = np.array([(LAT1 - p[1]) / MLAT / C for p in ring])
    X, Y = np.meshgrid(np.arange(nx) + 0.5, np.arange(ny) + 0.5)
    m = np.zeros(shape, bool)
    for k in range(len(xs)):
        ax, ay, bx, by = xs[k], ys[k], xs[(k + 1) % len(xs)], ys[(k + 1) % len(xs)]
        m ^= ((ay > Y) != (by > Y)) & (X < ax + (Y - ay) * (bx - ax) / ((by - ay) or 1e-12))
    return m


def building_mask(shape, polygons):
    """Footprint of the OSM buildings on the grid, filling each polygon only within its bounding box."""
    ny, nx = shape
    m = np.zeros(shape, bool)
    for ring in polygons:
        xs = [(p[0] - LON0) / MLON / C for p in ring]
        ys = [(LAT1 - p[1]) / MLAT / C for p in ring]
        i0, i1 = max(0, int(min(xs))), min(nx, int(max(xs)) + 2)
        j0, j1 = max(0, int(min(ys))), min(ny, int(max(ys)) + 2)
        if i0 >= i1 or j0 >= j1:
            continue
        X, Y = np.meshgrid(np.arange(i0, i1) + 0.5, np.arange(j0, j1) + 0.5)
        inside = np.zeros(X.shape, bool)
        for k in range(len(xs)):
            ax, ay, bx, by = xs[k], ys[k], xs[(k + 1) % len(xs)], ys[(k + 1) % len(xs)]
            inside ^= ((ay > Y) != (by > Y)) & (X < ax + (Y - ay) * (bx - ax) / ((by - ay) or 1e-12))
        m[j0:j1, i0:i1] |= inside
    return m


def ridges(h):
    z = np.nan_to_num(h, nan=0.0)
    high = z >= 3
    out = np.zeros(z.shape, bool)
    for dj, di in ((0, 1), (1, 0), (1, 1), (1, -1)):
        for d in (2, 3):  # 4 and 6 m
            a = np.roll(np.roll(z, d * dj, 0), d * di, 1)
            b = np.roll(np.roll(z, -d * dj, 0), -d * di, 1)
            out |= high & (a <= z - 3) & (b <= z - 3)
    return out


def components(cand):
    lab = np.zeros(cand.shape, np.int32)
    n = 0
    for j0, i0 in zip(*np.nonzero(cand)):
        if lab[j0, i0]:
            continue
        n += 1
        queue = [(j0, i0)]
        lab[j0, i0] = n
        while queue:
            j, i = queue.pop()
            for dj in (-1, 0, 1):
                for di in (-1, 0, 1):
                    a, b = j + dj, i + di
                    if 0 <= a < cand.shape[0] and 0 <= b < cand.shape[1] and cand[a, b] and not lab[a, b]:
                        lab[a, b] = n
                        queue.append((a, b))
    return lab, n


def segments(x, y, rng, min_len=40.0, tolerance=2.5):
    """Straight segments from a set of points (metres), with repeated RANSAC."""
    rest = np.ones(len(x), bool)
    out = []
    for _ in range(40):
        idx = np.nonzero(rest)[0]
        if len(idx) < min_len / C:
            break
        best = None
        for _ in range(150):
            a, b = rng.choice(idx, 2, replace=False)
            d = np.array([x[b] - x[a], y[b] - y[a]])
            L = float(np.hypot(*d))
            if L < 6:
                continue
            u = d / L
            dist = np.abs(-(x[idx] - x[a]) * u[1] + (y[idx] - y[a]) * u[0])
            near = idx[dist <= tolerance]
            if best is None or len(near) > len(best[0]):
                best = (near, a, u)
        if best is None:
            break
        near, a, u = best
        rest[near] = False
        t = (x[near] - x[a]) * u[0] + (y[near] - y[a]) * u[1]
        # longest continuous stretch (gaps up to 8 m): two aligned structures do not merge
        order = np.argsort(t)
        t_ord = t[order]
        cuts = np.nonzero(np.diff(t_ord) > 8)[0]
        starts, ends = np.r_[0, cuts + 1], np.r_[cuts, len(t_ord) - 1]
        k = int(np.argmax(t_ord[ends] - t_ord[starts]))
        t0, t1 = t_ord[starts[k]], t_ord[ends[k]]
        taken = near[(t >= t0) & (t <= t1)]
        if t1 - t0 >= min_len and len(taken) * C >= 0.5 * (t1 - t0):
            out.append((x[a] + t0 * u[0], y[a] + t0 * u[1], x[a] + t1 * u[0], y[a] + t1 * u[1], taken))
        if len(near) < min_len / C:
            break
    return out


def main():
    h = ndsm()
    geo = open(os.path.join(HERE, 'map-data.js'), encoding='utf-8').read()
    geo = json.loads(geo[geo.index('=') + 1:geo.rindex(';')])
    perimeter = geo['plant']['features'][0]['geometry']['coordinates'][0][0]
    cand = ridges(h) & inside_polygon(h.shape, perimeter)
    polygons = [(f['geometry']['coordinates'][0][0] if f['geometry']['type'] == 'MultiPolygon' else f['geometry']['coordinates'][0])
                for f in geo['factory']['features']]
    buildings = building_mask(h.shape, polygons)
    print('ridge cells', int(cand.sum()))
    lab, n = components(cand)
    rng = np.random.default_rng(7)
    ll = lambda px, py: [round(LON0 + px * MLON, 6), round(LAT1 - py * MLAT, 6)]
    feats, n_seg, metres = [], 0, 0.0
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        if len(jj) < 20:
            continue
        x, y = ii * C + C / 2, jj * C + C / 2
        for x1, y1, x2, y2, taken in segments(x, y, rng):
            # roof ridges and edges are ridges too: drop the segments lying on a building
            if buildings[jj[taken], ii[taken]].mean() > 0.3:
                continue
            L = math.hypot(x2 - x1, y2 - y1)
            n_seg += 1
            metres += L
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            tp = (x[taken] - x1) * ux + (y[taken] - y1) * uy
            # median height every 20 m (0 = stretch without measurement); the page rebuilds 4 m wide stretches
            heights = []
            for a in np.arange(0, L, 20):
                sel = taken[(tp >= a) & (tp < min(L, a + 20))]
                heights.append(round(float(np.median(h[jj[sel], ii[sel]])), 1) if len(sel) >= 2 else 0)
            feats.append(ll(x1, y1) + ll(x2, y2) + [heights])
    print(n_seg, 'straight segments,', round(metres / 1000, 1), 'km')
    with open(os.path.join(HERE, 'conveyors.js'), 'w', encoding='utf-8') as fh:
        fh.write('// Generated by build_conveyors.py: long thin elevated structures in the MASE 2008-2010 LiDAR survey.\n')
        fh.write('// Each entry: [lon1, lat1, lon2, lat2, [height every 20 m]].\n')
        fh.write('window.CONVEYORS=' + json.dumps({'segments': feats, 'km': round(metres / 1000, 1)}, separators=(',', ':')) + ';\n')


if __name__ == '__main__':
    main()
