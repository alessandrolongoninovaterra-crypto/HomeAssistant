# Dashboard Casa — approccio nativo (senza HACS)

> ## ⚠️ Vincolo hardware: niente card telecamera
> L'impianto gira su un **Raspberry Pi 3 (1 GB di RAM)**. Le card che mostrano
> immagini o video da una telecamera (`picture-entity` con `camera_image`,
> `picture-glance`, o una `tile` puntata su un'entità `camera.*`) avviano lo
> streaming tramite **ffmpeg**: su questo hardware saturano la memoria, il
> kernel termina Home Assistant Core, che riparte e ricarica la dashboard —
> **crash loop infinito**, con Home Assistant che si connette e cade dopo pochi
> secondi. È già successo una volta e ha reso il sistema inutilizzabile finché
> la dashboard non è stata rimossa.
>
> Per lo stato delle telecamere Blink usare **solo** le entità leggere:
> gli `switch.*_rilevamento_del_movimento_*` e i `sensor.*_temperatura`.
> Questo vincolo decade solo migrando su hardware più potente.

## Cosa contiene
`dashboard.yaml` usa **solo card native di Home Assistant** (`sections`, `grid`, `heading`, `tile`, `weather-forecast`, `calendar`, `markdown`) — niente Mushroom, niente card-mod, niente CSS custom. Nessuna dipendenza da HACS: elimina alla radice i problemi di stile avuti con l'approccio precedente (risorse non caricate, MIME type, stili non applicati).

Lo stile "iPhone/iPad" (sfondo grigio chiaro, card bianche con angoli molto arrotondati, ombra morbida, blu di sistema iOS, verde per gli interruttori accesi) è ottenuto con un **tema nativo di Home Assistant** (`themes/ios_style.yaml`) — anche questa è una funzione core, non richiede HACS né JavaScript esterno.

### Attivare il tema "iOS Style"
1. Copia `themes/ios_style.yaml` sul Raspberry Pi dentro `/config/themes/ios_style.yaml` (crea la cartella `themes` se non esiste, con l'add-on File editor o Samba).
2. Apri `configuration.yaml` e assicurati che contenga:
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```
   (se hai già una sezione `frontend:` con altre opzioni, aggiungi solo la riga `themes: !include_dir_merge_named themes` sotto).
3. Riavvia Home Assistant.
4. Non serve selezionare il tema nel tuo profilo utente: la vista "DashBoard" lo applica automaticamente tramite `theme: iOS Style` nel file `dashboard.yaml`, indipendentemente dal tema che usi altrove.

Una vista, "DashBoard":
- Header con saluto ("Ciao {{ user }}")
- **Piano Terra**: Salotto, Presa Salotto, Cucina, Pranzo 2 (interruttori con toggle)
- **Primo piano**: Rodolfo, Studio, Matrimoniale 2 (interruttori con toggle)
- **Giardino**: temperature Blink Esterno/Finestrone (con grafico trend) e interruttori di rilevamento movimento delle due telecamere (vedi avvertenza sopra: nessuna card con immagini dalle telecamere)
- **Meteo**: card nativa `weather-forecast` su `weather.forecast_casa`, 6 giorni di previsioni
- **Calendario**: card nativa su `calendar.famiglia`

> Nota: questa è la base fornita dall'utente. La struttura interruttori è diversa da quella della versione precedente (meno entità elencate) — verrà ampliata/corretta passo passo.

## Installazione
1. Impostazioni → Dashboard → "+ Aggiungi dashboard" → dai un nome → tre puntini → **Modifica in YAML** → incolla il contenuto di `dashboard.yaml`.
2. Salva.

Non serve installare nulla da HACS: tutte le card usate sono incluse di serie in Home Assistant.

## Calendario di famiglia
Serve un'entità `calendar.famiglia` reale. Se non l'hai già creata:
1. Impostazioni → Dispositivi e servizi → "+ Aggiungi integrazione" → cerca **"Local Calendar"**
2. Nome esatto: **Famiglia**

## Reinstallazione da zero sul Raspberry Pi 3

Ordine delle operazioni pensato per non ricadere nel crash loop. **Il punto 4 è
quello critico**: va fatto *prima* di aprire qualsiasi dashboard, altrimenti la
"Panoramica" generata automaticamente include da sola le telecamere.

1. Scrivi Home Assistant OS su una **scheda SD nuova** con Raspberry Pi Imager
   (lascia attiva la verifica dopo la scrittura).
2. Primo avvio, completa la procedura iniziale (utente, posizione).
3. Aggiungi le integrazioni: Sonoff/Matter, Meteo, **Local Calendar** (nome
   esatto: `Famiglia`), e per ultima **Blink**.
4. **Subito dopo Blink, prima di aprire qualsiasi dashboard**:
   Impostazioni → Dispositivi e servizi → Blink → Entità → seleziona
   `camera.esterno` e `camera.finestrone` → **Disabilita**.
   Restano attivi i sensori di temperatura e gli interruttori di movimento,
   che sono leggeri e sono quelli usati dalla dashboard.
5. Aggiungi in fondo a `configuration.yaml` il contenuto di
   `configuration_snippet.yaml` (configurazione `recorder` ottimizzata per il
   Pi 3: riduce molto le scritture sulla SD) e riavvia.
6. Crea la dashboard incollando `dashboard.yaml`.
7. Imposta i **backup automatici** (Impostazioni → Sistema → Backup) e falli
   salvare fuori dal Pi.

### La scheda SD è ancora buona?
Il modo più semplice per scoprirlo senza comprare nulla: **riscrivi l'immagine
sulla scheda attuale con Raspberry Pi Imager**, lasciando attiva la verifica.
Se la verifica fallisce, la scheda è da buttare. Se passa e il sistema si avvia
normalmente, la scheda regge e il problema era solo corruzione del filesystem
causata dai riavvii bruschi.

## Prossimi passi
Modifichiamo la dashboard un pezzo alla volta a partire da questa base — dimmi cosa cambiare.
