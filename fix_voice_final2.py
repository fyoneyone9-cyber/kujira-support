import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

ai_block_start = None
keyword_block_start = None
yoneyama_block_start = None

for i, l in enumerate(lines):
    if '{/* AI\u5207\u308a\u8fd4\u3057 */' in l and ai_block_start is None:
        ai_block_start = i
    if '\u30ad\u30fc\u30ef\u30fc\u30c9\u3067\u5207\u308a\u8fd4\u3057' in l and keyword_block_start is None:
        keyword_block_start = i - 2
    if '{/* \u7c73\u5c71\u30d1\u30bf\u30fc\u30f3' in l and yoneyama_block_start is None:
        yoneyama_block_start = i

print(f"AI: {ai_block_start+1}, Keyword: {keyword_block_start+1 if keyword_block_start else None}, Yoneyama: {yoneyama_block_start+1 if yoneyama_block_start else None}")
if yoneyama_block_start:
    print("Yoneyama line:", lines[yoneyama_block_start][:80])
