"""Crea un unico file HTML autonomo: storie, crediti e MP3 incorporati."""
import base64, glob, os, sys

app_dir, out = sys.argv[1], sys.argv[2]
page = open(os.path.join(app_dir, "index.html"), encoding="utf-8").read()
storie = open(os.path.join(app_dir, "storie.js"), encoding="utf-8").read()
crediti = open(os.path.join(app_dir, "versi", "crediti.js"), encoding="utf-8").read()

data = {}
for mp3 in sorted(glob.glob(os.path.join(app_dir, "versi", "*.mp3"))):
    key = os.path.splitext(os.path.basename(mp3))[0]
    data[key] = base64.b64encode(open(mp3, "rb").read()).decode()
data_js = "window.VERSI_DATA = {" + ",".join(f'"{k}":"{v}"' for k, v in data.items()) + "};"

page = page.replace('<script src="storie.js"></script>', "<script>\n" + storie + "\n</script>")
page = page.replace('<script src="versi/crediti.js"></script>', "<script>\n" + crediti + "\n" + data_js + "\n</script>")
assert 'src="storie.js"' not in page and 'src="versi/crediti.js"' not in page

doc = ('<!doctype html><html lang="it"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
       '</head><body>\n' + page + '\n</body></html>\n')
open(out, "w", encoding="utf-8").write(doc)
print(out, os.path.getsize(out) // 1024, "KB,", len(data), "registrazioni incorporate")
