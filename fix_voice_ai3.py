import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
# AIブロックの正確な開始・終了を探す
for i, l in enumerate(lines):
    if 'AI\u5207\u308a\u8fd4\u3057\u30b5\u30b8\u30a7\u30b9\u30c8' in l or ('AI' in l and 'Gemini API' in lines[i+1] if i+1<len(lines) else False):
        print(f"AI section at line {i+1}: {l[:60]}")
    if 'Gemini API' in l:
        print(f"Gemini at line {i+1}: {l[:60]}")
    if '\u30ad\u30fc\u30ef\u30fc\u30c9\u3067\u5207\u308a\u8fd4\u3057' in l:
        print(f"keyword at line {i+1}: {l[:60]}")
