# Dashboard Casa — approccio nativo (senza HACS)

## Cosa contiene
`dashboard.yaml` usa **solo card native di Home Assistant** (`sections`, `grid`, `heading`, `tile`, `weather-forecast`, `calendar`, `picture-entity`, `markdown`) — niente Mushroom, niente card-mod, niente CSS custom. Nessuna dipendenza da HACS: elimina alla radice i problemi di stile avuti con l'approccio precedente (risorse non caricate, MIME type, stili non applicati).

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
- **Giardino**: temperature Blink Esterno/Finestrone (con grafico trend), stato telecamere (`camera.esterno`, `camera.finestrone`)
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

## Prossimi passi
Modifichiamo la dashboard un pezzo alla volta a partire da questa base — dimmi cosa cambiare.
