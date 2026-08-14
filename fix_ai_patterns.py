with open(r'C:\Users\fyone\Desktop\teleapo_blob.tsx', 'r', encoding='utf-8-sig') as f:
    c = f.read()

# aiPatternの型を拡張
c = c.replace(
    "const [aiPattern, setAiPattern] = useState<'yoneyama' | 'hashimoto'>('yoneyama')",
    "const [aiPattern, setAiPattern] = useState<string>('yoneyama')"
)

# パターン選択UIを橋本削除→複数パターンに
old_buttons = """              <button onClick={() => setAiPattern('yoneyama')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'yoneyama' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💰 米山パターン（IT補助金訴求）
              </button>
              <button onClick={() => setAiPattern('hashimoto')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'hashimoto' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💬 橋本パターン（ヒアリング型）
              </button>"""

new_buttons = """              {[
                { id: 'yoneyama', label: '💰 IT補助金訴求', color: 'yellow' },
                { id: 'price', label: '💴 価格・コスト訴求', color: 'green' },
                { id: 'inbound', label: '🌏 インバウンド訴求', color: 'blue' },
                { id: 'case', label: '🏨 導入事例訴求', color: 'purple' },
                { id: 'urgency', label: '⏰ 緊急性訴求', color: 'red' },
              ].map(p => (
                <button key={p.id} onClick={() => setAiPattern(p.id)}
                  className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === p.id
                    ? p.color === 'yellow' ? 'bg-yellow-600 text-white'
                    : p.color === 'green' ? 'bg-green-600 text-white'
                    : p.color === 'blue' ? 'bg-blue-600 text-white'
                    : p.color === 'purple' ? 'bg-purple-600 text-white'
                    : 'bg-red-600 text-white'
                    : 'bg-slate-700 text-slate-300 border border-slate-600 hover:bg-slate-600'}`}>
                  {p.label}
                </button>
              ))}"""

if old_buttons in c:
    c = c.replace(old_buttons, new_buttons)
    print('pattern buttons replaced')
else:
    print('pattern buttons NOT found')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('saved')
