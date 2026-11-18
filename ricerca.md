# Ex Ilva di Taranto: ricerca per il sito (18/11/2026)

Legenda: **[P]** letto su fonte primaria/ufficiale · **[S]** solo stampa o fonti secondarie · **DA VERIFICARE** dubbio aperto.
Il video di Barbascura eXtra è usato solo come traccia (`sources/video-barbascura-notes.md`), mai come fonte.

## In breve

- **Progetti già esistenti:** nessuna mappa interattiva, StoryMap o scrollytelling sull'Ilva. Esistono solo timeline testuali (Il Post 2026, Euronews 2025). Lo spazio è libero.
- **Il "chiuso nel 2008":**
  - Non chiude nessun impianto principale. Nel 2008 ci sono la **diossina nel pecorino** (feb–mar), l'**abbattimento delle greggi** delle masserie e la **legge regionale anti-diossina** (dic).
  - Nel video un ex operaio dice che "area a freddo, tubifici e rivestimenti sono chiusi dal 2008". Le fermate di tubifici e rivestimento tubi per crisi di mercato sono documentate. La data 2008 è **DA VERIFICARE**.
- **Mortalità:** esistono solo stime per periodo o scenario, mai una serie annuale. I morti sul lavoro sono conteggi della stampa, non ufficiali.
- **Inquinamento:** dati orari ARPA dal 2005, emissioni dichiarate dallo stabilimento dal 2007, CO2 dal 2005. Prima del 2005 non c'è quasi nulla di misurato. Il buco va mostrato, non riempito.
- **Mappa:**
  - OSM ha la geometria dettagliata dello stabilimento (relation 11843712, circa 15 km²). Mancano però i nomi dei reparti, che vanno aggiunti a mano.
  - Ortofoto storiche esistono (1988, 1994, 2000, 2006, 2012 nazionali; 1997–2023 regionali), ma con licenza incerta: si possono mostrare via WMS, non ri-ospitare.
  - Il volo GAI del 1954 (il "prima") non è scaricabile gratis.

---

## 1. Cronologia

Colonna "Area" = cosa evidenziare sulla mappa.

| Data | Evento | Area | Fonte | Note |
|---|---|---|---|---|
| anni '50 | Campagna a ovest della città: uliveti, vigneti, masserie | tutto il sedime | panorama.it | |
| 9 lug 1960 | Prima pietra del IV Centro siderurgico IRI-Finsider (Italsider) | tutto il sedime | panorama.it; linkiesta.it/2012/08/la-barbarica-industrializzazione-dellilva-secondo-cederna/ | 9 o 10 luglio? I "40.000 ulivi sradicati" sono **DA VERIFICARE** |
| 21 ott 1964 | Si accende l'AFO1 (l'AFO2 il 29 gen 1965) | AFO1, AFO2 | linkiesta.it | Affaritaliani dice 24 ott |
| 10 apr 1965 | Inaugurazione ufficiale | tutto | linkiesta.it; ilpost.it/2026/10/18/ex-ilva-storia/ | Saragat o Moro? Il cinegiornale nel video dice che Moro inaugura "l'acciaieria": forse sono due cerimonie |
| 24 dic 1968 | Paolo VI celebra la messa di Natale nello stabilimento; il quartiere Paolo VI ne prende il nome | stabilimento + quartiere Paolo VI | **DA VERIFICARE** (fonte: video) | |
| 1970–1975 | Il raddoppio: AFO4 e AFO5, circa 10 Mt/anno di capacità | AFO4, AFO5, area nord-ovest | ilpost.it 2026; USGS Minerals Yearbook 1974 | |
| 1994 | Chiuso l'AFO3 (demolito dal 2019) | AFO3 | soc.chim.it/sites/default/files/chimind/pdf/2024_3_18_ca.pdf | fonte unica |
| 1995 | Privatizzazione: Gruppo Riva, 1.649 miliardi di lire + debiti | tutto | ilpost.it 2026 | Il video dice 2,5 miliardi, non torna |
| 27 feb – 5 mar 2008 | PeaceLink fa analizzare un pecorino locale: diossine e PCB circa 3 volte oltre il limite. Segue un esposto in procura | masserie | documenti.camera.it/_dati/leg16/lavori/stenografici/sed414/pdfbt64.pdf | |
| 2008 | Abbattimento delle greggi (masseria Fornaro e altre) | masserie | editorialedomani.it | Numero dei capi discordante: >500 in un giorno, ~1.200 (PeaceLink), >1.300 (video) |
| 2008 | (?) Fermata di area a freddo, tubifici, rivestimento tubi | LAF, tubifici | dichiarazione nel video, 54:36 | **DA VERIFICARE** |
| 19 dic 2008 | L.R. Puglia 44/2008 anti-diossina (0,4 ng TEQ/Nm³ dal 2011) | agglomerato | testo della legge | |
| 2011 | Divieto di raccolta delle cozze nel I seno del Mar Piccolo (diossine/PCB) | Mar Piccolo | **DA VERIFICARE** (fonte: video) | |
| 26 lug 2012 | La GIP Todisco sequestra l'area a caldo senza facoltà d'uso; i Riva vanno ai domiciliari | area a caldo + parchi | ilpost.it/2012/07/27/sei-impianti-dellilva-sotto-sequestro/ | |
| 28 nov 2012 | Tornado: crolla una gru al porto, muore Francesco Zaccaria | sporgenti del porto | **DA VERIFICARE** (data da confermare) | |
| 3 dic 2012 | D.L. 207/2012 "salva-Ilva": la produzione continua. La Consulta lo conferma (sent. 85/2013) | tutto | cortecostituzionale.it/scheda-pronuncia/2013/85 | primo di una lunga serie |
| gen 2015 | Ilva in amministrazione straordinaria (Gnudi, Laghi, Carrubba) | tutto | linkiesta.it/2020/07/ilva-taranto-arcelormittal/ | giorno esatto **DA VERIFICARE** |
| 8–12 giu 2015 | Alessandro Morricella investito dalla ghisa all'AFO2, muore il 12 giugno. L'AFO2 viene sequestrato. Il D.L. 92/2015 è bocciato dalla Consulta (58/2018) | AFO2 | internazionale.it/notizie/2015/06/29/...; cortecostituzionale.it/scheda-pronuncia/2018/58 | |
| 24 ott 2017 | Ordinanza "wind days": scuole dei Tamburi chiuse nei giorni di vento da nord-ovest | Tamburi | ilfattoquotidiano.it/2017/11/27/... | |
| 1 feb 2018 | Parte la copertura dei parchi minerali e fossili (Cimolai) | parchi minerali | comunicato ArcelorMittal 30/04/2019 | fine lavori **DA VERIFICARE** (2019-2020) |
| 1 nov 2018 | Arriva ArcelorMittal (affitto con obbligo d'acquisto; 8.200 addetti a Taranto) | tutto | corporate.arcelormittal.com | |
| 24 gen 2019 | CEDU, *Cordella c. Italia*: violati gli artt. 8 e 13 | città (Tamburi) | giurcost.org/casi_scelti/CEDU/CEDU24-01-19.html | |
| 2 mar 2019 | Chiuse le scuole Deledda e De Carolis, vicine alle collinette contaminate | Tamburi | agi.it 2019-03-02 | |
| 10 ago 2019 | Muore Cosimo Massaro (crollo di una gru) | porto | Il Manifesto/Revelli 2019 (peacelink.it/ecologia/docs/5316.pdf) | |
| 4 nov 2019 | ArcelorMittal annuncia il recesso dopo la revoca dello scudo penale | tutto | ilpost.it/2019/11/04/... | |
| 27 feb 2020 | Ordinanza del sindaco Melucci: rimuovere le emissioni o spegnere. Il TAR la conferma, il Consiglio di Stato la annulla (23 giu 2021) | area a caldo | ilpost.it/2021/06/23/... | |
| 14 apr 2021 | Nasce Acciaierie d'Italia; Invitalia al 38% | tutto | comunicato ArcelorMittal | il 68% indicato nel video è **DA VERIFICARE** |
| 31 mag 2021 | Sentenza di primo grado "Ambiente Svenduto": 26 condanne, confisca dell'area a caldo | area a caldo | ilpost.it/2021/05/31/... | |
| 5 mag 2022 | Altre condanne CEDU (Ardimento e altri c. Italia) | città | lawpluralism.unimib.it | |
| 20 feb 2024 | Acciaierie d'Italia in amministrazione straordinaria; esce ArcelorMittal | tutto | mimit.gov.it | |
| 25 giu 2024 | Corte di Giustizia UE C-626/22: con un pericolo grave l'attività va sospesa | area a caldo | curia.europa.eu/jcms/jcms/p1_4443799 | |
| 13 set 2024 | Ambiente Svenduto annullata in appello, atti trasferiti a Potenza | — | ilpost.it/2024/09/13/... | |
| 15 ott 2024 | Riparte l'AFO1 | AFO1 | milanofinanza.it | |
| 7–8 mag 2025 | Incendio all'AFO1 e sequestro; 3.926 lavoratori in CIG | AFO1 | ilfattoquotidiano.it/2025/05/08/... | |
| 2025 | Gare di vendita: Baku Steel (mar), poi Flacks (dic); entrambi si ritirano | — | ansa.it; agi.it; teleborsa.it | |
| 12 gen e 2 mar 2026 | Due operai morti sul lavoro | — | lapresse.it (2026/01/12, 2026/03/02) | nomi da aggiungere |
| 6 feb 2026 | "Ambiente Svenduto bis" a Potenza: 21 rinviati a giudizio | — | ilfattoquotidiano.it 2026/02/06 | |
| 21 feb 2026 | Riparte l'AFO2 | AFO2 | ladige.it | |
| 26 feb 2026 | Il Tribunale di Milano (azione inibitoria dei cittadini) sospende l'area a caldo | area a caldo | teleborsa.it 2026/02/26 | dal 24 o dal 26 agosto? **DA VERIFICARE** |
| 27 lug 2026 | Corte d'Appello di Milano (Genitori Tarantini): stop entro 90 giorni per l'amianto nei cowper e le polveri | area a caldo (cowper) | agi.it 2026-07-27; tg24.sky.it | |
| 8 ott 2026 | Produzione ferma, impianti in preriscaldo | area a caldo | italiaoggi.it | |
| 29 ott 2026 | La Cassazione conferma lo stop: 2.140 t di amianto | area a caldo | agi.it/economia/news/2026-10-29/ex-ilva-taranto-cassazione-39767804/ | |
| 3 nov 2026 | Inizia lo spegnimento degli altiforni; CIGS fino a 8.622 lavoratori | AFO1, AFO2, AFO4 | avvenire.it | |
| 8–9 nov 2026 | Offerte di Jindal e Arvedi; nessuna aggiudicazione al 18/11 | — | Teleborsa 2026-11-09 | situazione in corso |

---

## 2. Salute e mortalità

**Regola per il sito:** tenere sempre separati i **conteggi** (morti sul lavoro, casi osservati) dalle **stime attribuibili** (modelli). Accanto a ogni numero vanno sempre periodo, popolazione, fonte e intervallo di confidenza.

### Stime di decessi attribuibili alle emissioni

| Stima | Periodo | Popolazione | Valore | Fonte |
|---|---|---|---|---|
| Perizia 2012, effetto a breve termine (PM10 oltre il limite OMS di 20 µg/m³) | 2004–2010 | Borgo + Tamburi | **91 decessi** (IC80% 55–127); circa **40** correggendo per la fragilità. Inoltre 160 ricoveri cardiaci e 219 respiratori | [P] Camera Doc. CCIV-bis n.1 leg. XVII, p.113 |
| Perizia 2012, effetto a lungo termine | 1998–2010 (13 anni) | coorte Taranto, Massafra, Statte | **386 decessi** (30/anno, 1,4% del totale); 237 tumori, 937 ricoveri respiratori (638 pediatrici) | [P] testo citato via ISDE/PeaceLink e Domani; perizia originale non aperta |
| OMS, valutazione d'impatto | 10 anni prima dell'AIA (scenario 2010) | adulti >30 anni | **270–430** morti premature; 5–8/anno nello scenario post-AIA 2015 | [S] Quotidiano Sanità 21/01/2022 |
| VIIAS 2019 | scenari 2010 / 2012 / 2015 | Taranto | circa **28 / 18 / 5** decessi/anno | [S] Quotidiano Sanità 24/10/2019 |

Le cifre "83 morti l'anno" e "174" che girano in rete non sono riconciliabili con la perizia: non usarle.

### SENTIERI (ISS), comuni di Taranto e Statte

- **6° rapporto, 2023** [P]: *Epidemiol Prev* 2023;47(1-2) Suppl 1, pp.227–230.
  - **Mortalità 2013–2017:**

    | Causa | Uomini | Donne |
    |---|---|---|
    | Tutte le cause | SMR 110 | SMR 107 |
    | Tutti i tumori | SMR 114 | SMR 104 |
    | Polmone | SMR 118 | SMR 125 |
    | **Mesotelioma pleurico** | **SMR 366** (40 casi) | **SMR 359** (10 casi) |

  - **Bambine, ricoveri:** tutti i tumori SHR 153; leucemia mieloide SHR 814, su 5 casi.
  - **Mortalità pediatrica complessiva:** "in difetto o in linea con l'atteso". Va detto anche questo.
- **Aggiornamento ISS di circa il 2014** [S, due fonti concordi]. Fascia 0–14 anni:
  - incidenza dei tumori 2006–2008: **SIR 154**, cioè **20 casi contro 13 attesi (+54%)**. Il video riporta correttamente questo dato.
  - mortalità 2003–2010: SMR 121.
- **Rapporto regionale 2021** sui tumori pediatrici [P], intera provincia, 2006–2017: SIR 1,10, non significativo.
- **Mesotelioma "+350% / +200%" nel video:** non coincide con il 6° rapporto (+266% / +259%). Usare SENTIERI 6.

### Studio di coorte (Regione, DEP Lazio, ASL, ARPA, AReS; 2016)

- Coorte di 321.356 residenti di Taranto, Statte e Massafra, seguiti dal 1998.
- Hazard ratio per 10 µg/m³ di inquinante di origine industriale:

  | Esito | PM10 industriale | SO2 industriale |
  |---|---|---|
  | Mortalità per cause naturali | 1,04 | 1,09 |
  | Incidenza tumore del polmone | 1,29 | 1,42 |
  | Incidenza tumore del rene | 1,32 | 2,44 |

- Tamburi e Paolo VI sono i quartieri più colpiti. Bambini 0–14: ricoveri respiratori +24% ai Tamburi e +26% a Paolo VI [S].

### Valutazioni del Danno Sanitario (ARPA, AReS, ASL)

Residenti con rischio cancerogeno inalatorio aggiuntivo superiore a 1 su 10.000:

| Valutazione | Scenario | Residenti |
|---|---|---|
| VDS 2013 [P] | 2010, prima dell'AIA | circa **22.500** |
| VDS 2013 [P] | 2016, dopo l'AIA | circa **12.000** |
| VDS 2014/15 [P] | 2016 con le altre fonti, porto compreso | **14.141** |

Le VDS 2018, 2021 e 2024 concludono che il rischio ai Tamburi è "non accettabile" [P: audizione della Regione al Senato, 11/02/2025].

### Morti sul lavoro (conteggi, non ufficiali)

- Non esiste un elenco ufficiale.
- **208** morti per incidenti dal 1° agosto 1961 (Giovanni Gentile) al 10 agosto 2019 (Cosimo Massaro): Revelli, *Il Manifesto*, 17/11/2019.
- Serie annuale (ricerca del 18/11/2026): nessun elenco pubblico anno per anno. Esistono solo conteggi parziali con criteri diversi: 71 ufficiali nel 1960–1963 (Attino, in Il Post 12/01/2013), 45 nel 1993–2012 (Contropiano, 2012), 25 dal 2003 al marzo 2026 (Il Fatto Quotidiano, 02/03/2026). Possibili fonti per un elenco nominativo: INAIL, associazione 12 Giugno, ANMIL, archivi sindacali.
- Seconda ricerca (18/11/2026): **nessun elenco completo dal 1961**. A. De Palma (*Il de Martino* n. 22-23, 2013) scrive che nessuno (sindacati, INAIL, ispettorato, ASL) ha tenuto il conto; cita Gentile (1/8/1961, 23 anni, travolto da traversine) e 20 morti nel 1964, quasi tutti delle ditte. Revelli (2019) non cita la fonte del 208.
- **Verifica caso per caso (18/11/2026)**: `sources/work_deaths_check.json`, dati del sito in `work-deaths.js` (generati da quel file). Scelte: escluso Francesco Tomai (malore nello spogliatoio, 2021); aggiunti Antonio Mingolla (18/04/2006, gas all'altoforno 1, ditta Cmt) e Vito Antonio Rafanelli (morto 22/08/2006, tubificio, sentenza Trib. Taranto 13/08/2012), assenti nell'elenco del Fatto; Satta solo anno (27 settembre per il Fatto, 27 ottobre dal Manifesto); Di Leo come "Luigi" (cronache 2005–2008); Paurowicz 54 anni; Salamida 47 (agenzie; il Fatto dice 46); età omesse per Mingolla e Rafanelli (fonti deboli); Di Natale confermato solo per dinamica, nome solo dal Fatto. Anni del cantiere: Nistri (2009, via Leogrande) 18/28/23/32 morti nel 1961–64, De Palma 20 nel 1964.
- **Elenco nominativo 2003–2026**: P. De Rubertis, *Il Fatto Quotidiano*, 02/03/2026 (titolo "25 vittime", nel testo 24 nomi con data e dinamica). Per anno: 2003: 2 · 2004: 2 · 2005: 2 · 2006: 1 · 2007: 2 · 2008: 3 · 2012: 2 · 2013: 1 · 2014: 1 · 2015: 2 · 2016: 1 · 2018: 1 · 2019: 1 · 2021: 1 (Tomai, malore nello spogliatoio, non chiaramente infortunio) · 2026: 2. Da incrociare con le singole cronache prima di pubblicare.
- **286** contando anche la costruzione: conteggio della stampa riportato da T. Attino, *Generazione Ilva*.
- Va mostrato come un intervallo con la fonte. Le malattie professionali sono escluse.
- Per avere una serie per anno servirebbe compilare un elenco caso per caso: è un lavoro grosso, ma sarebbe un contributo originale del sito.

### Scelta editoriale (18/11/2026)
Le **stime da modello non vengono mostrate sul sito**: i 386 e i 91 decessi della perizia, i 270 della valutazione OMS, i 22.500 residenti della VDS. Sono troppo facili da contestare finché non le citiamo dai documenti originali. Restano in `events.js` con `kind: 'estimate'` e vengono filtrate all'avvio della pagina, quindi si possono riattivare togliendo una riga.

Sul sito restano solo **conteggi e misure**: i 208 morti sul lavoro, il +54% di tumori infantili, il benzo(a)pirene e il mesotelioma ×3,7.

### Cosa si può rappresentare graficamente
- **Barre per periodo:** SENTIERI (con l'avvertenza che i metodi cambiano tra un rapporto e l'altro).
- **Punti per scenario:** VDS, OMS e VIIAS, dichiarando che gli anni sono scenari modellati.
- **Schede:** stime singole come i 386 decessi della perizia.
- **Linea del tempo dei casi:** i morti sul lavoro.

---

## 3. Inquinamento e produzione

| Serie | Da | Formato | Dove |
|---|---|---|---|
| Qualità dell'aria ARPA: PM10, PM2.5, SO2, NO2, benzene, IPA, black carbon; centraline Machiavelli, Tamburi, Archimede, Statte… | **2005** | orari, xlsx per centralina dentro zip/rar annuali; le medie annue vanno calcolate | arpa.puglia.it/pagina3139_dati-storici-qualit-delllaria.html |
| Benzo(a)pirene a Tamburi (obiettivo 1 ng/m³ superato nel 2009–2011) | circa 2008 | solo PDF delle relazioni annuali | arpa.puglia.it/pagina3076_reportistica-aria.html |
| Deposizioni di diossine e PCB (Masseria Carmine, Tamburi, Talsano) | 2008–2019 | solo PDF | relazioni ARPA |
| Diossine dal camino E312 dell'agglomerato | campagne 2007–08 (96–172 g I-TEQ/anno); continuo dal 2016 | PDF | ARPA (copia su PeaceLink) |
| Emissioni dello stabilimento (diossine, PM10, SO2, NOx, benzene, CO2) | **2007** (EPER: 2001 e 2004) | database EEA "Industrial Reporting under IED and E-PRTR" | industry.eea.europa.eu |
| CO2 EU ETS (verificata) | **2005** | Union Registry; mirror euets.info | ID dell'impianto **DA TROVARE** |
| Produzione di acciaio | — | **nessuna serie pubblica continua** | |

Valori sparsi di produzione:

| Anno | Produzione |
|---|---|
| 1965 | 1,5 Mt |
| 1975 | circa 8 Mt (video) |
| 1994 | 5,8 Mt |
| circa 2007 | circa 10 Mt |
| dopo il 2012 | limite AIA di 6 Mt |
| 2022 | circa 3 Mt |
| 2025 | circa 2 Mt |

Fonti per completarla: USGS Minerals Yearbook (capitolo Italia), dichiarazioni EMAS e bilanci dell'azienda, relazioni ISPRA. La CO2 ETS può fare da indicatore indiretto dal 2005.

Prima del 2005 non c'è nulla di misurato online: sul grafico va mostrato come area vuota con la scritta "nessun dato".

### Medie annue calcolate (18/11/2026)

`build_air.py` legge i file orari ARPA delle centraline di Taranto (`sources/arpa-taranto/`, id degli archivi in `sources/arpa-archive-ids.txt`). Produce due file:

- `air-data.csv`: tutte le medie, ciascuna con il numero di ore valide.
- `air.js`: solo le medie con almeno il 75% delle ore valide nell'anno.

**Lettura dei dati:**
- **PM10 a via Machiavelli (Tamburi):** sale da 31,5 µg/m³ (2008) a 36,8 (2011), poi scende a 21,4 nel 2025.
- **Talsano, il confronto lontano dalla fabbrica:** 24–26 µg/m³ nel 2009–2011, circa 18–21 dal 2017. La differenza con i Tamburi si riduce dopo il 2012.
- **Paolo VI:** scende da circa 33 µg/m³ (2005–07, anni con poche ore valide) a circa 16–17 dal 2013.

**Problemi noti:**
- **Machiavelli 2006:** PM10 a 16,4 µg/m³, con mediana oraria 14,7. È coerente con i dati grezzi, ma metà degli anni vicini. Forse lo strumento era diverso: **DA VERIFICARE** con ARPA. Sul sito resta visibile, con una nota.
- **SO2 e benzene nel 2008:** valori alti a tutte le centraline, molti zeri a Talsano e massimi anomali (999 di NO2). Questi inquinanti non sono usati sul sito.
- **Via Orsini (Tamburi):** nel file 2024 il foglio ha l'intestazione "ILVA 1 ARIA", quindi potrebbe essere una centralina della rete dell'azienda gestita da ARPA. Va verificato prima di usarla.
- **Anni senza media valida a via Machiavelli:** 2005, 2007 e 2013. Il 2013 manca nel file regionale.
- Benzo(a)pirene e diossine non sono nei file orari.

---

## 4. Mappa e immagini

- **OpenStreetMap** (ODbL, attribuzione "© OpenStreetMap contributors"):
  - Lo stabilimento è la relation 11843712, bbox 40.4907,17.1693 – 40.5251,17.2247.
  - Contiene circa 1.350 edifici, 282 binari, 180 silos e 25 ciminiere. Sono nominati solo ACC/1, ACC/2, Parchi Minerali, LAF, TNA/1–2 e OFE-CAP.
  - Altiforni e cokerie vanno etichettati a mano.
  - Query Overpass (usare un mirror, es. overpass.private.coffee):
    ```
    [out:json][timeout:100];
    rel(11843712); map_to_area->.a;
    (nwr(area.a)[building]; nwr(area.a)[man_made]; nwr(area.a)[railway]; nwr(area.a)[landuse];);
    out geom;
    ```
- **Geoportale Nazionale**:
  - WMS `http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/WMS_v1.3/raster/<MAP>.map`, con le ortofoto `ortofoto_bn_88`, `ortofoto_bn_94`, `ortofoto_colore_00`, `_06`, `_12`.
  - **Licenza incerta:** vanno mostrate dal WMS con attribuzione, senza salvare tile. Prima di farne una copia, scrivere a gn@mase.gov.it.
- **SIT Puglia**:
  - Ortofoto 1997, 2006, 2010, 2011, 2013, 2015, 2016, 2019, 2022, 2023, più le carte IGM 1:25.000. Elenco dei servizi: webapps.sit.puglia.it/arcgis/rest/services/BaseMaps.
  - Licenza non dichiarata: scrivere a info@sit.puglia.it.
- **Volo GAI 1954–55 (IGM)**: è l'immagine perfetta del "prima", ma va comprata a fotogramma e la vendita risulta sospesa. Non si conosce un mosaico pugliese georeferenziato.
- **Satelliti**: Landsat dal 1972/1984 è di pubblico dominio e basta per la crescita dello stabilimento a 30–60 m. Sentinel-2 dal 2015 è libero, con attribuzione Copernicus.

**Proposta per il "prima":** la versione stilizzata è un vantaggio. Il 1955 si può disegnare (uliveti, masserie, linea di costa) usando come riferimento le carte IGM e la prima ortofoto disponibile, senza bisogno di ri-ospitare immagini protette.

---

### Impianti in 3D (`build_plants.py`, 18/11/2026)

**Posizioni:** rilevate a mano sull'ortofoto 2023 della Regione Puglia.
- **Altoforni:** 4, riconosciuti dalle file di cowper, dai campi di colata e dai nastri di carico. Sono 4 come quelli rimasti dopo la demolizione dell'AFO3, ma **la numerazione AFO1/2/4/5 non è assegnata** perché manca una planimetria.
- **Camino E312:** coincide entro 18 m con il camino OSM 383684495.
- **Gasometri:** 3, più 2 serbatoi cilindrici.
- **Cupole:** 3, tracciate dalla foto.

**Dimensioni:**
- **Copertura del parco minerale:** dichiarata 700 × 250–254 m, alta 77 m all'estradosso (VIA MASE; Cimolai indica 355.600 m²). Nella foto la sua impronta misura circa 500 × 270 m per navata: la differenza va chiarita.
- **Tutto il resto è stimato:** E312 210 m (valore diffuso, nessuna fonte trovata), altoforni 85 m, cowper 50 m, parco fossile 45 m.

**Tempi:**
- La mappa mostra i 4 altoforni dal 1965, ma due sono del raddoppio 1970–75: le fasi di costruzione non sono distinte.
- Le coperture compaiono dal 2020 per il parco minerale e dal 2022 per il fossile; prima ci sono cumuli stilizzati.

**Planimetria ufficiale trovata (18/11/2026).** Portale MASE, procedura AIA 2011, file in `sources/aia/`:
- **B.20, doc. 260022:** planimetria CAD del 2007 con tutti i camini siglati.
- **B.6, doc. 260236:** tabella dei 278 camini con impianto di provenienza e **altezza ufficiale**.
  - E312 (agglomerazione linee D-E): **210 m**.
  - Camini delle cokerie: 100–127 m.
  - Camini dei cowper: 64–71 m.
  - Campi di colata: E111 (AFO1), E112 (AFO2), E113 (AFO3), E114 (AFO4), E115/E116 (AFO5).
  - Cowper: da E134 a E138, uno per AFO dall'1 al 5.

**Numerazione degli altoforni.** La B.20 è allineata alla mappa con una similitudine (`sources/aia/georef_B20.py`). I punti di controllo sono i due serbatoi e il gasometro: rotazione 87,7°, scarto inferiore a 10 m. Ogni coppia di camini cade a 23–108 m da uno dei 4 forni riconosciuti nella foto, senza ambiguità: **AFO1 e AFO2** a sud-ovest, vicino ai due serbatoi; **AFO4 e AFO5** a nord-est. L'AFO5 è fermo dal 2015 (ISPRA).

**Camini e cokerie (aggiornamento).** `sources/aia/build_stacks.py` produce `stacks.json`:
- **Camini estratti:** 115. Di questi, 107 sono pallini estratti in automatico dal PDF vettoriale della B.20; 8 sono stati letti a mano in zona cokerie, dove l'estrazione non li prende.
- **Sigle e altezze:** le sigle sono lette a vista sulle etichette. **61 camini** hanno l'altezza ufficiale della B.6; gli altri sono grigi, disegnati a 30 m.
- **Verifica indipendente dell'allineamento:** l'E312 cade a 9 m dal camino OSM.
- **Limiti:**
  - la B.6 conta 278 camini, quindi ne mancano circa 160, quasi tutti bassi (officine, tubifici, laminazione);
  - le sigle con "?" sono letture incerte.

**Batterie delle cokerie:** 12 edifici OSM lunghi e stretti (L > 60 m, orientamento di circa 35°), entro 320 m dai camini E422–E426. Altezza stimata 18 m.

**Correzione sulle cupole:**
- La grande a nord-ovest copre il **parco fossile**, completata nel 2021–22.
- La grande a sud-est copre il **parco minerale**, completata nel 2020. Lo indicano le scritte della B.20 allineata, e torna con i 355.600 m² di Cimolai, pari a 2 × 700 × 254 m.
- La terza, a nord-est, è una copertura costruita tra il 2019 e il 2022 su un parco con cumuli grigi: **quale parco sia non è verificato**.

### Altezze dal rilievo laser (18/11/2026)

**Dati:** Banca dati PST del Ministero dell'Ambiente (sim.mase.gov.it/pst), LiDAR DSM First e DTM a 1 m, licenza CC BY 4.0. Sono 29 tessere sullo stabilimento, voli di marzo e dicembre 2008 e del 2010, salvate in `sources/lidar/`.
- **Download:** il carrello dell'app invia una POST a `https://sim.mase.gov.it/core/api/esri/api/v1/downloads` con `{canale: 'PST2', prodotto: 'LIDAR_2014', layer: 'dsm_first_1x1' | 'dtm_1x1', tileList: [{fid, tavola, regione, contratto}]}`, al massimo 20 tessere per richiesta. Lo stato si legge in `.../downloads/{idSessione}` e il file in `.../downloads/{id}/file/{n}`. Le tessere si trovano su `Grigliato_lidar/FeatureServer/2`.
- **Formato:** GeoTIFF WGS84, 1000 × 1000 pixel da 1e-5°, nodata -9999.

**Metodo (`build_heights.py`):** altezza = DSM − DTM. Per ogni edificio si prende l'85° percentile dei pixel interni; per i camini, il picco entro 15 m.

**Verifiche contro le altezze AIA:**

| Camino | LiDAR | AIA |
|---|---|---|
| E312 | 209,8 m | 210 m |
| E424 | 125,6 m | 125 m |
| E423 | 99,0 m | 100 m |
| E425 | 128,1 m | 125 m |
| E138 | 67,6 m | 71 m |

**Risultati:**
- 1.486 edifici dello stabilimento su 1.640 e 735 edifici della città hanno l'altezza misurata. Sotto i 2,5 m resta la stima: edifici costruiti dopo il 2010 o non visti dal rilievo.
- Altoforni misurati: AFO1 84 m, AFO2 83 m, AFO4 90 m. Per l'AFO5 nessun picco è attribuibile entro 25 m, quindi l'altezza resta ricostruita.
- Gasometri: tra 58 e 83 m.

**Limiti:**
- I cumuli dei parchi non sono misurabili: il DTM li include nel terreno, quindi DSM − DTM ≈ 0.
- Le coperture dei parchi sono successive al rilievo.
- I camini con sigla vengono spostati sul picco del rilievo solo quando le altezze concordano entro il 20%.

### Nastri, collinette, cumuli e porto (18/11/2026)

- **Nastri e condotte sopraelevate** (`build_conveyors.py` → `conveyors.js`):
  - Metodo: rilevatore di creste sottili sul DSM − DTM a 2 m (cella ≥ 3 m e terreno più basso di 3 m su entrambi i lati entro 4–6 m, in almeno una direzione), limitato al perimetro dello stabilimento.
  - Segmenti estratti con RANSAC (≥ 40 m, rettilinei); scartati quelli sopra edifici OSM per più del 30%, cioè i colmi dei tetti.
  - Risultato: 722 segmenti, circa 68 km (l'ISPRA indica 60 km di nastri).
  - Il metodo non distingue nastri e condotte: per questo legenda e scheda le citano insieme.
  - Tentativi scartati: soglia a 5–8 m con edifici allargati e filtro di allungamento, che prendeva filari d'alberi e bordi dei capannoni.
- **Collinette ecologiche** (`build_reliefs.py`):
  - Fascia tracciata sul DTM; rilievo misurato come DTM meno il 5° percentile del piano in blocchi da 100 m.
  - Risultato: 9,5 ha, in linea con i circa 9 ha del sequestro del 2019. Mostrate dal 1975 («anni Settanta»).
- **Cumuli dei parchi:** il DTM li include nel terreno, quindi la forma è misurata. Coprono 5,5 ha nel parco minerale, 6,6 ha nel fossile e 2,9 ha nel terzo parco. Sostituiscono i cumuli schematici.
- **Porto** (`build_port.py`):
  - Da OSM `osm-port.json`: 5° sporgente (way 885868986), 5 nastri ArcelorMittal con quote LiDAR, 50 linee di pontili e dighe.
  - Gru: assenti in OSM.

**Ordine di build:** `build_map`, `build_heights`, `build_map`, `build_plants`, `build_conveyors`, `build_reliefs`, `build_port`.

## 5. Progetti esistenti

Non esiste niente di interattivo. Le cose più vicine:

| Progetto | Cosa offre |
|---|---|
| Il Post, storia dell'ex Ilva (18/10/2026) | timeline testuale |
| Euronews, "Shadows of indifference" (06/2025) | timeline in un articolo |
| PeaceLink | analisi in PDF dei dati ARPA, metodo contestato: rifare i calcoli sui dati originali |
| Global Energy Monitor, Global Iron and Steel Tracker | capacità degli impianti, probabilmente CC BY 4.0 |

---

## 6. Verifiche (aggiornate il 18/11/2026)

Le fonti di ciascun punto sono in `events.js`.

| # | Punto | Esito |
|---|---|---|
| 1 | Fermate 2008 di area a freddo, tubifici e rivestimenti | **Smentito.** Nel giugno 2012 tubifici e laminatoi a freddo sono ancora in marcia, con fermate temporanee; a novembre 2012 l'area a freddo ha 1.942 addetti. La crisi 2008–09 porta solo cassa integrazione. L'affermazione del video non va usata. |
| 2 | Inaugurazione | **Due cerimonie.** Moro inaugura l'acciaieria a novembre 1964 (cinegiornale Luce del 26/11/1964). Saragat inaugura il Centro il 10/04/1965. Il Post attribuisce a Moro il 1965: è sbagliato. |
| 3 | Prima pietra | 9 luglio 1960 (probabile, Linkiesta). I "40.000 ulivi" non hanno nessuna fonte autorevole: tolti. |
| 4 | Messa di Paolo VI | Confermata: notte del 24–25/12/1968 (vatican.va). Che il quartiere Paolo VI prenda il nome dalla visita **non è confermato**. |
| 5 | Cozze nel Mar Piccolo | 2011: blocco della ASL (luglio, notizia di stampa), poi ordinanza regionale n. 1989/2011, di cui non si conosce la data. Divieti rinnovati nel 2016 e nel 2018. |
| 6 | Morti delle gru | Francesco Zaccaria, 28/11/2012. Cosimo Massaro, **10 luglio 2019**: Revelli scrive 10 agosto, ed è sbagliato. Sull'età di Massaro le fonti non concordano. |
| 7 | Coperture dei parchi | Parco minerale coperto al 100% all'ispezione ISPRA del 18–21/02/2020. Parco fossile coperto, verifica ISPRA del 26/01/2022 (scadenza 31/10/2021). |
| 8 | Amministrazione straordinaria 2015 | Decreto MISE del 21/01/2015; D.L. 1/2015. |
| 9 | Sospensione del Tribunale di Milano | Dal 24 agosto 2026, salvo revisione dell'autorizzazione ambientale. |
| 10 | Produzione per anno | Punti con fonte: 1965, 2007, 2013–2015 (ISPRA), 2020–2023, 2025. **Manca quasi tutto il 1966–2006.** Fonti da cercare: relazioni Finsider/Italsider, annuari Federacciai, S. Romeo. |
| 11 | Licenze delle ortofoto | Ancora aperto. |
| 12 | Morti sul lavoro | Non si sa chi abbia compilato il conteggio di 208. Il 286 di Attino riguarda i primi anni dal cantiere (contro 71 ufficiali nel 1960–63), non tutta la storia. Morti 2026: Claudio Salamida (12/01) e Loris Costantino (02/03). |

**Salute:**
- **"91 decessi":** sono il totale del 2004–2010, non un valore annuale.
- **"386 decessi":** trovati solo in fonti secondarie; la perizia originale (va.mite.gov.it) restituisce 404.
- **Valutazione OMS:** pubblicata nel 2023 (ISBN 9789289058360): 270 morti premature in 10 anni nello scenario 2010, fino a 430.
- **+54% di tumori nei bambini:** il dato viene dalla relazione ISS 2014 e riguarda l'incidenza, non la mortalità.

**Verifiche del 18/11/2026 (seconda tornata), già applicate al sito:**
- **Benzo(a)pirene:** confermato dalla tabella 3 del report ARPA 2016 (id 5310): 1,39 / 1,82 / 1,14 ng/m³ nel 2009–2011; 0,76 nel 2012. Il PDF è in `sources/arpa-bap/`.
- **+54% di tumori infantili:** confermato sulla relazione ISS 2014, p. 189, nella copia d'archivio Wayback dell'URL ufficiale iss.it, che oggi risponde 404: «20 casi osservati rispetto a 13 attesi (SIR=154, IC90% 102-224)». Il PDF è in `sources/`. Sono citati anche la sintesi della Camera e Cannone et al., E&P 2015.
- **1955:** la fonte Panorama è sostituita da Gamba (Geotema 72, AGEI) e da La Stampa 1965 citata da Linkiesta. Tolte le "masserie", per cui non c'è una fonte autorevole. Nota Treccani (Cella e Fortunato 2015): «acciaio fra gli ulivi» era anche un'immagine promozionale.
- **1995:** prezzo delle azioni 1.460 miliardi di lire, 1.649 dopo l'arbitrato del 2000; incasso complessivo per il Tesoro 2.514 miliardi (Libro bianco MEF 2001); circa 1.500 miliardi di debiti trasferiti a parte. Firma a marzo 1995, closing il 28/04/1995 (Assonime).
- **Cozze:** ordinanza **ASL Taranto** n. 1989 del 22/07/2011 (non della Regione); ordinanza del presidente della Regione n. 188/2016.
- **ArcelorMittal 2018:** il comunicato originale risponde 404; si usa la copia d'archivio. Tolti gli "8.200 addetti", che il comunicato non riporta.
- **Emissioni EEA:** PM10, diossine, benzene e IPA dal 2007 al 2023, dalla vista Tableau del portale europeo, esportata in CSV da `build_emissions.py`. Si usa solo la facility 2007001763; la CO2 è esclusa perché dal 2015 il portale la somma alla centrale elettrica.

**Ancora aperti:**
- data dell'ordinanza regionale 1989/2011;
- chi ha compilato l'elenco dei 208;
- pagine della perizia originale;
- produzione 1966–2006;
- licenze delle ortofoto;
- origine del nome del quartiere Paolo VI;
- Machiavelli 2006 (§3).

## File

- `sources/video-barbascura-notes.md`: affermazioni del video con minuto e stato di verifica.
- `sources/video-barbascura-transcript.txt`: trascrizione automatica.
- `sources/extracts/`: testi estratti da SENTIERI 6, VDS ARPA, atti Camera e Senato, perizia (via ISDE), Revelli.

### Moli in concessione (18/11/2026)
- Fonte della concessione: nota ILVA DIR/407 dell'11/11/2013 (registro comunicazioni, Camera Doc. CCIV n. 3): "II Sporgente, III Sporgente e calata 3, del IV, del V Sporgente e Parco Coils ... aree demaniali ... in concessione ad ILVA S.p.A.".
- Identificazione: PRP AdSP, tavola C2.12 (`sources/adsp/sheet_C2_12.pdf`): da ovest pontile petroli, darsena servizi, 4°, calata 4, 3°, calata 3, 2°, calata 2, 1°, molo San Cataldo. OSM ha un contorno solo per il 5° (way 885868986); 2°–4° ritagliati dalla costa (way 176922694) in `build_port.py`, chiusi fra gli spigoli alla radice (la fascia di banchina iniziale sovrapponeva i poligoni); calata 3 non disegnata, `sources/osm-piers/port2.json`.
- Anni: 3° 1970–73 e 4° in esercizio dal 1974 (AdSP); 2° e 5° mostrati dal 1965, **anno non documentato**: da verificare. Parco Coils non mappato (posizione non trovata).
- Stato attuale: nel 2021 il Comune chiedeva la restituzione del 2° e 4° sporgente; nel 2025 l'AdSP valutava manifestazioni di interesse su aree in concessione a Ilva. Da verificare se la concessione è cambiata.
- Eventi con zona 'porto': Zaccaria 2012, Massaro 2019 (non attribuiti a un molo preciso).
