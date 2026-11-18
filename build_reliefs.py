"""reliefs.js: ecological hills and yard piles from the terrain model (MASE LiDAR DTM 2008-2010).

The survey DTM counts as "ground" both the hills and the piles of ore and coal.
For each 4 m cell: relief = DTM elevation - elevation of the surrounding ground (5th percentile in 100 m
blocks, interpolated). Cells with enough relief become small extruded volumes.
"""
import base64, io, json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_heights as BH  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LON0, LON1, LAT0, LAT1 = 17.200, 17.240, 40.484, 40.515
C = 4.0
MLAT = 1 / 111320
MLON = 1 / (111320 * math.cos(math.radians(40.5)))
# strip of the three hills, along the Appia road between the yards and Tamburi (traced on the DTM)
HILLS = [(17.2172, 40.4936), (17.2252, 40.4983), (17.2286, 40.4994), (17.2290, 40.4981), (17.2256, 40.4968), (17.2176, 40.4930)]


def dtm_grid(c=C):
    nx, ny = int((LON1 - LON0) / MLON / c), int((LAT1 - LAT0) / MLAT / c)
    xs = LON0 + (np.arange(nx) + 0.5) * c * MLON
    out = np.full((ny, nx), np.nan, np.float32)
    for j in range(ny):
        lat = LAT1 - (j + 0.5) * c * MLAT
        klat = int(math.floor(lat * 100))
        klon = np.floor(xs * 100).astype(int)
        for b in set(klon.tolist()):
            t = BH.TILES.get((klat, b))
            if t is None:
                continue
            m = klon == b
            x = np.clip(((xs[m] - b / 100) / BH.STEP).astype(int), 0, 999)
            y = min(999, int(((klat + 1) / 100 - lat) / BH.STEP))
            out[j, m] = t[1][y, x]
    return out


def ground(dtm, block=25):
    """Ground elevation: 5th percentile per 100 m block, bilinearly interpolated."""
    ny, nx = dtm.shape
    by, bx = math.ceil(ny / block), math.ceil(nx / block)
    p = np.full((by, bx), np.nan, np.float32)
    for j in range(by):
        for i in range(bx):
            v = dtm[j * block:(j + 1) * block, i * block:(i + 1) * block]
            v = v[~np.isnan(v)]
            if len(v) > 20:
                p[j, i] = np.percentile(v, 5)
    # blocks without data take the mean of their neighbours
    for _ in range(5):
        empty = np.isnan(p)
        if not empty.any():
            break
        pad = np.pad(p, 1, constant_values=np.nan)
        neighbours = np.stack([pad[1 + dj:1 + dj + by, 1 + di:1 + di + bx] for dj in (-1, 0, 1) for di in (-1, 0, 1)])
        with np.errstate(all='ignore'):
            p[empty] = np.nanmean(neighbours, axis=0)[empty]
    jj = (np.arange(ny) + 0.5) / block - 0.5
    ii = (np.arange(nx) + 0.5) / block - 0.5
    j0, i0 = np.clip(np.floor(jj).astype(int), 0, by - 2), np.clip(np.floor(ii).astype(int), 0, bx - 2)
    fj, fi = np.clip(jj - j0, 0, 1)[:, None], np.clip(ii - i0, 0, 1)[None, :]
    a, b = p[j0][:, i0], p[j0][:, i0 + 1]
    c, d = p[j0 + 1][:, i0], p[j0 + 1][:, i0 + 1]
    return (a * (1 - fi) + b * fi) * (1 - fj) + (c * (1 - fi) + d * fi) * fj


def inside(lon, lat, polygon):
    m = np.zeros(lon.shape, bool)
    for (ax, ay), (bx, by) in zip(polygon, polygon[1:] + polygon[:1]):
        m ^= ((ay > lat) != (by > lat)) & (lon < ax + (lat - ay) * (bx - ax) / ((by - ay) or 1e-12))
    return m


def main():
    BH.load()
    dtm = dtm_grid()
    rel = dtm - ground(dtm)
    ny, nx = dtm.shape
    LON = LON0 + (np.arange(nx)[None, :] + 0.5) * C * MLON + np.zeros((ny, 1))
    LAT = LAT1 - (np.arange(ny)[:, None] + 0.5) * C * MLAT + np.zeros((1, nx))

    plants = open(os.path.join(HERE, 'plants.js'), encoding='utf-8').read()
    plants = json.loads(plants[plants.index('=') + 1:plants.rindex(';')])
    yards = {}
    for f in plants['features']:
        p = f['properties']
        if p['kind'] == 'dome' and p['yard'] not in yards:  # the first band is the whole footprint
            yards[p['yard']] = ([tuple(q) for q in f['geometry']['coordinates'][0][:-1]], p['since'])

    counts = {}

    def cells(mask, **props):
        """A run of contiguous cells with the same height (to the metre) becomes a single rectangle."""
        hq = np.round(np.nan_to_num(rel)).astype(int)
        for j in range(ny):
            i = 0
            while i < nx:
                if not mask[j, i]:
                    i += 1
                    continue
                k = i
                while k + 1 < nx and mask[j, k + 1] and hq[j, k + 1] == hq[j, i]:
                    k += 1
                cell(i, k + 1, j, h=float(hq[j, i]), **props)
                i = k + 1

    groups = []  # each group: shared properties + rows [i, i_end, j, h]

    def cell(i, i_end, j, h, **props):
        if not groups or groups[-1]['props'] != props:
            groups.append({'props': props, 'rows': []})
        groups[-1]['rows'].append([int(i), int(i_end), int(j), int(h)])

    m_hills = inside(LON, LAT, HILLS) & (rel >= 2)
    cells(m_hills, kind='hill', group='hills')
    counts['hills'] = (int(m_hills.sum()), float(np.nanmax(rel[m_hills])) if m_hills.any() else 0)

    for yard, (polygon, since) in yards.items():
        m = inside(LON, LAT, polygon) & (rel >= 1.5)
        cells(m, kind='pile', yard=yard, until=since - 1, measured=True, group='piles-' + yard,
              tint={'ore': '#8a4b2e', 'coal': '#2f2b28', 'other': '#6b6a66'}[yard])
        counts[yard] = (int(m.sum()), float(np.nanpercentile(rel[m], 95)) if m.any() else 0)

    # top view: images shaded from the 1 m DTM (the 4 m grid of the volumes is too coarse)
    images = []
    C1 = 1.0
    dtm1 = dtm_grid(C1)
    rel1 = dtm1 - ground(dtm1, block=100)
    # smoothing (sigma 2 m): removes the noise and the texture of resampling from 1e-5° to 1 m
    k = np.exp(-0.5 * (np.arange(-6, 7) / 2.0) ** 2); k /= k.sum()
    smooth = np.nan_to_num(rel1)
    for axis in (0, 1):
        smooth = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), axis, smooth)
    gy, gx = np.gradient(smooth, C1)
    light = np.clip(0.8 + (-gx * 0.6 + gy * 0.6) / np.sqrt(1 + gx ** 2 + gy ** 2) * 0.9, 0.3, 1.5)  # sun from the north-west
    ny1, nx1 = rel1.shape

    def image(polygon, threshold, colour, **props):
        xs, ys = [q[0] for q in polygon], [q[1] for q in polygon]
        i0, i1 = max(0, int((min(xs) - LON0) / MLON / C1)), min(nx1, int((max(xs) - LON0) / MLON / C1) + 1)
        j0, j1 = max(0, int((LAT1 - max(ys)) / MLAT / C1)), min(ny1, int((LAT1 - min(ys)) / MLAT / C1) + 1)
        lon = LON0 + (np.arange(i0, i1)[None, :] + 0.5) * C1 * MLON + np.zeros((j1 - j0, 1))
        lat = LAT1 - (np.arange(j0, j1)[:, None] + 0.5) * C1 * MLAT + np.zeros((1, i1 - i0))
        r = np.nan_to_num(rel1[j0:j1, i0:i1])
        m = inside(lon, lat, polygon) & (r >= threshold)
        rgb = np.array(colour, np.float32)[None, None, :] * light[j0:j1, i0:i1, None]
        im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB')
        # x3: interpolated shading, outline recomputed as a threshold (sharp even at high zoom)
        X = 3
        im = im.resize((im.width * X, im.height * X), Image.BICUBIC)
        edge = Image.fromarray((m * 255).astype(np.uint8)).resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(X * 0.8))
        edge = np.clip((np.asarray(edge, np.float32) - 128) * 3 + 128, 0, 255) / 255
        im.putalpha(Image.fromarray((edge * 245).astype(np.uint8)))
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=82, method=6)
        x0, x1 = LON0 + i0 * C1 * MLON, LON0 + i1 * C1 * MLON
        y1, y0 = LAT1 - j0 * C1 * MLAT, LAT1 - j1 * C1 * MLAT
        images.append({**props, 'coordinates': [[x0, y1], [x1, y1], [x1, y0], [x0, y0]],
                       'url': 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()})
        print(f"image {props.get('yard', props['kind'])}: {im.width}x{im.height} px, {len(buf.getvalue()) // 1024} KB")

    image(HILLS, 2, (92, 118, 60), kind='hill', since=1975)
    for yard, (polygon, since) in yards.items():
        image(polygon, 1.5, {'ore': (150, 62, 34), 'coal': (48, 44, 42), 'other': (98, 96, 92)}[yard], kind='pile', yard=yard, until=since - 1)

    for k, (n, h) in counts.items():
        print(f'{k}: {n} cells of 4 m ({n * 16 / 10000:.1f} ha), maximum/95th percentile height {h:.1f} m')
    with open(os.path.join(HERE, 'reliefs.js'), 'w', encoding='utf-8') as fh:
        fh.write('// Generated by build_reliefs.py: hills and piles from the MASE 2008-2010 LiDAR DTM.\n')
        # compact format: the page rebuilds the rectangles from the grid
        fh.write('window.RELIEFS=' + json.dumps({'grid': {'lon0': LON0, 'lat1': LAT1, 'dlon': C * MLON, 'dlat': C * MLAT},
                                                'groups': groups, 'images': images}, separators=(',', ':'), ensure_ascii=False) + ';\n')


if __name__ == '__main__':
    main()
