import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S0255の定義（outfitのラベル・プロンプトを含む箇所）
pos = 33677100
chunk = content[pos:pos+3000]
print(chunk)
