# Dashboard Casa — approccio nativo (senza HACS)

> ## ⚠️ Blink escluso per il momento
> **Nessuna entità Blink è presente in questa dashboard**, e l'integrazione
> Blink non va aggiunta per ora: né telecamere, né sensori di temperatura, né
> interruttori di rilevamento movimento.
>
> Motivo: l'impianto gira su un **Raspberry Pi 3 (1 GB di RAM)**. Le card che
> mostrano immagini o video da una telecamera (`picture-entity` con
> `camera_image`, `picture-glance`, o una `tile` puntata su un'entità
> `camera.*`) avviano lo streaming tramite **ffmpeg**: su questo hardware
> saturano la memoria, il kernel termina Home Assistant Core, che riparte e
> ricarica la dashboard — **crash loop infinito**. È già successo e ha reso il
> sistema inutilizzabile finché la dashboard non è stata rimossa.
>
> Quando in futuro si vorrà rimettere Blink: aggiungere l'integrazione,
> **disabilitare subito le entità `camera.*`** prima di aprire qualsiasi
> dashboard, e usare solo le entità leggere
> (`switch.*_rilevamento_del_movimento_*` e `sensor.*_temperatura`).

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

Tempo totale: circa un'ora, di cui buona parte di attesa. L'ordine delle
operazioni è pensato per non ricadere nel crash loop: **la fase 4 è quella
critica**.

### Fase 1 — Scrivere il sistema sulla SD (10 min)
1. Sul PC installa **Raspberry Pi Imager** (raspberrypi.com/software).
2. Spegni il Pi, estrai la SD, mettila nel lettore del PC.
3. In Imager: **Scegli dispositivo** → Raspberry Pi 3.
4. **Scegli sistema operativo** → *Other specific-purpose OS* → *Home
   assistants and home automation* → *Home Assistant* → **Home Assistant OS
   (RPi 3 64-bit)**.
5. **Scegli scheda SD** → la tua → Scrivi.
6. Lascia che completi la **verifica** a fine scrittura. Se la verifica
   fallisce, la scheda è da buttare: comprane una nuova (meglio se "High
   Endurance") e ripeti.

### Fase 2 — Primo avvio (15-25 min di attesa)
1. Rimetti la SD nel Pi, collega il cavo di rete e alimenta.
2. **Aspetta senza fare nulla.** Il primo avvio su Pi 3 è lento: scarica e
   installa il Supervisor. Possono volerci anche 25 minuti.
3. Dal PC apri `http://homeassistant.local:8123`. Se non risponde, aspetta
   ancora qualche minuto o cerca l'IP nel pannello del router.
4. Completa la procedura iniziale: nome utente, password, posizione.

### Fase 3 — Blindare la dashboard predefinita (2 min)
Da fare **prima** di aggiungere Blink. La "Panoramica" predefinita si genera da
sola includendo *tutte* le entità: se resta in modalità automatica, appena
aggiungi le telecamere se le ritrova dentro e il Pi va di nuovo in crisi.

1. Apri la Panoramica → matita in alto a destra → compare l'avviso che la
   dashboard è generata automaticamente → **"Prendi il controllo"**.
2. Da quel momento è statica e non aggiunge più nulla da sola.

### Fase 4 — Integrazioni (Blink esclusa)
Aggiungi (Impostazioni → Dispositivi e servizi → Aggiungi):
1. Gli interruttori **Sonoff / Matter**
2. Il **meteo** (Met.no)
3. **Local Calendar**, con nome esatto `Famiglia`

**Non aggiungere Blink** — vedi l'avvertenza in cima a questo file. Per ora
l'impianto resta senza telecamere, così il Pi 3 lavora tranquillo e si può
verificare che tutto sia stabile prima di aggiungere altro.

### Fase 5 — Ottimizzazione recorder (opzionale, consigliata)
Riduce molto le scritture sulla SD e quindi la sua usura.
1. Installa l'add-on **File editor**, aprilo.
2. Apri `configuration.yaml`, incolla in fondo il contenuto di
   `configuration_snippet.yaml`, salva.
3. Riavvia Home Assistant.
4. **Ferma l'add-on File editor** quando hai finito: su 1 GB di RAM ogni
   add-on attivo pesa.

### Fase 6 — Dashboard
Impostazioni → Dashboard → "+ Aggiungi dashboard" → tre puntini → **Modifica in
YAML** → incolla `dashboard.yaml` → Salva.

> ⚠️ **Verifica gli entity_id.** Riconfigurando le integrazioni da zero, gli
> identificativi delle entità possono cambiare (es. `switch.salotto_sonoff_..._1`
> potrebbe diventare `..._2`). Se qualche card appare come "Entità non
> disponibile", controlla in Impostazioni → Entità il nome esatto e aggiorna il
> file.

### Fase 7 — Backup automatici (5 min, il passaggio più importante)
Impostazioni → Sistema → Backup → configura un backup automatico e falli
salvare **fuori dal Pi** (Google Drive, Samba, chiavetta USB).

È l'unica cosa che rende irrilevante qualsiasi guasto futuro: si ripristina
tutto su qualunque macchina in mezz'ora.

## Prossimi passi
Modifichiamo la dashboard un pezzo alla volta a partire da questa base — dimmi cosa cambiare.
