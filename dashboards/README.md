# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Cosa contiene
`ios-dashboard.yaml` è costruita sulle **entità reali** della tua casa (estratte dall'elenco entità che mi hai fornito). Nessun ID da sostituire: è già pronta all'uso.

Struttura: **una sola pagina** (vista `panel`, pensata per stare tutta a schermo in orizzontale su un display collegato al Pi), divisa in 3 colonne affiancate:
- **Esterno** — telecamere Blink (toggle rilevamento movimento, singolo e "tutte insieme") con temperatura e segnale Wi-Fi di ciascuna
- **Piano Terra** — Cucina, Salotto (+ presa), Pranzo (+ presa aggiuntiva)
- **Primo Piano** — Matrimoniale (+ armadio), Rodolfo, Studio

In alto: meteo e pulsante "Spegni Tutto".

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
3. Apri `configuration.yaml` (con lo stesso add-on) e aggiungi in fondo il contenuto di `configuration_snippet.yaml` (incluso in questa cartella).
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

## Personalizzazioni future
Se aggiungi nuovi dispositivi o vuoi rinominare/riorganizzare le stanze, incollami il nuovo elenco entità (Impostazioni → Entità → esporta CSV, o Strumenti per sviluppatori → Stati) e aggiorno il file.
