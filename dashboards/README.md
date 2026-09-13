# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Cosa contiene
`ios-dashboard.yaml` è costruita sulle **entità reali** della tua casa (estratte dall'elenco entità che mi hai fornito). Nessun ID da sostituire: è già pronta all'uso.

Struttura:
- **Home** — tutte le stanze principali (Salotto, Cucina, Sala, Camere, Roddi, Studio) come pulsanti grandi on/off, più un pulsante "Spegni Tutto"
- **Giardino** — temperature Blink (Esterno/Finestrone) e toggle rilevamento movimento telecamere
- **Sistema** — aggiornamenti disponibili (HA Core/OS/Supervisor, HACS, Mushroom, firmware Matter), lista della spesa, info sole

Nota: nella tua casa le luci/prese sono tutte gestite tramite entità **switch** (Sonoff/Matter), non `light` — quindi i pulsanti usano il toggle standard on/off (niente controllo luminosità, perché i dispositivi non lo supportano).

## Installazione
1. Installa **HACS** se non l'hai già: https://hacs.xyz/docs/setup/download
2. In HACS → Frontend installa:
   - `Mushroom`
   - `card-mod`
3. Riavvia Home Assistant.
4. Impostazioni → Dashboard → "+ Aggiungi dashboard" → dai un nome (es. "iOS") → apri i tre puntini → **Modifica in YAML** → incolla **tutto** il contenuto di `ios-dashboard.yaml` così com'è (il file non contiene commenti, non serve modificare nulla prima di incollare).
5. Salva. Fatto — è già collegata ai tuoi dispositivi.

> Se l'editor YAML di HA dà un errore tipo "duplicated mapping key" o simili, quasi sempre è dovuto a un copia-incolla parziale o a un'indentazione alterata: riapri `ios-dashboard.yaml`, seleziona tutto (Ctrl+A) e ricopialo integralmente, senza aggiungere o togliere righe a mano.

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
