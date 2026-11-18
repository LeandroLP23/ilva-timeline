# Extra official emission figures, ILVA Taranto steelworks

Research date: 2026-11-18. Values are in `emissions_extra.csv`. Nothing was interpolated. Where a source
gives a different unit, the CSV converts it only to t or g TEQ, and the original figure is in `notes`.

## What was found

| Year | PM | PCDD/F (g TEQ) | Benzene (t) | PAH, air (t) | Source |
|---|---|---|---|---|---|
| 2002 | 9,707.4 t **total PM** (secondary) | 71.4 | 188 | 25.9 | EPER (labelled "2001"), primary |
| 2003 | none | none | none | none | not found |
| 2004 | none | 76.2 | 183 | 25.8 | EPER 2004, primary, method E |
| 2005 | 10,979 t **total PM** (secondary) | 93.0 (secondary) | 219.24 (secondary) | 31.12 (secondary) | ARPA Puglia via the GIP decree; PeaceLink |
| 2006 | 11,462.3 t **total PM** | 91.5 | 231.39 | 32.24 | INES 2006 xls, primary |
| 2024 | 60.51 t PM10 | 0.19 | 1.517 | none reported | EEA Industrial Reporting v16, primary |

## Sources

- **EPER, ILVA S.P.A. Stabilimento di Taranto, EPER id 190098** (Commission/EEA site eper.ec.europa.eu,
  Wayback copies): `eper_2004_IT_190098_details_print.html` (2004 values and a 2001-vs-2004 time series) and
  `eper_2004_IT_190098_ILVA_Taranto.xml` (2004 download with M/C/E codes). All 2004 values are coded **E**
  (estimated). The EPER XML has no medium field. The HTML page splits air and water.
- **Italy's EPER "2001" column is actually reference year 2002.** The first INES declaration (INES2002,
  reference year 2001) collected only facility identification and no emissions (`ines/APAT_RTI_INES_dichiarazione2002_rif2001.pdf`).
  The first emission data are for 2002 (`ines/APAT_Rapporti_62-2005_INES_dati_2002.pdf`). The ISPRA paper
  `ispra_ines-eper-prtr.pdf` states that Italy's first EPER submission referred to 2002. The PeaceLink "2002"
  figures (71.4 g dioxins, 188,236.7 kg benzene, 25,913.9 kg PAH) match the EPER "2001" column, which
  confirms it.
- **INES 2006**: ISPRA/APAT published `dati_Registro_INES_2006` (xls, last version 8 April 2010; three
  archived versions have identical ILVA rows). The ILVA rows are extracted in `ines/ines_2006_ilva_taranto_rows.csv`.
  Values are given per IPPC activity, and the CSV sums them per pollutant for air (`ARIA1_ACQUA0` = 1).
  The file has no M/C/S method column. One archived link to the file is labelled "ultimo anno rilevato con la normativa indicata": 2006 was the last
  INES year before E-PRTR.
- **2005**: no primary INES copy survives. The INES web search used POST forms that the Wayback Machine did not
  capture. The figures come from:
  - The Taranto GIP's preventive-seizure decree (July 2012, `gip2012.pdf`, p.146), quoting ARPA Puglia:
    "polveri totali … 10979 tonnellate/anno … stabilimento ILVA (dati INES 2005)". On p.144 it quotes ARPA:
    "93 grammi/anno riportato nel Registro INES" for PCDD/F, without stating the year.
  - The PeaceLink table at https://www.peacelink.it/editoriale/a/51745.html, built "sui dati INES". This is
    the only source for the 2005 benzene (219,240.3 kg) and PAH (31,124.3 kg) figures.
  These are pointers, not primary data.
- **2024**: EEA "Industrial Reporting under the IED and E-PRTR", v16 (published 2026-02-20, covering 2007–2024).
  The source file is the user-friendly CSV `F1_4_Air_Releases_Facilities`, facility `IT.CAED/741231004.FACILITY`
  ("STABILIMENTO DI TARANTO"). That file has the same 2007–2023 values as `emissions.js`, so it is the same
  facility as EEA 2007001763. The 2024 data are in the dataset but not yet in the Tableau view
  (`Browsethedata_6_platform`), which still stops at 2023. The CSV has no method column. The full Access DB
  (2 GB) has methods but was not downloaded. The ILVA extract is in `eea_v16_taranto_steelworks_air.csv`.
  The 2024 benzene value (1,516.53 kg) is much lower than in 2021–2023, and PAH was not reported.

## Not found

- **Any 2003 value.** The only ILVA 2003 figures would be in the INES web database, which is not archived.
- **PM10 before 2007.** ILVA never reported PM10 to INES or EPER. INES had two separate pollutants, "PM"
  (total particulate) and "PM10", each with a 50 t threshold (`ines/All-1-Lineeguida.pdf`, Tab. 1.6.2), and
  ILVA declared only "PM". EPER's list had only PM10, so ILVA has no particulate entry in EPER 2002 or 2004.
  **Total PM cannot be plotted as PM10.** PM10 is only a fraction of total dust, and that fraction is unknown here.
- **2005 PM10, and primary copies of the 2005 figures.**

## Differences from the E-PRTR series

- **Thresholds.** INES/EPER: PCDD/F 1 g TEQ (0.001 kg), benzene 1 t, PAH 50 kg, PM 50 t, PM10 50 t.
  E-PRTR: PCDD/F 0.1 g, benzene 1 t, PAHs 50 kg, PM10 50 t. Under E-PRTR, a missing PAH year (2013–2019,
  2021–2024) means the release was below 50 kg or was not reported. It does not mean zero.
- **PAH definition.** INES/EPER used the sum of the 6 Borneff PAHs. E-PRTR "PAHs" are 4 compounds
  (benzo[a]pyrene, benzo[b]- and benzo[k]fluoranthene, indeno[1,2,3-cd]pyrene). The two series are not
  strictly comparable.
- **Method codes.** INES used M/C/S (S = stimato), with P (point only) or P+D (including diffuse/fugitive)
  flags. EPER and E-PRTR use M/C/E. All EPER 2004 values for ILVA are E. E-PRTR 2007–2008 values for PM10,
  dioxins, benzene and PAH are also "Estimated".
- **Size of the jump.** INES/EPER benzene was about 180–230 t a year in 2002–2006, against 15.9 t in E-PRTR
  2007. PAH was about 26–32 t against 1.51 t. The step is too large to read as a real one-year change: it most
  likely reflects a change of estimation basis (for example, fugitive coke-oven emissions) or definition. No
  source found explains it, so a chart should mark the break between registers. Dioxins line up much better:
  91.5 g in 2006 and 99.6 g in 2007.
- **Dioxin TEQ.** INES describes values as "espressi come Teq" without naming the scheme. ARPA Puglia's stack
  measurements, in I-TEQ, estimated about 172 g/yr in 2008 against 93 g/yr in INES (GIP decree p.144).
- **Air vs water.** PeaceLink's 2002 PAH figure is air only. A 2006 PeaceLink figure of 35,480 kg, seen in
  search results but not opened, equals air plus water in INES 2006 (32,239.7 + 3,241.1 kg). PeaceLink may
  therefore mix the two, which is why its 2005 PAH figure is flagged.

## Confidence

- High: 2002 and 2004 (official EPER pages, which match PeaceLink exactly), 2006 (official ISPRA file,
  identical across three versions), and 2024 (official EEA dataset, which matches every earlier year).
- Medium: 2005 total PM and 2005 dioxins (official ARPA figures quoted in a court decree; the dioxin year is
  inferred from PeaceLink and the Camera interrogazione 4-07368 of 2010).
- Low to medium: 2005 benzene and PAH (NGO table only), and the 2002 total PM. The 2002 PM unit is labelled
  "q/a" in the source, but in the same table the 2005 value equals the official 10,979 t.
