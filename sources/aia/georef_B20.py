"""Aligns site plan B.20 ('small' coordinates of the 1431 px render) to the map (EPSG:3857) with a least-squares similarity transform."""
import numpy as np

# (drawing x, drawing y) -> (3857 x, 3857 y)
control = {
    'tank T1 / circle B': ((313.7, 1187.3), (1915553.5, 4938935.0)),
    'tank T2 / circle A': ((304.7, 1193.3), (1915599.0, 4938880.0)),
    'gasholder G2': ((397.3, 1229.5), (1915914.6, 4939591.5)),
}
src = np.array([(x, -y) for (x, y), _ in control.values()])  # drawing y points down
dst = np.array([v[1] for v in control.values()])
# similarity: [X, Y] = [a -b; b a][x, y] + [tx, ty]
A, B = [], []
for (x, y), (X, Y) in zip(src, dst):
    A += [[x, -y, 1, 0], [y, x, 0, 1]]
    B += [X, Y]
(a, b, tx, ty), *_ = np.linalg.lstsq(np.array(A), np.array(B), rcond=None)
T0 = lambda x, y: (a * x - b * y + tx, b * x + a * y + ty)
T = lambda x, y: T0(x, -y)
print('scale units/px', round(float(np.hypot(a, b)), 3), 'rotation', round(float(np.degrees(np.arctan2(b, a))), 1))
for k, ((x, y), (X, Y)) in control.items():
    px, py = T(x, y)
    print('residual', k, round(px - X), round(py - Y))

points = {
    'E111 casthouse AFO1': (300 + 436 / 11.66, 1180 + 247 / 11.66),
    'E134 cowper AFO1': (300 + 250 / 11.66, 1180 + 230 / 11.66),
    'E112 casthouse AFO2': (300 + 557 / 11.66, 1180 + 368 / 11.66),
    'E135 cowper AFO2': (300 + 430 / 11.66, 1180 + 477 / 11.66),
    'E113 casthouse AFO3': (300 + 626 / 11.66, 1180 + 464 / 11.66),
    'E114 casthouse AFO4': (400 + 75 / 11.66, 1245 + 468 / 11.66),
    'E137 cowper AFO4': (400 + 180 / 11.66, 1245 + 205 / 11.66),
    'E116 casthouse AFO5': (400 + 373 / 11.66, 1245 + 393 / 11.66),
    'E138 cowper AFO5': (400 + 340 / 11.66, 1245 + 475 / 11.66),
}
mine = {'A1': (1915748.5, 4939016.5), 'A2': (1915852.5, 4939101.0), 'E1': (1916256.5, 4939690.0), 'E2': (1916396.0, 4939878.5)}
for k, (x, y) in points.items():
    X, Y = T(x, y)
    nearest = min(mine, key=lambda m: np.hypot(mine[m][0] - X, mine[m][1] - Y))
    d = np.hypot(mine[nearest][0] - X, mine[nearest][1] - Y) * 0.76
    print(f'{k:20s} -> nearest {nearest}, {d:.0f} m')
