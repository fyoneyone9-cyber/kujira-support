"""
PDFの内容（2026-08-12版）をteleapo/page.tsxのHubSpotタブに反映
- AIテレアポ導入後の新ステージ構成を追加
- 「あなたが電話する4つの箱」セクションを追加
"""
import re

path = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(path, encoding='utf-8') as f:
    content = f.read()

# HubSpotタブの冒頭（フロー説明の前）に新ステージ案内セクションを挿入
OLD = """      {/* フロー */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">"""

NEW = """      {/* AIテレアポ導入後の新ステージ案内（2026-08-12更新） */}
          <div className="bg-blue-950/40 border border-blue-700/50 rounded-2xl p-6 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">🤖</span>
              <div>
                <h2 className="text-base font-bold text-white">AIテレアポ導入後の役割分担</h2>
                <p className="text-sm text-blue-300/80 mt-0.5">2026年8月12日更新 / 不明点は田中さんへ</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-xs font-bold text-green-400 mb-2">✅ あなたが電話する4つの箱（優先順）</p>
                <div className="space-y-2">
                  {[
                    { num: '①', label: 'AIテレアポ結果', count: '1,237件', desc: '録音・メモ確認→前回の話を踏まえて電話。最も成果につながりやすい', color: 'green' },
                    { num: '②', label: 'IVR（突破待ち）', count: '283件', desc: '自動音声で止まった先。人の手で番号を押して突破する', color: 'blue' },
                    { num: '③', label: 'AIへの着信折り返し', count: '49件', desc: '相手からかけてきた→すぐ電話！', color: 'yellow' },
                    { num: '④', label: '本社・チェーン本部', count: '110件', desc: '1件決まれば傘下に波及。AIでは突破不可→人の力が必要', color: 'purple' },
                  ].map((item) => (
                    <div key={item.num} className={`flex items-start gap-3 p-3 rounded-xl border ${
                      item.color === 'green' ? 'bg-green-950/40 border-green-800/40' :
                      item.color === 'blue' ? 'bg-blue-950/40 border-blue-800/40' :
                      item.color === 'yellow' ? 'bg-yellow-950/40 border-yellow-800/40' :
                      'bg-purple-950/40 border-purple-800/40'
                    }`}>
                      <span className={`text-sm font-bold flex-shrink-0 ${
                        item.color === 'green' ? 'text-green-400' :
                        item.color === 'blue' ? 'text-blue-400' :
                        item.color === 'yellow' ? 'text-yellow-400' : 'text-purple-400'
                      }`}>{item.num}</span>
                      <div>
                        <p className="text-white text-xs font-bold">{item.label} <span className="text-slate-400 font-normal">({item.count})</span></p>
                        <p className="text-slate-300 text-xs mt-0.5">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs font-bold text-slate-400 mb-2">🤖 AIが担当（触らなくてOK）</p>
                <div className="space-y-1.5">
                  {[
                    { label: 'これから架電（未架電）', count: '16,367件', desc: 'AIが順番にかける' },
                    { label: 'AIテレアポ架電中', count: '2,453件', desc: '今まさにAIが架電中' },
                    { label: '留守番電話', count: '25件', desc: '後日AIがかけ直す' },
                    { label: '電話不出', count: '656件', desc: '何度かけても出ない先' },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2 p-2 bg-slate-700/40 rounded-lg">
                      <span className="text-slate-500 text-xs">🚫</span>
                      <p className="text-slate-400 text-xs">{item.label} <span className="text-slate-500">({item.count})</span> — {item.desc}</p>
                    </div>
                  ))}
                </div>
                <p className="text-xs font-bold text-slate-400 mb-2 mt-3">⏳ あとで（4箱消化後）</p>
                <div className="space-y-1.5">
                  {[
                    { label: 'メルマガ配信（見込顧客）', count: '208件' },
                    { label: '将来的見込顧客', count: '142件' },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2 p-2 bg-slate-600/30 rounded-lg">
                      <span className="text-slate-500 text-xs">📋</span>
                      <p className="text-slate-400 text-xs">{item.label} <span className="text-slate-500">({item.count})</span></p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="bg-red-950/40 border border-red-800/40 rounded-xl p-3">
              <p className="text-xs text-red-400 font-bold">⚠️ 鉄則：電話後は必ずメモを残す。AIも含め次の担当者が重複しないように。</p>
            </div>
          </div>

          {/* フロー */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">"""

count = content.count(OLD)
print(f"置換対象: {count}件")
content = content.replace(OLD, NEW)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 完了")
