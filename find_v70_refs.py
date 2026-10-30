import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

V70 = "moodyKrea2MixUncensoredWeekend_v70_fp8"
V80 = "moodyKrea2MixUncensoredV8SEGoes_v80_int8"

files = [
    r"C:\AI\ComfyUI\api_server_3001.py",
    r"C:\AI\ComfyUI\dashboard.html",
]

for fpath in files:
    p = pathlib.Path(fpath)
    if not p.exists():
        print(f"NOT FOUND: {fpath}")
        continue
    with open(p, encoding='utf-8', errors='replace') as f:
        content = f.read()
    count = content.count(V70)
    print(f"{p.name}: {count} occurrences of v70")
    if count > 0:
        # 前後20文字のコンテキスト
        idx = 0
        shown = 0
        while True:
            idx = content.find(V70, idx)
            if idx == -1: break
            shown += 1
            if shown <= 5:
                print(f"  [{idx}]: ...{content[max(0,idx-30):idx+len(V70)+30]!r}...")
            idx += 1
        if shown > 5:
            print(f"  ... {shown-5} more occurrences")
