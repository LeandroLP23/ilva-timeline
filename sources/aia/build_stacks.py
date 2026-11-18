"""stacks.json: stacks of site plan B.20 (AIA 2011) with code, height and unit from form B.6.

Positions: red dots extracted from the vector PDF (stacks_b20.json, coordinates of the 1431 px render),
placed on the map with the similarity transform of georef_B20.py (independent check: E312 lands 9 m from the OSM chimney).
Codes: read by eye on the labels; '?' = uncertain reading, missing = unreadable or outside the frame.
"""
import json, math, os, runpy, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    T = runpy.run_path(os.path.join(HERE, 'georef_B20.py'))['T']
R = 6378137

# dot index -> code read on the label
CODES = {0: 'E340', 1: 'E731', 2: 'E733', 3: 'E101', 4: 'E105?', 6: 'E103', 7: 'E400', 9: 'E104', 10: 'E422', 11: 'E401',
         12: 'E106?', 13: 'E108', 14: 'E427', 15: 'E423', 16: 'E134', 17: 'E431', 19: 'E135', 20: 'E111', 24: 'E112',
         28: 'E136', 31: 'E113', 33: 'E528/2', 35: 'E528/1', 36: 'E567/1', 37: 'E530', 39: 'E167', 44: 'E161',
         57: 'E114', 61: 'E137', 63: 'E138', 65: 'E115', 68: 'E711', 69: 'E732', 73: 'E751', 75: 'E116', 76: 'E707',
         77: 'E713', 79: 'E740', 82: 'E735', 84: 'E703', 85: 'E324', 86: 'E736', 87: 'E737', 88: 'E314', 89: 'E738',
         90: 'E705', 91: 'E326', 92: 'E325', 93: 'E743', 94: 'E315', 95: 'E327', 98: 'E701', 99: 'E312', 23: 'E424'}
# dots missed by the automatic extraction (coke ovens area), position read on the enlarged drawing
EXTRA = [('E425', 364.5, 1321.6), ('E426?', 383.8, 1328.0), ('E436', 356.8, 1300.2), ('E435', 353.0, 1296.0),
         ('E418', 343.7, 1297.5), ('E408', 337.3, 1331.6), ('E107', 390.0, 1310.6), ('E108', 383.3, 1309.0)]

# form B.6 (MASE doc. 260236): code -> (height m, source process)
B6 = {
    'E400': (54, 'caricamento fossili in sili'), 'E401': (30, 'frantumazione primaria fossile'),
    'E422': (100, 'cokefazione batterie 3-4'), 'E423': (100, 'cokefazione batterie 5-6'),
    'E424': (125, 'cokefazione batterie 7-8'), 'E425': (125, 'cokefazione batterie 9-10'),
    'E426': (125, 'cokefazione batteria 11'), 'E428': (127, 'cokefazione batteria 12'),
    'E427': (65, 'trattamento gas coke'), 'E435': (30, 'sfornamento batterie 11-12'), 'E436': (30, 'sfornamento batterie 7-8'),
    'E408': (24, 'miscelazione fossile'), 'E107': (35, 'stock-house AFO4'), 'E431': (25, 'frantumazione e vagliatura coke'),
    'E167': (44, 'trasporto fossile PCI'), 'E161': (44, 'stoccaggio fossile PCI'),
    'E312': (210, 'agglomerazione linee D-E'), 'E314': (35, 'agglomerazione linea D'), 'E315': (35, 'agglomerazione linea E'),
    'E324': (40, 'raffreddamento agglomerato D'), 'E325': (40, 'raffreddamento agglomerato E'),
    'E326': (37, 'calce idrata linea D'), 'E327': (37, 'calce idrata linea E'), 'E340': (20, 'bricchettazione residui'),
    'E101': (30, 'stock-house AFO1'), 'E103': (30, 'stock-house AFO2'), 'E104': (30, 'stock-house AFO2-AFO3'),
    'E105': (30, 'stock-house AFO3'), 'E106': (35, 'stock-house AFO4'), 'E108': (36, 'stock-house AFO5'),
    'E111': (35, 'campo di colata AFO1'), 'E112': (25, 'campo di colata AFO2'), 'E113': (25, 'campo di colata AFO3'),
    'E114': (35, 'campo di colata AFO4'), 'E115': (30, 'campo di colata AFO5 sud'), 'E116': (30, 'campo di colata AFO5 nord'),
    'E134': (66, 'cowper AFO1'), 'E135': (64, 'cowper AFO2'), 'E136': (65, 'cowper AFO3'),
    'E137': (66, 'cowper AFO4'), 'E138': (71, 'cowper AFO5'),
    'E528/1': (49, 'degasatori acciaieria 1'), 'E528/2': (49, 'degasatori acciaieria 1'), 'E530': (7, 'ferroleghe acciaieria 1'),
    'E567/1': (15, 'vapore acciaieria 1'), 'E701': (20, 'decapaggio nastri'), 'E703': (22, 'oil cellar tandem'),
    'E705': (22, 'treno tandem'), 'E707': (25, 'treno temper 2'), 'E711': (25, 'oil cellar temper 2'), 'E713': (28, 'ricottura nastri'),
    'E731': (14, 'asciugatura lamiere'), 'E732': (14, 'granigliatura lamiere'), 'E733': (14, 'preparazione primer'),
    'E735': (25, 'pretrattamento nastri'), 'E736': (25, 'elettrodeposizione'), 'E737': (25, 'elettrodeposizione'),
    'E738': (25, 'elettrodeposizione'), 'E740': (25, 'soluzione elettrolitica'), 'E743': (28, 'satinatura cilindri'),
    'E751': (44, 'pretrattamento nastro'),
}
SINCE = {'E107': 1975, 'E114': 1975, 'E115': 1975, 'E116': 1975, 'E137': 1975, 'E138': 1975, 'E106': 1975, 'E108': 1975}


def main():
    pts = json.load(open(os.path.join(HERE, 'stacks_b20.json')))
    n0 = len(pts)
    pts += [{'x': x, 'y': y} for _, x, y in EXTRA]
    CODES.update({n0 + k: e[0] for k, e in enumerate(EXTRA)})
    out = []
    for i, p in enumerate(pts):
        X, Y = T(p['x'], p['y'])
        lon, lat = X / R * 180 / math.pi, (2 * math.atan(math.exp(Y / R)) - math.pi / 2) * 180 / math.pi
        code = CODES.get(i)
        h, process = B6.get((code or '').rstrip('?'), (None, None))
        out.append({'code': code, 'h': h, 'process': process, 'lon': round(lon, 6), 'lat': round(lat, 6),
                    'since': SINCE.get((code or '').rstrip('?'), 1965)})
    json.dump(out, open(os.path.join(HERE, 'stacks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    known = sum(1 for c in out if c['h'])
    print(len(out), 'stacks,', known, 'with official height')


if __name__ == '__main__':
    main()
