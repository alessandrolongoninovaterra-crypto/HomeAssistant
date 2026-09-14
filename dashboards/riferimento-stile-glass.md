# Riferimento: stile dashboard "glass" scura

Descrizione testuale dello screenshot di riferimento fornito dall'utente (non ho un file immagine salvabile, solo la descrizione — vedi limite spiegato in chat).

## Stile visivo
- Sfondo: gradiente viola/blu scuro (tipo `#2B1A52` → `#5F3FAE`), diagonale
- Card: effetto "vetro" — sfondo bianco semi-trasparente (~8% opacità) + blur, bordo sottile chiaro, angoli molto arrotondati (~20-22px), testo bianco
- Card orologio: unica card a colore pieno (blu/viola acceso), non trasparente, per farla risaltare
- Icone dispositivi: cerchio colorato pieno con icona bianca dentro

## Layout (griglia di card, non un'unica lista)
1. **Riga 1**: orologio grande (ora + data) + 2 gauge circolari (temperatura, umidità) + 3 pulsanti rotondi con icona (luci rapide)
2. **Riga 2**: lista dispositivi con toggle a destra + pallini colorati (selettore colore luce RGB) + blocco pulsanti azione (power/reboot/scena)
3. **Riga 3**: statistiche throughput/rete (download/upload)
4. **Card sistema**: mini dashboard NAS e host Raspberry Pi — CPU%, RAM%, temperatura, spazio disco, uptime, ciascuno con icona
5. **Card immagine**: anteprima da una telecamera
6. **Card meteo**: temperatura attuale grande + condizioni + riga previsioni prossimi giorni con icone

## Adattamento fatto per l'utente
Sull'impianto reale (switch on/off, non luci RGB dimmerabili; nessun NAS; nessuna entità camera con stream, solo switch di rilevamento movimento Blink) ho adattato:
- Selettore colore luce → rimosso (non applicabile a interruttori semplici)
- NAS → sostituito con nota per aggiungere l'integrazione **System Monitor** e monitorare il Raspberry Pi 3 stesso
- Feed telecamera live → sostituito con card Giardino (toggle + temperatura Blink Esterno/Finestrone)
- Gauge umidità → sostituito con gauge segnale Wi-Fi Blink (non c'è un sensore di umidità in casa)

Implementato nella vista **"Home"** (prima vista) di `ios-dashboard.yaml`.
