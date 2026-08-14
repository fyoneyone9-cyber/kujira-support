import subprocess

# HEADのblobをバイナリで取得
blob_hash = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'ls-tree', 'HEAD', 'src/app/(app)/teleapo/page.tsx'],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True, text=True
).stdout.split()[2]

raw = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'cat-file', 'blob', blob_hash],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True
).stdout

# UTF-8として読む（文字化けがあっても）
c = raw.decode('utf-8', errors='replace')

# aiPatternの型を拡張
c = c.replace(
    "const [aiPattern, setAiPattern] = useState<'yoneyama' | 'hashimoto'>('yoneyama')",
    "const [aiPattern, setAiPattern] = useState<string>('yoneyama')"
)

# パターンボタンの旧コードを検索
import re
m = re.search(r"setAiPattern\('yoneyama'\).*?setAiPattern\('hashimoto'\).*?橋本.*?</button>", c, re.DOTALL)
if m:
    print('found at:', m.start(), '-', m.end())
    
    new_buttons = """setAiPattern('yoneyama')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'yoneyama' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💰 IT補助金訴求
              </button>
              <button onClick={() => setAiPattern('price')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'price' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💴 価格・コスト訴求
              </button>
              <button onClick={() => setAiPattern('inbound')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'inbound' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                🌏 インバウンド訴求
              </button>
              <button onClick={() => setAiPattern('case')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'case' ? 'bg-purple-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                🏨 導入事例訴求
              </button>
              <button onClick={() => setAiPattern('urgency')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'urgency' ? 'bg-red-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                ⏰ 緊急性訴求"""
    
    c = c[:m.start()] + new_buttons + c[m.end():]
    print('replaced')
else:
    print('not found, trying simpler search...')
    idx = c.find("setAiPattern('hashimoto')")
    if idx > 0:
        print('hashimoto found at:', idx, repr(c[idx-100:idx+200]))

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('saved, len:', len(c))
