"""Converte in clip MP3 i file originali caricati a mano in originali/.
Riconosce ogni file dal nome che ha su Wikimedia Commons (spazi o trattini bassi indifferenti).
uso: converti_originali.py <cartella_originali> <cartella_mp3> <scelte.json>"""
import array, json, os, re, subprocess, sys

orig_dir, out_dir, scelte_f = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)

def norm(name):
    name = re.sub(r"^File:", "", name)
    return re.sub(r"[\s_]+", " ", name).strip().lower()

files = {norm(f): os.path.join(orig_dir, f) for f in os.listdir(orig_dir) if not f.lower().endswith(".md")}

def loudest_start(src, dur):
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h"); a.frombytes(pcm)
    e = [sum(x * x for x in a[i:i + 800]) for i in range(0, len(a), 800)]
    win = int(dur * 10)
    best, best_i = -1, 0
    for i in range(0, max(1, len(e) - win)):
        s = sum(e[i:i + win])
        if s > best: best, best_i = s, i
    return max(0, best_i / 10 - 0.2)

for key, spec in json.load(open(scelte_f)).items():
    dst = os.path.join(out_dir, key + ".mp3")
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        continue
    src = files.get(norm(spec["title"]))
    if not src:
        continue
    dur = spec.get("dur", 5)
    start = loudest_start(src, dur) if spec.get("start") == "auto" else spec.get("start", 0)
    af = (f"atrim=start={start}:duration={dur},asetpts=PTS-STARTPTS,"
          f"silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
          f"afade=t=in:d=0.04,afade=t=out:st={max(0.1, dur - 0.6)}:d=0.6,"
          f"loudnorm=I=-18:TP=-2:LRA=11")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af,
                    "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "80k", dst], check=True)
    print(f"{key:10} convertito da {os.path.basename(src)}", flush=True)
