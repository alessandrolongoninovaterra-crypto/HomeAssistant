# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Cosa contiene
`ios-dashboard.yaml` è costruita sulle **entità reali** della tua casa (estratte dall'elenco entità che mi hai fornito). Nessun ID da sostituire: è già pronta all'uso.

Tre viste:

- **Home** (prima vista, predefinita) — dashboard scura in stile "glass" (vetro sfumato su sfondo viola/blu), su un'unica schermata orizzontale senza scroll: barra in alto (orologio, meteo **Oggi/Domani/Dopodomani**, "Spegni Tutto", "Telecamere"), poi una riga con a sinistra le 3 colonne compatte di interruttori (Piano Terra / Primo Piano / Giardino, con temperatura e Wi-Fi Blink accanto al rispettivo interruttore) e a destra un **calendario di famiglia** (vedi sezione dedicata sotto per configurarlo). Vedi `riferimento-stile-glass.md` per i dettagli dell'adattamento dallo screenshot originale.

- **Casa** — piantina stilizzata di una casetta con giardino, con le icone dei dispositivi posizionate sopra il disegno nella stanza corrispondente: tocca un'icona per accendere/spegnere. In alto: meteo, toggle "Telecamere" (accende/spegne insieme i due rilevamenti movimento Blink) e "Spegni Tutto"; ai lati del giardino le due telecamere Blink con relativa temperatura. Il disegno è incorporato direttamente nel file YAML (nessun file immagine separato da caricare).
- **Lista** — la stessa disposizione ma a righe compatte (Esterno / Piano Terra / Primo Piano affiancati), utile se su schermi piccoli le icone sulla piantina sono difficili da toccare con precisione, o per vedere anche il segnale Wi-Fi dei sensori Blink.

Mappatura stanze basata sulla tua planimetria reale, comprese le proporzioni: il Primo Piano è più stretto e non copre il garage, il garage è arretrato/più in basso rispetto al corpo principale, il giardino avvolge la casa con il vialetto ciottolato sul lato del garage:
- **Primo Piano**: Matrimoniale (+ Matrimoniale 2 + Armadio) camera sinistra, Rodolfo camera destra, Studio nella fascia centrale accanto al bagno
- **Piano Terra**: Soggiorno/Salotto (+ Presa Salotto), Pranzo (+ Pranzo 2 + Presa) al centro, Cucina a destra, Garage arretrato sulla destra
- **Giardino**: telecamere Blink Esterno (lato giardino) e Finestrone (lato vialetto/garage) con temperatura

Non incluso: il Piano Seminterrato della planimetria (camino, lavanderia, ripostiglio) perché nessuna delle tue entità attuali vi corrisponde. Se in futuro aggiungi dispositivi lì, dimmelo e lo aggiungo.

Nota: nella tua casa le luci/prese sono tutte gestite tramite entità **switch** (Sonoff/Matter), non `light` — quindi i pulsanti usano il toggle standard on/off (niente controllo luminosità, perché i dispositivi non lo supportano).

## Installazione

### Metodo A — incolla nell'editor UI (più semplice, ma può dare errori di indentazione)
1. Installa **HACS** se non l'hai già: https://hacs.xyz/docs/setup/download
2. In HACS → Frontend installa:
   - `Mushroom`
   - `card-mod`
3. Riavvia Home Assistant.
4. Impostazioni → Dashboard → "+ Aggiungi dashboard" → dai un nome (es. "iOS") → apri i tre puntini → **Modifica in YAML** → incolla **tutto** il contenuto di `ios-dashboard.yaml` così com'è. Non serve nessun altro file: il disegno della piantina è incorporato nel YAML stesso.
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
Le card meteo usano l'entità `weather.forecast_casa`, attualmente fornita dall'integrazione **Met.no** (già configurata). Non esiste un'integrazione Home Assistant per **3bMeteo**: è un sito commerciale senza API pubblica, e fare scraping sarebbe fragile (si rompe a ogni modifica del sito) — quindi non l'ho implementato. Se vuoi una fonte più "italiana", l'alternativa più vicina è **MeteoAM** (Aeronautica Militare), disponibile come integrazione di terze parti via HACS: dimmelo se la vuoi installare e aggiorno il file con la nuova entità.

## Calendario di famiglia (per gli appuntamenti)
La card calendario nella vista "Home" ha bisogno di un **calendario reale** collegato a Home Assistant per funzionare — senza, resta vuota/dà errore. Il modo più semplice, senza account esterni, è il calendario locale integrato:

1. Impostazioni → Dispositivi e servizi → "+ Aggiungi integrazione" → cerca **"Local Calendar"**
2. Dagli il nome **"Famiglia"** (importante: usa esattamente questo nome, così l'entità creata sarà `calendar.famiglia`, quella già scritta nel file — se usi un altro nome, dimmelo e aggiorno il file)
3. Fatto: ora nella dashboard puoi cliccare su un giorno del calendario per aggiungere un appuntamento direttamente dal touchscreen, visibile a tutta la famiglia che usa questa dashboard

Se invece preferisci usare un calendario Google già condiviso in famiglia, puoi aggiungere l'integrazione **Google Calendar** invece di Local Calendar — in quel caso l'entity_id sarà diverso (tipo `calendar.nome@gmail.com`): dimmelo e aggiorno `ios-dashboard.yaml`.

## Personalizzazioni future
Se aggiungi nuovi dispositivi o vuoi rinominare/riorganizzare le stanze, incollami il nuovo elenco entità (Impostazioni → Entità → esporta CSV, o Strumenti per sviluppatori → Stati) e aggiorno il file.
