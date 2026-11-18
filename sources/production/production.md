# Taranto steelworks: yearly production (research of 18/11/2026)

Data: `production.csv` (one row per source and value, 76 rows). Units: million tonnes (Mt).
`quantity` is `crude_steel`, `pig_iron` or `capacity`. Only `crude_steel` rows belong on the chart.

## Method

- Searched company reports, AIA files, ministry reports to Parliament, ISPRA control reports,
  academic theses and the press. Downloaded files are in this folder, with a `.txt` text extract
  next to each PDF.
- A value goes in the CSV only when the source states it in numbers for one plant and one year.
  Values read off charts, group totals, Italy totals and plan targets are left out.
- "Acciaio solido" (Ilva, Ministry of Environment) is cast steel, which is crude steel in
  worldsteel terms. I recorded it as `crude_steel`.
- When sources disagree, each value has its own row and the conflict is explained in `notes`.

## Coverage (crude steel)

| Years | Main source | Confidence |
|---|---|---|
| 1966 | Romeo PhD thesis (Verona 2014), citing Finsider's 1966 annual results (IRI archive) | high |
| 1969–1979 | Romeo, Tab. 5.1: Finsider four-year plans, actual output (pig iron as well) | high |
| 1980–1985, 1987, 1990 | Caiazzo PhD thesis (Florence 2025), Fig. 1.15 table: Nuova Italsider 1984 publication (1980–84) and IRI archive files (1985, 1987, 1990) | medium-high |
| 1992–1994 | Caiazzo text, citing the IRI archive and Affinito, De Cecco, Dringoli (Donzelli 2000) | medium |
| 1998 (or 1997–98) | Caiazzo: "nel biennio 1997-1998 ... 9,2 Mt". Year and scope are ambiguous | low |
| 2001 | Caiazzo text (Gazzetta del Mezzogiorno, 28/02/2002) | medium-low |
| 2005 | Ilva AIA application, Scheda A: 9.175 Mt (pig iron 8.604; capacity 15) | high |
| 2006 | three sources that disagree: 10.2 / 9.6 / about 8.5 | low |
| 2007–2010 | Ilva, Rapporto Ambiente e Sicurezza 2011, p. 22 (company table, pig iron as well) | high |
| 2013–2014 | Ministry of Environment reports to Parliament (Doc. CCIV n. 3, 4, 5): 5.682 and 6.219 Mt | high |
| 2015 | ISPRA control reports: "circa 4,7 Mt" | medium |
| 2020–2022 | ADI Sustainability Report 2022 as quoted by GMK Center; ECCO; ISPRA | medium |
| 2023 | Assonime 2025 (matches CEO Morselli) | medium |

## Disagreements with the current `PRODUCTION` points (events.js)

| Year | Site | Finding |
|---|---|---|
| 1964 | 0 | Not verified. The AIA file gives 1964 as the start of "produzione di ghisa e acciaio" (blast furnace 1 started in October 1964). Romeo says the plant "esordì nel 1966" with 2.2 Mt. |
| 1965 | 1.5 | Not verified: the USGS 1965 text is behind a bot wall. Caiazzo's Fig. 1 chart looks consistent, but it has no numbers. |
| 2007 | 10 | **Conflict.** Ilva's own data give 9.368 Mt (Caiazzo: 9.3). Il Post's "quasi 10" is a rounding. Use 9.4. |
| 2013 | 5.7 | Confirmed (5.682). |
| 2014 | 6.3 | **Conflict.** ISPRA says 6.3, but the Ministry report (operator data) says 6.219 Mt, which is 6.2. |
| 2015 | 4.7 | ISPRA only ("circa"). |
| 2020 | 3.4 | ECCO and the ADI report say 3.4; ISPRA says 3.3. Minor. |
| 2021 | 4.1 | Confirmed by the ADI report and ISPRA ("a ridosso dei 4 Mt"). One GMK article (Dec 2022) says 3 Mt without a source. |
| 2022 | 3.5 | The ADI report (via GMK) says 3.5; Assonime says 3.1; UILM (via SteelOrbis, not saved) says about 3.4. |
| 2023 | 3.0 | Confirmed (Assonime). |
| 2025 | 2 | Not checked against a second source. Caiazzo's Fig. 2.4 chart shows about 2, citing Corriere di Taranto (05/03/2026). |

Also in research.md §3:

- **1994, 5.8 Mt is wrong for Taranto.** It is the Riva group's output in 1994, before it bought
  Ilva (Ilva Rapporto Ambiente e Sicurezza 2011, p. 6). Taranto in 1994 was 8.4 Mt (Caiazzo,
  citing Affinito et al.). An unsourced Linkiesta blog gives 8.5.
- **1975, "about 8 Mt (video)"** conflicts with Finsider's actual figure of 7.010 Mt. Taranto first
  passed 7.5 Mt in 1976 (7.761).

## Other conflicts and caveats

- **2006 peak.** Caiazzo gives 10.2 (citing Pirro 2011, which I did not retrieve). Linkiesta gives
  "a little over 9.6" with no source. Assonime calls about 8.5 the 2006 peak, but that cannot be
  a peak when 2005 was 9.18 and 2007 was 9.37. Leave 2006 out until Pirro or an Ilva document
  is checked.
- **2024.** Assonime gives only upper bounds, and they disagree within the same report: "meno di
  2,3" in footnote 179 and "meno di 2 milioni" on p. 31.
- **2017–2021.** ISPRA gives only an average of "circa 4,5 Mt", which is not usable per year.
- **Caiazzo's charts** (Fig. 1, 1.16, 2.4) show a full 1964–2025 line. They are images without
  numbers, so I did not read values off them. Fig. 1.7 also plots non-zero "steel production" for
  1960–63, before the plant existed, which is a further reason not to digitise those charts.
- **Capacity vs output.** The site has often been described by capacity: 10.5 Mt as the
  post-1975 design, 11.5 Mt at privatisation and in AIA 2012, 15 Mt in the 2005 AIA declaration,
  about 10 Mt according to ISPRA. Those rows are labelled `capacity` and are not production.
- **Plan targets** in Romeo's Tab. 5.1 ("Previsioni") were left out.

## Gaps (no reliable yearly figure found)

1964–1965, 1967–1968, 1986, 1988–1989, 1991, 1995–1997, 1999–2000, 2002–2004, 2006 (in
conflict), 2011–2012, 2016–2019, 2024 (bounds only) and 2025 (not checked).

Leads, in order of value:

1. **F. Pirro, "L'incidenza dello stabilimento siderurgico dell'ILVA di Taranto
   sull'economia provinciale e regionale", Rivista economica del Mezzogiorno 1-2/2011, p. 253.**
   Series for 2002–2009. Paywalled on rivisteweb.
2. **L. Pierri, A. Magazzino, *Economia e società a Taranto II*, Nuova Italsider 1984, p. 133.**
   Series for 1964–1984. Library only.
3. **Affinito, De Cecco, Dringoli, *Le privatizzazioni nell'industria manifatturiera italiana*,
   Donzelli 2000, pp. 90–92.** Covers 1994–1998.
4. **S. Romeo, *L'acciaio in fumo* (Donzelli 2019).** Likely has 1980s–2010s figures.
5. **Ministry reports to Parliament after Doc. CCIV n. 6** (2016–2018). Not found under the
   leg17 URL pattern. Each report checks the 8 Mt cap with the full-year output.
6. **ADI Sustainability Report 2022.** Primary source for 2020–2022
   (`https://archivio.lifonti.it/ADI/Sustainability%20Report%20ADI%202022.pdf`). The host has a
   TLS certificate mismatch and the Wayback copy is cut off at 1 MB, so it was not read. ArcelorMittal
   Italia reports would cover 2018–2019.
7. **2011–2012.** Search the Gazzetta del Mezzogiorno of 01/03/2014 (Colucci), Leogrande on
   minima&moralia (29/07/2012), and Ilva's Rapporto Ambiente e Sicurezza 2012 if it was published.
8. **The earlier Ilva Rapporti Ambiente e Sicurezza (2009, 2010)** may cover 2004–2008.
   EDC_dnws1115.pdf (2010 edition) did not respond and has no Wayback copy.

## Files

| File | Used for |
|---|---|
| romeo_tesi_univr_2014.pdf | 1966, 1969–1979, capacity 1975 |
| caiazzo_tesi_unifi.pdf | 1974, 1980–2009 cross-checks, 2006 conflict |
| edc_dnws2124.pdf | Ilva RAS 2011: 2007–2010, Riva group 1994 = 5.8 Mt |
| mite_259942.pdf | AIA Scheda A: 2005 |
| camera_leg17_docCCIV3_part11.pdf, camera_leg17_docCCIV4v1_part03.pdf, camera_leg17_docCCIV5_part03.pdf | 2013, 2014, 2012 AIA capacity |
| camera_leg17_doc204_6_23.pdf | partial 2015 (Jan–Jul) |
| ispra_controlli_2025.pdf | 2013–2015, 2020–2021, 2017–2021 average |
| ecco_taranto_2021.pdf | 2020 |
| astrid_rapporto_ilva_2025.pdf | Assonime: 2006, 2022–2024 |

GMK Center and Linkiesta were read online and not saved.
