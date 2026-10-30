import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# bigLust_v10 という文字列を探す
idx = 0
count = 0
while True:
    idx = content.lower().find('biglust_v', idx)
    if idx == -1:
        break
    print(f"idx={idx}: {content[max(0,idx-80):idx+120]}")
    print()
    idx += 1
    count += 1
    if count > 20:
        break

if count == 0:
    print("Not found: bigLust_v")
    # localStorage経由かもしれない → STYLEPRESETSのcheckpointフィールドを全列挙
    import re
    for m in re.finditer(r"checkpoint\s*:\s*['\"]([^'\"]+)['\"]", content):
        v = m.group(1)
        if 'lust' in v.lower() or 'big' in v.lower():
            print(f"checkpoint: {v}")
