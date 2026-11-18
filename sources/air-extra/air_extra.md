# Extra air-quality data: Tamburi / Talsano (official sources)

Data: `air_extra.csv` (331 rows, one per value, with source URL and table/page).
Downloaded documents: `dl/` (ARPA Puglia, named `arpa_<id>.pdf`) and `dl2/` (ISPRA, Regione, Camera, MiTE copy). Each has a text extraction (`.txt`) next to it.
Values were copied from tables or labelled chart bars. Nothing was read off by eye from unlabelled bars, and nothing was interpolated.

## 1. PM10 before 2005: none found

- No official yearly PM10 value for any Tamburi station before 2005 turned up. That covers the 1995–2004 provincial and municipal network, the ARPA reports, ISPRA's urban reports I–VI and the Regione Puglia plans.
- ARPA states that the regional network (RRQA) in Taranto has been run by ARPA since 2004, and that validated data are published from 2005 (Taranto 2021 report, id 6940/PeaceLink 5521, §1.1). ARPA's own provincial PM10 trend chart for Taranto (2009 regional report, id 4679, Fig. 6) also starts in 2005, while Bari's goes back to 2002.
- ISPRA's IV urban report (2007 edition) gives PM10 for Taranto only as a chart of exceedance days for 2006. It has no annual means.
- The only pre-2008 Tamburi numbers in an ARPA document are **BaP campaign values**, not PM10 and not annual means. They are in the ARPA 2008–09 BaP report (id 5351, p.3):
  - 1999–2000: 1.9 ng/m³ (warm season) and 2.6 (cold season), Viviano et al.
  - 2004: 5.8 (winter) and 0.8 (summer), ISPESL
  - Oct 2005: 1.1, Univ. Bari
  - Feb 2006: 1.8, Univ. Bari

  ARPA notes that these campaigns cover less than 33% of the year, so they cannot be used for the annual target value. They are in the CSV.
- Gap: the 1990s Provincia di Taranto network (TSP/PM10) is not documented online in any official source I could reach. Two leads remain: a records request to Provincia/ARPA, or EEA AirBase, which holds Italian EoI submissions from that period. AirBase is not an Italian source and I did not query it.

## 2. Checks of our PM10 values (via Machiavelli unless noted)

Our values come from `air-data.csv` (hourly means, ≥75% hours).

| Year | Ours | Official | Source | Verdict |
|---|---|---|---|---|
| 2005 | 28.39 (67% of hours, not shown) | none | – | no official station value |
| 2006 | **16.41** | **none found** | – | unverified (see below) |
| 2007 | no valid mean | no annual mean; **47 exceedance days** | ARPA Dec 2007 report | consistent: ISPRA's 2007 table has no industrial Taranto station with >75% data |
| 2008 | 31.51 | ISPRA: the 2 industrial-suburban stations (not named) had **32–37**, with 36–59 exceedance days | ISPRA VI urban report | **possible disagreement**: one station reached 37, and our three industrial candidates are 31.5 (Machiavelli), 32.4 (Archimede, only 50% of hours) and 23.5 (Statte). Cannot be resolved without ARPA's 2008 station table, which is not online. |
| 2009 | 33.36 | 33.36 (mean of daily means); 33 | ARPA 2009 regional report, Scheda 3; VDS Tab. 3.2; 2012 plan Tab. 2.6 | agree exactly |
| 2010 | 32.42 | 32 | ARPA 2010 regional report; VDS; plan | agree |
| 2011 | 36.78 | 37 | VDS; plan | agree |
| 2012 | 33.64 | 33.5; 34 | ARPA 2012 regional report annex; VDS | agree |
| 2013 | **missing** | **30** | ARPA Taranto 2013 report (id 4858) Tab. 1; VDS | **official value found for our gap year** (Archimede 26, Talsano 23) |
| 2014 | 27.2 | 27 | id 4859 | agree |
| 2015 | 28.46 | 29 | id 4860 | minor (0.5 µg/m³; ARPA's 12 monthly means average 28.7) |
| 2016–2019 | 26.66 / 26.53 / 25.26 / 25.12 | 27 / 27 / 25 / 25 | Taranto 2019 report Tab. 2.1.5 | agree |
| 2020–2023 | 24.36 / 23.41 / 24.0 / 26.3 | 24 / 23 / 24 / 26 | Taranto reports 2020–2023 | agree |
| 2024 | 24.5 | 24 | Taranto 2024 report Fig. 2.1.1 | agree |
| 2025 | 21.43 | 21 | Taranto 2025 report Tab. 2.1.1 | agree |

Talsano also agrees within rounding:

| Year | Ours | ARPA |
|---|---|---|
| 2009 | 24.43 | 24.42 |
| 2010 | 23.89 | 24 |
| 2011 | 26.16 | 26 |
| 2012 | 23.28 | 23.3 |
| 2013 | 23.01 | 23 |
| 2016–2025 | – | all within 0.5 µg/m³ |

ARPA also publishes **via Orsini** (AdI network, Tamburi) PM10 for 2016–2025: 29, 29, 27, 27, 27, 25, 28, 33, 27, 22. Our CSV has no Orsini PM10. It is the highest-reading Tamburi site in most years, and ARPA treats it as a legal-limit site.

### Machiavelli 2006

ARPA's annual reports start in 2009, and no 2006 annual or monthly report for Taranto is online. ISPRA's IV urban report has no station means. So the value cannot be checked against an official figure.

Evidence from the raw ARPA file (`sources/arpa-taranto/2006/.../TARANTO 2006.xlsx`):

- Machiavelli's PM10 column has near-full hourly coverage.
- Its monthly means stay between 10 and 20 µg/m³ in **every** month of 2006.
- Over the same months, Archimede reads 29–57 and background Talsano 25–42.

A real drop would not halve PM10 next to the plant all year while the background site stays at ~30. A uniform halving points to an instrument or calibration problem. Note also that 16.4 is close to Machiavelli's later PM2.5 level (16.3 in 2009).

Recommendation: keep the note on the site, or drop the 2006 point. It cannot be confirmed from official sources.

## 3. BaP in PM10, annual means (ng/m³)

Main series: ARPA BaP 2020 report (id 5726, Tab. 4), repeated unchanged in the 2021 report (id 6778). Later years come from the Taranto reports.

| Year | Machiavelli | Talsano | via Alto Adige |
|---|---|---|---|
| 2008 | 1.26 (May–Dec only) | – | – |
| 2009 | 1.39 | 0.38 | 0.39 |
| 2010 | 1.82 | 0.31 | 0.31 |
| 2011 | 1.14 | 0.32 | 0.31 |
| 2012 | 0.76 | 0.24 | 0.24 |
| 2013 | 0.18 | 0.24 | 0.16 |
| 2014 | 0.12 | 0.23 | 0.13 |
| 2015 | 0.15 | 0.19 | 0.12 |
| 2016 | 0.12 | 0.22 | 0.14 |
| 2017 | 0.25 | 0.39 | 0.18 |
| 2018 | 0.11 | 0.14 | 0.10 |
| 2019 | 0.11 (first published as 0.14) | 0.16 | 0.10 |
| 2020 | 0.22 | 0.21 | 0.15 |
| 2021 | 0.33 | 0.25 | 0.20 |
| 2022 | 0.3 (1 decimal only) | 0.2 | 0.2 |
| 2023 | 0.1 (1 decimal; 40% coverage) | 0.1 | 0.1 |
| 2024 | 0.14 | 0.12* | 0.1* |
| 2025 | 0.12 | 0.07* | 0.08* |

\* Indicative measurement: coverage between 14% and 50%.

Checks of the site's figures:

- **2010 (1.82) and 2012 (0.76) agree.**
- **2009 (1.39) and 2011 (1.14)** match the current ARPA series. Earlier official documents give lower values:
  - 2009: 1.31 in the 2008–09 BaP report and in the 2012 plan Tab. 2.4; 1.3 in the 2009 regional report; 1.385 in the plan Tab. 2.5.
  - 2011: 1.13 in the 2011 regional report and plan Tab. 2.4; 1.135 in plan Tab. 2.5.

  The revised series is the one ARPA uses consistently from 2014 onward, so keep 1.39 and 1.14.
- **"Later 0.1–0.2" is not accurate.** Machiavelli was 0.25 in 2017, 0.22 in 2020, 0.33 in 2021 and about 0.3 in 2022. Suggested wording: "0.1–0.3 ng/m³ since 2013".
- Talsano, far from the plant, is at or above Machiavelli in several years from 2013. ARPA attributes this to local biomass burning.
- The Scuola Deledda (Tamburi) site has data from 2013 and is in the source tables but not in the CSV. ARPA's tables give it as the highest site in some years: 0.42 in 2021, 0.29 in 2024, 0.21 in 2025.

## 4. Dioxins

**Deposition (deposimetri): yes, there is a yearly series.** It covers 2008–2025, PCDD/F + dl-PCB as total TEQ, in pg TE/m²/day, and also BaP deposition. Source: ARPA Taranto 2025 report (id 8763), Tab. 3.2.2 and 3.2.3. All of it is in the CSV.

Tamburi values:

| Period | Site | pg TE/m²/day |
|---|---|---|
| 2008–2012 | Tamburi-Chiesa | 24.1, 15.7, 13.3, 19.9, 19.9 |
| 2013–2015 | Tamburi-Chiesa | 8.6, 2.9, 3.4 |
| 2016–2025 | Tamburi-Orsini | 1.7–5.8 |

Other sites:

- Masseria Carmine: 13.9 in 2008, 8–9 in 2009–2011, 0.6–5.8 from 2012.
- Talsano: 6.9 in 2008, below 1 in 9 of the 10 years 2016–2025.
- Inside the plant (AGL2): 8.5–36 since 2016.

The earlier Taranto reports carry the same table. In the 2021 report, for example, 2008 Tamburi is 24.1.

**Stack E312 emissions: no ARPA yearly numeric series found.** What exists:

- 2011: mean of 4 ARPA campaigns, 0.389 ng TEQ/Nm³ (ISPRA, June 2013).
- 2012: mean of 3 campaigns, 0.18 ng I-TE/Nm³ (same source).
- Undated, likely 2011–12: 0.27 ng I-TEQ/Nm³ in Camera inquiry-commission records (20 June 2012).
- 2007–08 campaigns: already in `research.md`.
- Since 2016–2018, long-term (28-day) sampling at E312 has been operator self-monitoring. ISPRA publishes it only as a scatter chart with yearly mean lines (11th controls report, 2024, Fig. 7, 2018–2024). The chart has no numeric labels, so no values were taken.
- The same ISPRA report labels E312 **dust** mass emissions: 57.3 t in 2018, 13.65 t in 2023 and 3.14 t in 2024. These are in the CSV; they are dust, not dioxin.
- Lead not reached: two ARPA slide decks on E312 campaigns mirrored on archivio.ecodallecitta.it (EDC_dnws2246, EDC_dnws3350). The server refused connections. Search snippets attribute "~180 g I-TEQ/year (2007–08) → ~26 g/year (2009–10)" to dnws2246; that figure is not verified.

## Confidence

- **High:** PM10 2009–2025 Machiavelli and Talsano, BaP 2009–2025 and deposition 2008–2025. All are printed numbers in ARPA tables, and the series agree across successive reports except where noted.
- **Medium:** ISPRA 2007/2008 ranges (station names not given) and E312 2011–2012 campaign means (ISPRA summary of ARPA work).
- **Not established:** any pre-2005 PM10, official 2005–2008 annual means at Machiavelli, and a yearly E312 PCDD/F series.
