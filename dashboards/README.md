# Dashboard Casa — approccio nativo (senza HACS)

## Cosa contiene
`dashboard.yaml` usa **solo card native di Home Assistant** (`sections`, `grid`, `heading`, `tile`, `weather-forecast`, `calendar`, `picture-entity`, `markdown`) — niente Mushroom, niente card-mod, niente CSS custom. Nessuna dipendenza da HACS: elimina alla radice i problemi di stile avuti con l'approccio precedente (risorse non caricate, MIME type, stili non applicati).

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
