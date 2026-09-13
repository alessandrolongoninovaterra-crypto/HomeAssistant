# Dashboard stile iOS per Home Assistant (Raspberry Pi 3)

## Perché questo approccio
Non ho accesso alla tua istanza Home Assistant reale (nessuna rete/credenziali verso il tuo Raspberry Pi), quindi non posso leggere le tue entità o "collegarmi" alla dashboard attuale. Questo file è un template pronto che riproduce l'estetica iOS (card arrotondate, pulsanti grandi, colori piatti) usando **Mushroom Cards**, la libreria più diffusa per questo stile su HA, scelta apposta perché è leggera e va bene su un Pi 3.

## Installazione
1. Installa **HACS** se non l'hai già: https://hacs.xyz/docs/setup/download
2. In HACS → Frontend installa:
   - `Mushroom`
   - `card-mod`
   - (opzionale, per layout più fluidi) `layout-card`
3. Riavvia Home Assistant.
4. Impostazioni → Dashboard → "+ Aggiungi dashboard" → dai un nome (es. "iOS") → apri i tre puntini → **Modifica in YAML** → incolla il contenuto di `ios-dashboard.yaml`.
5. **Sostituisci tutti gli `entity:` placeholder** (es. `light.soggiorno`, `climate.termostato`, `cover.tapparelle_soggiorno`, `scene.modalita_cinema`, `alarm_control_panel.allarme_casa`, `lock.porta_ingresso`, `media_player.tv_soggiorno`, `weather.casa`, `sensor.temperatura_esterna`) con i tuoi ID reali.
   Li trovi in **Impostazioni → Dispositivi e servizi → Entità** (usa la barra di ricerca).

## Ottimizzazioni per Raspberry Pi 3
Il Pi 3 ha una CPU/GPU modesta, quindi il template evita apposta:
- sfondi sfocati (`backdrop-filter: blur`) — molto costosi da renderizzare;
- troppe card annidate o animazioni CSS complesse;
- grafici storici (`history-graph`/`statistics-graph`) nella vista principale — se ti servono, mettili in una vista separata così non vengono caricati insieme al resto.

Se noti lag nell'interfaccia (tablet a muro, browser sul Pi stesso, ecc.):
- riduci la risoluzione di rendering del browser kiosk (se usi Fully Kiosk Browser o simili);
- disabilita le transizioni card-mod superflue;
- usa meno viste "sections" con card pesanti insieme.

## Se vuoi che aggiusti la dashboard sulle tue entità reali
Puoi incollarmi qui l'export YAML della tua dashboard attuale (Impostazioni → Dashboard → tre puntini → Modifica in YAML → copia tutto), oppure elencarmi le tue entità principali (luci, termostati, tapparelle, sensori, scene), e adatto subito questo template ai tuoi dispositivi reali.
