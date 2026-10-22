# Strumenti per i versi degli animali

Registrazioni prese da Wikimedia Commons con licenza libera e convertite in clip MP3 brevi.

- `candidati*.json`: risultati della ricerca su Commons (titolo, URL, licenza, autore).
- `scelte_tutte.json`: la registrazione scelta per ogni animale e il tratto da usare.
- `fetch_convert.py`: scarica e converte le clip mancanti (si ferma al primo limite di Wikimedia).
- `build_crediti.py`: copia le clip in `../versi/` e genera `../versi/crediti.js`.
- `bundle.py`: crea il file unico scaricabile con storie, crediti e audio incorporati.

```
python3 fetch_convert.py scelte_tutte.json candidati.json candidati2.json --raw /tmp/raw --out /tmp/mp3
python3 build_crediti.py /tmp/mp3 ../versi scelte_tutte.json candidati.json candidati2.json
python3 bundle.py .. Fiabe-della-Buonanotte.html
```
