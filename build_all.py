"""Regenerate the site's data files in dependency order.

Usage: python build_all.py [--air-archive DIR] [--network]

Steps whose inputs are not in the repository (LiDAR tiles, ARPA hourly archives, network)
are skipped with a message and their committed outputs are left as they are.
"""
import argparse, glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIDAR = bool(glob.glob(os.path.join(HERE, 'sources', 'lidar', '*_DSMFirst.tiff')))


def run(script, *args):
    print(f'== {script} {" ".join(args)}', flush=True)
    subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.join(HERE, script), *args], check=True, cwd=HERE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--air-archive', help='folder with the ARPA Puglia yearly archives (rebuilds air-data.csv)')
    ap.add_argument('--network', action='store_true', help='also download emissions from the EEA portal')
    a = ap.parse_args()

    # map-data.js needs heights.json, which needs map-data.js: build the map twice around the heights
    run('build_map.py')
    if LIDAR:
        run('build_heights.py')
        run('build_map.py')
    run('build_plants.py')
    if LIDAR:
        # the port step also needs the tiles: without them conveyor heights would fall back to defaults
        for s in ('build_conveyors.py', 'build_reliefs.py', 'build_port.py'):
            run(s)
    else:
        print('-- no LiDAR tiles in sources/lidar/: heights, conveyors, reliefs and port left unchanged')
    if a.air_archive:
        run('build_air.py', a.air_archive)
    else:
        run('build_air.py', '--js')
    if a.network:
        run('build_emissions.py')
    else:
        print('-- emissions.js left unchanged (use --network to download from the EEA portal)')


if __name__ == '__main__':
    main()
