"""Copia gli MP3 pronti in fiabe/versi/ e genera versi/crediti.js dai metadati di Commons."""
import html, json, os, re, shutil, sys

src_dir, dst_dir, scelte_f = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst_dir, exist_ok=True)
index = {}
for f in sys.argv[4:]:
    for cs in json.load(open(f)).values():
        for c in cs:
            index[c["title"]] = c
cred = {}
for key, spec in json.load(open(scelte_f)).items():
    c = index[spec["title"]]
    cred[key] = {"title": c["title"], "license": c["license"], "artist": c["artist"], "page": c["page"]}

def plain(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()[:120]

out = {}
for key, c in sorted(cred.items()):
    mp3 = os.path.join(src_dir, key + ".mp3")
    if not os.path.exists(mp3):
        continue
    shutil.copyfile(mp3, os.path.join(dst_dir, key + ".mp3"))
    titolo = re.sub(r"^File:", "", c["title"])
    titolo = re.sub(r"\.(ogg|oga|opus|wav|flac|mp3)$", "", titolo, flags=re.I)
    out[key] = {"titolo": titolo, "autore": plain(c.get("artist")), "licenza": c.get("license") or "licenza libera", "page": c["page"]}

with open(os.path.join(dst_dir, "crediti.js"), "w") as fh:
    fh.write("window.VERSI_REC = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n")
print(len(out), "registrazioni:", ", ".join(out))
