import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S4 tifaの定義を確認
m4 = re.search(r'id:\s*[\'"]char_kaizo_nichijou4_tifa[\'"][^\}]{0,600}', content)
if m4:
    print("=== S4 tifa ===")
    print(m4.group()[:400])

print()
# S5 tifaの定義を確認
m5 = re.search(r'id:\s*[\'"]char_kaizo_nichijou5_tifa[\'"][^\}]{0,600}', content)
if m5:
    print("=== S5 tifa ===")
    print(m5.group()[:400])
