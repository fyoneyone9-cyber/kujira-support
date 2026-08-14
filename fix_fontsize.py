import subprocess, re

blob_hash = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'ls-tree', 'HEAD', 'src/app/(app)/teleapo/page.tsx'],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True, text=True
).stdout.split()[2]

raw = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'cat-file', 'blob', blob_hash],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True
).stdout

c = raw.decode('utf-8', errors='replace')

# テレアポページ内の小さい文字クラスを一括で大きくする
replacements = [
    # text-sm → text-base
    ('text-slate-200 leading-relaxed', 'text-slate-200 text-base leading-relaxed'),
    # ステップ説明・トーク文
    ('"text-sm text-slate-200 leading-relaxed flex-1"', '"text-base text-slate-200 leading-relaxed flex-1"'),
    # バリエーションのトーク文
    ('"text-sm text-white leading-relaxed"', '"text-base text-white leading-relaxed"'),
    # ポイント説明
    ('"text-xs text-slate-300 mt-2 leading-relaxed"', '"text-sm text-slate-300 mt-2 leading-relaxed"'),
    # キーワードバッジ以外のtext-xs → text-sm（ラベル類）
    ('"text-xs font-bold text-red-400 mb-2"', '"text-sm font-bold text-red-400 mb-2"'),
    ('"text-xs font-bold text-blue-400"', '"text-sm font-bold text-blue-400"'),
    ('"text-xs font-bold text-yellow-400"', '"text-sm font-bold text-yellow-400"'),
    ('"text-xs font-bold text-purple-400"', '"text-sm font-bold text-purple-400"'),
    ('"text-xs font-bold text-green-400"', '"text-sm font-bold text-green-400"'),
    ('"text-xs font-bold text-slate-400"', '"text-sm font-bold text-slate-400"'),
    # テーブルのtext-sm → text-base
    ('<table className="w-full text-sm">', '<table className="w-full text-base">'),
    # ステータス表のtd
    ('"text-slate-300 py-3 text-sm"', '"text-slate-300 py-3 text-base"'),
]

count = 0
for old, new in replacements:
    if old in c:
        n = c.count(old)
        c = c.replace(old, new)
        print(f'replaced {n}x: {old[:50]}')
        count += n

# 米山パターンのトーク本文（最重要）: text-sm text-slate-200 → text-base
c = re.sub(r'className="text-sm text-slate-200 leading-relaxed"', 'className="text-base text-slate-200 leading-relaxed"', c)
c = re.sub(r'className="text-sm text-white leading-relaxed font-medium"', 'className="text-lg text-white leading-relaxed font-medium"', c)
# ステップ説明の小さいテキスト
c = re.sub(r'<p className="text-sm text-slate-400 mb-4">', '<p className="text-base text-slate-400 mb-4">', c)
c = re.sub(r'<p className="text-sm text-slate-300 mt-1">', '<p className="text-base text-slate-300 mt-1">', c)

print(f'total: {count} replacements')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('saved')
