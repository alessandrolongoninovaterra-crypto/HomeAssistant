# Strumenti per i versi degli animali

Registrazioni vere di animali da Wikimedia Commons, con licenza libera, ridotte a clip MP3 brevi a volume uniforme.

- `scelte.json`: la registrazione usata per ognuno dei 12 animali e il tratto da tagliare (`"auto"` = il tratto più forte).
- `candidati*.json`: risultati della ricerca su Commons (titolo, URL, licenza, autore), usati per i crediti.
- `converti_originali.py`: converte i file originali scaricati da Commons in clip MP3.
- `build_crediti.py`: copia le clip in `../versi/` e genera `../versi/crediti.js`.
- `bundle.py`: crea il file unico scaricabile, con fiabe, crediti e audio incorporati.

```
python3 converti_originali.py <cartella_originali> /tmp/mp3 scelte.json
python3 build_crediti.py /tmp/mp3 ../versi scelte.json candidati.json candidati2.json
python3 bundle.py .. Fiabe-della-Buonanotte.html
```
