"""Scarica i file scelti da Commons e li converte in MP3 brevi e normalizzati.
uso: fetch_convert.py <scelte.json> <candidati.json>... --raw DIR --out DIR"""
import json, subprocess, sys, time, urllib.request, urllib.error, os

UA = "FiabeBuonanotte/1.0 (personal non-commercial project)"
args = sys.argv[1:]
raw = args[args.index("--raw") + 1]
out = args[args.index("--out") + 1]
files = [a for a in args if not a.startswith("--") and a not in (raw, out)]
scelte = json.load(open(files[0]))
index = {}
for f in files[1:]:
    for cands in json.load(open(f)).values():
        for c in cands:
            index[c["title"]] = c
os.makedirs(raw, exist_ok=True)
os.makedirs(out, exist_ok=True)
credits = {}

for key, spec in scelte.items():
    title, start, dur = spec["title"], spec.get("start", 0), spec.get("dur", 5)
    c = index.get(title)
    if not c:
        print("MANCA", key, title, flush=True); continue
    ext = os.path.splitext(c["url"])[1]
    src = os.path.join(raw, key + ext)
    if not os.path.exists(src):
        for attempt in range(4):
            try:
                req = urllib.request.Request(c["url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r, open(src, "wb") as fh:
                    fh.write(r.read())
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  {key}: limite di Wikimedia, mi fermo e riprovo al prossimo controllo", flush=True)
                    sys.exit(3)
                print(f"  {key}: errore HTTP {e.code}", flush=True); break
        time.sleep(1.5)
    if not os.path.exists(src):
        print(f"{key:10} download non riuscito, riprovo al prossimo giro", flush=True)
        continue
    dst = os.path.join(out, key + ".mp3")
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        credits[key] = {"title": title, "license": c["license"], "artist": c["artist"], "page": c["page"]}
        print(f"{key:10} gia' pronto", flush=True)
        continue
    if start == "auto":
        import array
        pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "8000",
                              "-f", "s16le", "-"], capture_output=True, check=True).stdout
        a = array.array("h"); a.frombytes(pcm)
        step = 800  # 0.1 s
        e = [sum(x * x for x in a[i:i + step]) for i in range(0, len(a), step)]
        win = int(dur * 10)
        best, best_i = -1, 0
        for i in range(0, max(1, len(e) - win)):
            s = sum(e[i:i + win])
            if s > best: best, best_i = s, i
        start = max(0, best_i / 10 - 0.2)
    dst = os.path.join(out, key + ".mp3")
    fade_start = max(0.1, dur - 0.6)
    af = (f"atrim=start={start}:duration={dur},asetpts=PTS-STARTPTS,"
          f"silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
          f"afade=t=in:d=0.04,afade=t=out:st={fade_start}:d=0.6,"
          f"loudnorm=I=-18:TP=-2:LRA=11")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af,
                    "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "80k", dst], check=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                       capture_output=True, text=True).stdout.strip()
    credits[key] = {"title": title, "license": c["license"], "artist": c["artist"], "page": c["page"]}
    json.dump(credits, open(os.path.join(out, "_crediti.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{key:10} {float(d):4.1f}s {os.path.getsize(dst)//1024:4d}KB  {c['license']}", flush=True)

json.dump(credits, open(os.path.join(out, "_crediti.json"), "w"), ensure_ascii=False, indent=1)
