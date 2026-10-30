import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

V70 = "moodyKrea2MixUncensoredWeekend_v70"
V80 = "moodyKrea2MixUncensoredV8SEGoes_v80_int8"

with open(r"C:\AI\ComfyUI\dashboard.html", encoding='utf-8', errors='replace') as f:
    content = f.read()

# V70の残存確認
v70_count = content.count(V70)
print(f"V70 残存: {v70_count} 件")

# V80の参照確認
v80_matches = []
idx = 0
while True:
    i = content.find(V80, idx)
    if i == -1: break
    ctx = content[max(0,i-50):i+len(V80)+50]
    v80_matches.append(ctx)
    idx = i + 1

print(f"V80 参照: {len(v80_matches)} 件")
for m in v80_matches:
    print(f"  {m!r}")

# moody_krea2_premiumのSTYLE_PRESET確認
m = re.search(r'moody_krea2_premium[^}]{0,500}', content)
if m:
    print(f"\nmoody_krea2_premium preset:\n{m.group(0)[:400]}")
