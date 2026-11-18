# Port concessions to the steelworks: extra research (18/11/2026)

Scope: (1) where the "Parco Coils" is, (2) status of the concessions in 2024–2026, (3) construction years of the 2nd–5th sporgente.
Files downloaded to this folder are listed at the end. PDF page numbers are the PDF viewer's page (printed page in brackets where it differs).

---

## Q3 first, because it is the cleanest: construction years

Source: AdSP del Mar Ionio, *Documento di Indirizzo alla Progettazione (DIP) – Realizzazione di un impianto di cold ironing presso le banchine pubbliche/in concessione*, albo pretorio, July 2022.
URL: https://port.taranto.it/albopretorio//images/allegati_10/20220701081644_Documento_di_Indirizzo_alla_Progettazione_DIP.pdf
Local: `adsp_cold_ironing_DIP_2022.pdf`

| Pier | Quote | Page |
|---|---|---|
| 2nd sporgente | "Il Secondo Sporgente è ubicato a ponente del Molo S. Cataldo, parallelamente a questo, ad una distanza di circa 300 m. La realizzazione dell'opera risale al periodo 1962-64." Area "circa 90.000 m2". West quay "destinata alla movimentazione di prodotti finiti (tubi, lamiere, coils ecc.)". | PDF 18 [17] |
| Calata 3 | "La Calata 3 è compresa tra il 2° e il 3° Sporgente ha uno sviluppo di circa 230 m ... destinato alla movimentazione di rottami di ferro e loppa d'altoforno". No year given. | PDF 18 [17] |
| 3rd sporgente | "Il Terzo sporgente fu realizzato nel periodo 1970-73" (confirmed). Area "circa 100.000 m2". | PDF 18 [17] |
| 4th sporgente | "Il Quarto sporgente è entrato in esercizio nel 1974" (confirmed). Recently enlarged under the "Piastra Portuale" works. | PDF 18–19 [17–18] |
| 5th sporgente | "Il Quinto sporgente, la cui realizzazione risale alla fine degli anni '70, è situato a circa 2,5 Km a ovest di Punta Rondinella. Il molo è banchinato solo sul fronte di ponente ... La banchina, di lunghezza pari a 1200 m, orientata a SW ... Il terrapieno, profondo circa 250 m, dispone di una superficie operativa pari a circa 600.000 m2. Le banchine e le aree retrostanti sono assentite in Concessione all'azienda siderurgica". | PDF 20 [19] |

Confidence: high for 2nd (1962–64), 3rd, 4th (official AdSP document). Medium for the 5th: the source only says "fine degli anni '70" (late 1970s); no exact year found. Context in the same document: Calata 5 caisson plant "realizzato nel 1976", Molo Polisettoriale "progetto risale al 1977", containment works "1978-83" (PDF 21 [20]).

Consequence for the map (no edits made): `build_port.py` shows the 2nd from 1965 and the 5th from 1965. The 2nd is documented from 1964 (completed 1962–64). The 5th from 1965 is not supported; the only official dating is "late 1970s".

Unknown: exact year the 5th sporgente entered service; whether "1962-64" means construction completed in 1964 or entry into service.

---

## Q1: where the Parco Coils is

### What the sources say

1. **ISPRA, *Controlli presso lo stabilimento ... Acciaierie d'Italia di Taranto*, report I semestre 2023 (rev. 11/10/2023)**
   URL: https://www.isprambiente.gov.it/files2023/controlli-ambientali/relazione-ispra-controlli-stabilimento-ilva-anno-2023_isemestre_rev11ott23.pdf (local `ispra_2023_isem.pdf`)
   - PDF p. 45, inspection 25–27/01/2023, under "Relativamente al V sporgente": "Presso il parco coils – area S11 sono state visionate: la vasca (VP4) e i percorsi dell'interconnecting"; "Le aree S8, S9 e S10 sono allo stato attuale utilizzate come deposito dei coils".
   - PDF p. 46, inspection 7–8/06/2023: "Infine, è stato visionato il parco coils che non è ubicato sullo sporgente marittimo, ma nella zona attigua all'ingresso del medesimo [the V sporgente]".
   - Same page, important for drawing the 5th: "Su tutto il perimetro della parte nord e ovest di sporgente gestito da ADI è presente un cordolo ... La restante parte dello sporgente, lungo parte del lato ovest e del lato sud, è di competenza dell'autorità portuale".
2. **ISPRA report 2024 (already local: `sources/air-extra/dl2/ispra_controlli_ilva_2024.txt`, line ~1938)**: the AIA work schedule lists the plant "AM03 – Impianto trattamento acque meteoriche V sporgente e parco Coils". The Ilva in AS quarterly report (`sources/production/ilvaas_trim_IV2024.txt`, line 1291) has "5° PIER AND COIL YARD RAINWATER MANAGEMENT". The Parco Coils is always grouped with the 5th sporgente.
3. **ILVA, AIA *Relazione tecnica su vincoli territoriali, ambientali e urbanistici*, February 2007**, MASE VA portal. URL: https://va.mite.gov.it/File/Documento/259889 (local `mase_259889.pdf`), PDF p. 5 [Pag 5/33]: "Nella zona ovest tra le aree in concessione rientra il V sporgente (cosiddetto "molo ovest") e l'area antistante. Detta area è separata dalle aree di proprietà dalla S.S. n. 106." The pier is linked to the plant "anche con un raccordo stradale interno di proprietà ILVA".
4. 2013 ILVA notes (Camera Doc. CCIV n. 3 communications register, local `sources/production/mite_293085.txt` lines 6138–6142 and 7249–7251): "da realizzare sul II sporgente, III Sporgente e calata 3 e sul V Sporgente e Parco Coils". Same grouping: V Sporgente together with Parco Coils.

### Description for drawing

- The Parco Coils is **on land, at the root (landward end) of the 5th sporgente, next to its entrance**, not on the pier itself (ISPRA 2023, p. 46).
- It is part of the concession "V sporgente e l'area antistante", which lies **between the pier and SS 106** (ILVA 2007, p. 5).
- OSM (my reading, not an official source): way 885868986 "5° Sporgente Acciaierie d'Italia" runs from the tip at about 40.4949 N, 17.1572 E north-east to the root at about 40.502–40.506 N, 17.168–17.172 E. At the root, SS 106 (ways 74277090, 173656937) and the Ferrovia Jonica pass at about 40.504 N, 17.170 E. There is an untagged OSM gate at 40.50645 N, 17.16944 E (node 11492543633), on the root edge of the polygon (Overpass extract `osm_v_sporgente_root.json`). The coil yard is plausibly in the root/NE part of that polygon, between the quay area and SS 106. **No official source gives coordinates or an outline**, and OSM does not tag the gate as the pier's entrance.

Confidence: high that it is at the root/entrance of the 5th sporgente, on land, inside the concession; low for any exact outline. Drawing it as a separate polygon would need the ADI drawings (DIR 212/2023 of 10/05/2023 and DIR 72/2023 of 17/02/2023, areas S3–S11), which are cited by ISPRA but were not found online. The MASE AIA document list for ILVA (procedure 2038/4338, 44 pages) has no V-sporgente drawing: only DIR 395 for the II sporgente (Documento 678396).

Also relevant for the 5th: the AdSP built a "cassa di colmata" **"in ampliamento al V Sporgente (lato levante)"** (AdSP POT 2017–2019 rev. 2018, PDF p. 74 [72], local `POT2017_2019_rev2018.pdf`; URL https://port.taranto.it/attachments/article/2189/POT2017-2019_REV_2018.pdf). OSM has "Barriera di colmata" ways at about 40.4957–40.4987 N, 17.1659 E. Together with the ISPRA note that part of the west and south sides is under AdSP control, this means the OSM polygon of the 5th may be larger than the ADI concession.

---

## Q2: status of the concessions (2000 → 2026)

### Title and term

- **Concession deed:** "Le aree portuali sono aree demaniali date in concessione all'ILVA dall'Autorità Portuale con atto di riordino n. 5/00 rep. n. 114 in data 22/11/2000 per la durata di anni 50." (ILVA AIA report 2007, `mase_259889.pdf`, PDF p. 5). Arithmetically that runs to November 2050. **No source states the expiry date explicitly**, and the deed itself was not found online.
- Areas covered (same page): "il II, III e IV sporgente comprese le aree ad essi antistanti e confinanti con la cosiddetta "strada dei moli"" plus "il V sporgente (cosiddetto "molo ovest") e l'area antistante". Total "aree demaniali per complessivi mq 931.000" (PDF p. 3). The 2007 text does not name calata 3 or the Parco Coils; the 2013 notes do.
- **Transfer to ArcelorMittal (2018):** "Arcelor ha fatto istanza di subentro nella posizione di ILVA per quanto riguarda la titolarità delle concessioni in essere" (AdSP POT 2017–2019 rev. 2018, `POT2017_2019_rev2018.pdf`, PDF p. 28). No AdSP decree authorising the subentro (art. 46 cod. nav.) was found.

### What the AdSP publishes now

- AdSP page "Terminal Siderurgico", unchanged between 05/08/2021 and 10/08/2026 (Wayback snapshots, local `adsp_terminal_siderurgico_2021.html` and `_2026.html`): "Acciaierie d'Italia ha in concessione quattro sporgenti (numero 2, 3, 4 e 5) e una calata (numero 3) 931.000 mq di aree operative". Live URL (now 404 after the site migration): https://port.taranto.it/index.php/it/banchine-commerciali/terminal-siderurgico ; snapshot https://web.archive.org/web/20260810080804/https://www.port.taranto.it/index.php/it/banchine-commerciali/terminal-siderurgico
- AdSP page "Banchine Commerciali Libere", 2021 and 20/05/2026 snapshots (local `adsp_banchine_libere_2021.html` and `_2026.html`): free quays "(non assentite in concessione) ... la Calata 1, il 1° Sporgente levante, il 1° Sporgente ponente, il 1° Sporgente testata, la Calata 2 e il **4° Sporgente ponente**". So the **west side of the 4th is not in concession**. The cold-ironing DIP (PDF p. 4) also lists "il IV Sporgente lato di Ponente, ampliato nell'ambito ... "Piastra Portuale"" among the public quays.
- AdSP POT 2023–2025, Tabella 10 "Dettaglio destinazione d'uso delle aree e concessioni" (p. 48; source file truncated, see Files). Text recovered from the PDF streams, but the concessionaire names are in an undecodable font, so only "S.p.A." survives:
  - 2° Sporgente Levante, S.p.A., minerale ferro; Testata 2°, sosta tecnica navi; 2° Ponente, materiale siderurgico;
  - CALATA 3, S.p.A., ferroleghe / loppa;
  - 3° Levante, Testata and Ponente, S.p.A., materiale siderurgico / combustibile-catrame;
  - "4° Sporgente levante radice **Cemitaly S.r.l.** ... Carico cemento"; "4° Sporgente Ponente S.p.A. 350.000 ... Scarico ferro carbone"; Testata 4°, S.p.A., imbarco bitume;
  - "5° Sporgente/Molo Ovest S.p.A. 45.000 631.300 Prodotti siderurgici".

  The concessionaire names cannot be read, so I cannot confirm who holds "4° Ponente" in this table. It may conflict with the "Banchine libere" page. The same POT says one bulk terminal is "distribuito lungo quattro sporgenti e una calata" (p. 48). Caution: the "durata di 49 anni" in that POT refers to the **SCCT container terminal**, not ADI. One web-search summary attributed it to ADI wrongly.
- AdSP cold-ironing DIP 2022, PDF p. 20 [19]: "Il 5° Sporgente, attualmente in concessione ad Acciaierie d'Italia S.p.A. (già ArcelorMittal Italia, ancor prima ILVA SpA)".
- ISPRA I sem. 2023, PDF p. 44: "La Società operante per l'Autorità di Sistema Portuale del Mar Ionio in data 27/06/2022 ha iniziato lo sgombero delle aree per la riconsegna ad Acciaierie d'Italia S.p.A. ... verbale di riconsegna delle aree" (AdSP note prot. 8885 of 28/06/2022). This is the opposite direction: areas handed back **to** ADI. The text does not say which areas.
- ISPRA I sem. 2023, PDF p. 46: part of the 5th (part of the west side and the south side) is "di competenza dell'autorità portuale".

### Requests and announcements (press, pointers only)

- **2021, Comune (mayor Melucci):** Shipping Italy, 11/05/2021, https://www.shippingitaly.it/2021/05/11/melucci-comune-di-taranto-ancora-in-pressing-sullex-ilva-restituisca-banchine-portuali-sottoutilizzate/ : the Comune "chiederà la revisione delle attuali concessioni dello stabilimento siderurgico, presumibilmente in relazione al Secondo e al Quarto Sporgente". This was an announced request. No AdSP decision on it was found.
- **22/11/2025, AdSP president Gugliotti (press meeting):** Shipping Italy, https://www.shippingitaly.it/2025/11/22/ultimatum-a-yilport-fra-le-linee-dindirizzo-di-gugliotti-per-il-futuro-del-porto-di-taranto/ : "Ci sono diverse manifestazioni di interesse da parte di alcuni operatori che sarebbero interessati a gestire delle aree oggi date in concessione a Ilva." He added: "ci sarà necessità da parte della grande industria di meno aree". This is the "2025 expressions of interest". They are informal approaches reported by the press; no AdSP public notice (avviso) was found.
- **18/09/2026, Comune (mayor Bitetti, councillor Cosa):** TarantoToday, https://www.tarantotoday.it/politica/porto-ionico-revisione-concessioni-banchine-investimenti-18-09-2026.html (local `tt_concessioni_2026-09-18.html`): a letter to the AdSP asking for "una razionalizzazione delle concessioni demaniali". It names no pier.
- **11/11/2026, AdSP:** Shipping Italy, https://www.shippingitaly.it/2026/11/11/ladsp-di-taranto-prepara-la-controproposta-a-yilport-sul-molo-polisettoriale : "le aree portuali oggi in uso all'ex Ilva ... che la futura configurazione dello stabilimento siderurgico potrebbe in parte liberare"; "Solo una volta scelto il progetto industriale ... sarà possibile capire quali porzioni della circoscrizione portuale resteranno destinate alla siderurgia". Gugliotti has "avviato interlocuzioni informali con la struttura commissariale di Acciaierie d'Italia".

### Bottom line for Q2

As of the latest official AdSP page (Wayback 10/08/2026), the steelworks is still shown as holding the 2nd, 3rd, 4th and 5th sporgente plus calata 3 (931,000 m²). Three qualifications:
- the west side of the 4th is listed as free;
- the root of the east side of the 4th is Cemitaly's (POT 2023–25);
- part of the 5th is under AdSP control (ISPRA 2023).

I found no act of revocation, return or reassignment for 2021–2026. As of November 2026, a reduction is being discussed but not decided (press).

Confidence: medium. The AdSP page may simply not have been updated; the absence of an act is not proof that none exists.

Unknown:
- the deed's expiry date stated explicitly (2050 is inferred from 22/11/2000 + 50 years);
- any later deed numbers (subentro to AM InvestCo/ADI in 2018–2021, position after ADI entered AS in February 2024);
- whether the concessions are held by Ilva in AS (the owner) or by ADI in AS;
- which areas were handed back to ADI in June 2022;
- the AdSP POT 2026–2028 (approved March 2026 per Corriere di Taranto, 18/03/2026), not found online.

Note: the cold-ironing DIP p. 103 says "in concessione ad ENI (II-III-V Sporgente, Pontile ENI e Molo Polisettoriale)". This looks like a drafting error, since the same document's p. 20 says the 5th is ADI's; do not use it.

---

## Files in this folder

- `adsp_cold_ironing_DIP_2022.pdf`: AdSP DIP cold ironing (years of the piers, 5th in concession to ADI).
- `ispra_2023_isem.pdf`: ISPRA controls report I sem. 2023 (Parco Coils location; AdSP part of the 5th; 2022 handback).
- `mase_259889.pdf`: ILVA AIA report 2007 on territorial constraints (atto di riordino 5/00, 50 years, 931,000 m²).
- `POT2017_2019_rev2018.pdf`: AdSP POT 2017–19 rev. 2018 (Arcelor subentro request; cassa di colmata on the east side of the 5th).
- `POT_2023_2025_TRUNCATED_first5MB.pdf`: AdSP POT 2023–25. The live URL returns 404, and the Wayback copy (20250429003151) stops at 5,242,880 bytes, so the PDF does not open. Text of pp. 14–80 was recovered from the raw streams; Tabella 10 concessionaire names are unreadable.
- `adsp_terminal_siderurgico_2021.html` / `_2026.html`, `adsp_banchine_libere_2021.html` / `_2026.html`: Wayback snapshots of AdSP pages.
- `tt_concessioni_2026-09-18.html`: TarantoToday article (press).
- `osm_v_sporgente_root.json`: Overpass extract around the root of the 5th sporgente (ODbL).
