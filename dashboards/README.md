# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Cosa contiene
`ios-dashboard.yaml` è costruita sulle **entità reali** della tua casa (estratte dall'elenco entità che mi hai fornito). Nessun ID da sostituire: è già pronta all'uso.

Due viste:

- **Home** (prima vista, predefinita) — dashboard scura in stile "glass" (vetro sfumato su sfondo viola/blu), su un'unica schermata orizzontale senza scroll: barra in alto (orologio, "Spegni Tutto", "Telecamere"), poi una riga con a sinistra **4 colonne compatte** (Piano Terra / Primo Piano / Giardino / Meteo — quest'ultima una mini tabella 3 giorni × 3 fasce orarie, vedi sezione dedicata sotto) e a destra un **calendario di famiglia** (vedi sezione dedicata sotto per configurarlo). Vedi `riferimento-stile-glass.md` per i dettagli dell'adattamento dallo screenshot originale.
- **Lista** — la stessa disposizione degli interruttori ma a righe compatte (Esterno / Piano Terra / Primo Piano affiancati), utile per vedere anche il segnale Wi-Fi dei sensori Blink oltre alla temperatura.

Nota: nella tua casa le luci/prese sono tutte gestite tramite entità **switch** (Sonoff/Matter), non `light` — quindi i pulsanti usano il toggle standard on/off (niente controllo luminosità, perché i dispositivi non lo supportano).

## Installazione

### Metodo A — incolla nell'editor UI (più semplice, ma può dare errori di indentazione)
1. Installa **HACS** se non l'hai già: https://hacs.xyz/docs/setup/download
2. In HACS → Frontend installa:
   - `Mushroom`
   - `card-mod`
3. Riavvia Home Assistant.
4. Impostazioni → Dashboard → "+ Aggiungi dashboard" → dai un nome (es. "iOS") → apri i tre puntini → **Modifica in YAML** → incolla **tutto** il contenuto di `ios-dashboard.yaml` così com'è.
5. Salva.

> **Se l'editor dà errori tipo "bad indentation" o "duplicated mapping key"**: non è il file, è un bug noto dell'editor Lovelace che a volte auto-indenta il testo incollato aggiungendo spazi extra riga per riga. In quel caso passa al Metodo B.

### Metodo B — dashboard da file (affidabile al 100%, consigliato)
Bypassa del tutto l'editor UI caricando il file YAML direttamente dal filesystem del Pi:

1. Installa gli stessi componenti HACS del Metodo A (Mushroom, card-mod) e riavvia.
2. Copia `ios-dashboard.yaml` sul Raspberry Pi dentro `/config/dashboards/ios-dashboard.yaml`. Per farlo puoi usare:
   - l'add-on **File editor** o **Studio Code Server** (Impostazioni → Add-on → Negozio di componenti aggiuntivi)
   - oppure l'add-on **Samba share** per copiare il file da PC via rete
3. Apri `configuration.yaml` (con lo stesso add-on) e aggiungi in fondo il contenuto di `configuration_snippet.yaml` (incluso in questa cartella, opzionale — serve solo per questo metodo).
4. Riavvia Home Assistant (Impostazioni → Sistema → Riavvia). La dashboard "iOS" comparirà nel menu laterale.

Con questo metodo il file viene letto così com'è, senza passare da nessun editor di testo che possa alterarne l'indentazione — se in futuro modifico il file, ti basta ricopiarlo su `/config/dashboards/ios-dashboard.yaml` e riavviare.

## Ottimizzazioni per Raspberry Pi 3
Il Pi 3 ha una CPU/GPU modesta, quindi il template evita apposta:
- sfondi sfocati (`backdrop-filter: blur`) — molto costosi da renderizzare;
- troppe card annidate o animazioni CSS complesse;
- grafici storici nella vista principale.

Se noti lag nell'interfaccia (tablet a muro, browser sul Pi stesso, ecc.):
- riduci la risoluzione di rendering del browser kiosk (se usi Fully Kiosk Browser o simili);
- usa meno viste "sections" con card pesanti insieme.

## Fonte meteo
Le card meteo usano l'entità `weather.forecast_casa`, attualmente fornita dall'integrazione **Met.no** (già configurata). Non esiste un'integrazione Home Assistant per **3bMeteo**: è un sito commerciale senza API pubblica, e fare scraping sarebbe fragile (si rompe a ogni modifica del sito) — quindi non l'ho implementato.

**Per passare a MeteoAM** (Aeronautica Militare, fonte più "italiana"):
1. HACS → tre puntini in alto a destra → **"Repository personalizzati"** → aggiungi `https://github.com/sibest19/hass-meteoam` come categoria **Integrazione**
2. Cerca "MeteoAM" in HACS → installa → riavvia Home Assistant
3. Impostazioni → Dispositivi e servizi → "+ Aggiungi integrazione" → cerca "MeteoAM" → segui la configurazione
4. Vai su Impostazioni → Entità, cerca "meteo" e trovi la nuova entità (es. `weather.meteoam`) — **dimmi l'entity_id esatto** e aggiorno `ios-dashboard.yaml` e `template_meteo_snippet.yaml` sostituendo `weather.forecast_casa` ovunque compare

## Meteo: mini tabella 3 giorni × 3 fasce orarie
Nella vista "Home", la colonna "Meteo" (accanto a Piano Terra / Primo Piano / Giardino) mostra una mini tabella con i **giorni in colonna** (O = Oggi, D = Domani, Dp = Dopodomani) e le **fasce orarie in riga** (M = Mattina ~9:00, P = Pranzo ~13:00, S = Sera ~20:00) — 9 celle in tutto, compresse per stare nella stessa larghezza delle altre colonne. Serve la previsione ORARIA, che le card Lovelace standard non possono filtrare da sole — serve un piccolo sensore helper:

1. Apri `configuration.yaml` (con File editor o Studio Code Server) e aggiungi in fondo il contenuto di `template_meteo_snippet.yaml` (incluso in questa cartella)
2. Riavvia Home Assistant
3. Verifica che siano comparse 9 nuove entità (Impostazioni → Entità, cerca "Meteo"): `sensor.meteo_oggi_mattina`, `..._oggi_pranzo`, `..._oggi_sera`, `..._domani_mattina`, `..._domani_pranzo`, `..._domani_sera`, `..._dopodomani_mattina`, `..._dopodomani_pranzo`, `..._dopodomani_sera`

> Nota: le fasce di "Domani"/"Dopodomani" dipendono da quanto in avanti arriva la previsione oraria della tua fonte meteo (Met.no ne copre solitamente a sufficienza; verifica dopo l'installazione che le celle non restino vuote/"unknown" per i giorni più lontani).

## Calendario di famiglia (per gli appuntamenti)
La card calendario nella vista "Home" ha bisogno di un **calendario reale** collegato a Home Assistant per funzionare — senza, resta vuota/dà errore. Il modo più semplice, senza account esterni, è il calendario locale integrato:

1. Impostazioni → Dispositivi e servizi → "+ Aggiungi integrazione" → cerca **"Local Calendar"**
2. Dagli il nome **"Famiglia"** (importante: usa esattamente questo nome, così l'entità creata sarà `calendar.famiglia`, quella già scritta nel file — se usi un altro nome, dimmelo e aggiorno il file)
3. Fatto: ora nella dashboard puoi cliccare su un giorno del calendario per aggiungere un appuntamento direttamente dal touchscreen, visibile a tutta la famiglia che usa questa dashboard

Se invece preferisci usare un calendario Google già condiviso in famiglia, puoi aggiungere l'integrazione **Google Calendar** invece di Local Calendar — in quel caso l'entity_id sarà diverso (tipo `calendar.nome@gmail.com`): dimmelo e aggiorno `ios-dashboard.yaml`.

## Personalizzazioni future
Se aggiungi nuovi dispositivi o vuoi rinominare/riorganizzare le stanze, incollami il nuovo elenco entità (Impostazioni → Entità → esporta CSV, o Strumenti per sviluppatori → Stati) e aggiorno il file.
