# Ex-Ilva Taranto, year by year

A static website (in Italian) on the history of the Taranto steelworks, from the olive groves before 1960 to the shutdown of the blast furnaces in 2026. It combines:

- a map of the plant in 2D and 3D, with building and stack heights measured by the Ministry of the Environment's LiDAR survey;
- an event-driven timeline: each year with events gets the same space, long quiet periods are compressed;
- yearly data (workplace deaths, PM10 in the air, declared emissions, steel output), aligned with the timeline;
- health data shown on the areas they refer to;
- a methods page (`methods.html`) listing every source.

Every figure on the site comes from an official or documented source. Model estimates are kept in the data but not shown. Doubts and open questions live in [`research.md`](research.md), not on the site.

## Running it

The pages load their data with `<script>` tags, so any static file server works:

```sh
python -m http.server 8000
```

then open <http://localhost:8000/>. Opening `index.html` directly from disk also works in most browsers.

## Project layout

| Path | Content |
|---|---|
| `index.html`, `style.css`, `app.js` | the main page |
| `methods.html` | methods and sources page |
| `events.js` | events, health periods and steel production, written by hand with sources |
| `work-deaths.js` | workplace deaths since 2003, generated from `sources/work_deaths_check.json` |
| `map-data.js`, `heights.json`, `plants.js`, `reliefs.js`, `port.js`, `conveyors.js`, `air.js`, `emissions.js` | generated data |
| `build_*.py` | data generators |
| `osm*.json` | OpenStreetMap extracts used by the generators |
| `sources/` | curated source data (CSV with source and page for every value) and method notes |
| `research.md` | research notes, verification log and open questions |

## Rebuilding the data

```sh
pip install -r requirements.txt
python build_all.py                          # map, plants, reliefs, port, air
python build_all.py --network                # also downloads emissions from the EEA portal
python build_all.py --air-archive DIR        # rebuilds the air series from the ARPA Puglia yearly archives
```

Some inputs are large or third-party and are not in the repository; the steps that need them are skipped and their committed outputs kept:

- **LiDAR tiles** (`sources/lidar/`, about 255 MB): DSM First and DTM at 1 m from the MASE PST database, downloadable tile by tile from the MASE remote-sensing portal (`sim.mase.gov.it`), flights 2008–2010. Without them the heights, reliefs, conveyors and port steps are skipped.
- **ARPA Puglia hourly archives** (`sources/arpa-taranto/`): yearly archives from the [ARPA Puglia historical data page](https://www.arpa.puglia.it/pagina3139_dati-storici-qualit-delllaria.html); their ids are listed in `sources/arpa-archive-ids.txt`.
- **PDF documents** cited in `methods.html` and `research.md`: linked there, not stored here.

## Data and attribution

- Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, [ODbL](https://opendatacommons.org/licenses/odbl/); `map-data.js`, `port.js` and the `osm*.json` extracts are derived from it.
- Heights and reliefs: LiDAR survey of the Italian Ministry of the Environment (MASE), PST database, CC BY 4.0.
- Air quality: ARPA Puglia. Emissions: European Environment Agency (E-PRTR / Industrial Emissions Portal), earlier years from the ISPRA INES and EPER registers.
- Stack heights and plant layout: AIA 2011 permit documents (MASE).

The full list of sources, with links, is on the methods page.
