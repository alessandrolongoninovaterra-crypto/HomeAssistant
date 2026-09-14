# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Cosa contiene
`ios-dashboard.yaml` è costruita sulle **entità reali** della tua casa (estratte dall'elenco entità che mi hai fornito). Nessun ID da sostituire: è già pronta all'uso.

Due viste, entrambe in stile scuro "glass" (vetro sfumato su sfondo viola):

- **Home** (prima vista, predefinita) — header con orologio + pulsanti "Spegni tutto"/"Telecamere", sezione "Luci" a 3 colonne (Piano Terra / Primo Piano / Esterno, con temperatura e Wi-Fi Blink sotto ciascuna telecamera), poi una riga finale con **Meteo** (card nativa con previsioni prossimi giorni) e **Calendario Famiglia** affiancati.
- **Lista** — stessa disposizione ma tutto impilato in una colonna a griglie 2×N, utile su schermi più stretti o per scorrere rapidamente tutti i dispositivi.

Nota: nella tua casa le luci/prese sono tutte gestite tramite entità **switch** (Sonoff/Matter), non `light` — quindi i pulsanti usano il toggle standard on/off (niente controllo luminosità, perché i dispositivi non lo supportano).

> **Vincolo di design permanente**: la dashboard verrà sempre usata in **orizzontale su tablet**, non in verticale su telefono. La vista "Home" deve stare su un'unica schermata senza scroll verticale — per questo il calendario ha un'altezza massima con scroll interno, e le righe degli interruttori sono compatte. Qualsiasi modifica futura deve rispettare questo vincolo.

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

## Meteo
La card "Meteo" nella vista "Home" ora usa la card nativa `weather-forecast` di Home Assistant (giorno per giorno, senza sensori aggiuntivi da configurare) collegata a `weather.forecast_casa`.

> `template_meteo_snippet.yaml` (la mini tabella 3 giorni × 3 fasce orarie con sensori helper) resta nel repo ma **non è più usato dalla dashboard attuale** — l'abbiamo sostituito con la card nativa più semplice. Se lo hai già installato non serve rimuoverlo (i sensori restano innocui ma inutilizzati); se vuoi tornare alla tabella dettagliata a fasce orarie, dimmelo.

## Calendario di famiglia (per gli appuntamenti)
La card calendario nella vista "Home" ha bisogno di un **calendario reale** collegato a Home Assistant per funzionare — senza, resta vuota/dà errore. Il modo più semplice, senza account esterni, è il calendario locale integrato:

1. Impostazioni → Dispositivi e servizi → "+ Aggiungi integrazione" → cerca **"Local Calendar"**
2. Dagli il nome **"Famiglia"** (importante: usa esattamente questo nome, così l'entità creata sarà `calendar.famiglia`, quella già scritta nel file — se usi un altro nome, dimmelo e aggiorno il file)
3. Fatto: ora nella dashboard puoi cliccare su un giorno del calendario per aggiungere un appuntamento direttamente dal touchscreen, visibile a tutta la famiglia che usa questa dashboard

Se invece preferisci usare un calendario Google già condiviso in famiglia, puoi aggiungere l'integrazione **Google Calendar** invece di Local Calendar — in quel caso l'entity_id sarà diverso (tipo `calendar.nome@gmail.com`): dimmelo e aggiorno `ios-dashboard.yaml`.

## Personalizzazioni future
Se aggiungi nuovi dispositivi o vuoi rinominare/riorganizzare le stanze, incollami il nuovo elenco entità (Impostazioni → Entità → esporta CSV, o Strumenti per sviluppatori → Stati) e aggiorno il file.
