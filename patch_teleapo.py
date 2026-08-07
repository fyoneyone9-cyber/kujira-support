
import re, sys

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original lines: {content.count(chr(10))}", flush=True)

# 1. import useCallbackを追加
content = content.replace(
    "import { useState } from 'react'",
    "import { useState, useCallback } from 'react'"
)

# 2. AiSuggestion型をTABSの直前に追加
content = content.replace(
    "const TABS = [",
    "type AiSuggestion = { label: string; talk: string; point: string }\n\nconst TABS = ["
)

# 3. TABSに米山パターンタブを追加
content = content.replace(
    "  { id: 'script', label: '📞 トークスクリプト', icon: '📞' },\n  { id: 'status',",
    "  { id: 'script', label: '📞 トークスクリプト', icon: '📞' },\n  { id: 'yoneyama', label: '💰 米山パターン', icon: '💰' },\n  { id: 'status',"
)

# 4. 瀬戸パターンセクションを削除
seto_start = "          {/* パターンA */}"
status_tab = "      {/* ─── TAB: ステータス一覧 ─── */}"

idx_seto = content.find(seto_start)
idx_status = content.find(status_tab)

if idx_seto != -1 and idx_status != -1:
    # 直前の改行まで削除
    content = content[:idx_seto].rstrip() + "\n        </div>\n      )}\n\n" + content[idx_status:]
    print("Deleted Seto/Hashimoto patterns", flush=True)
else:
    print(f"WARNING: seto_start found={idx_seto != -1}, status_tab found={idx_status != -1}", flush=True)

# 5. AI state追加（export default function TeleapoPage の直後）
old_state = """  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)"""

new_state = """  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)

  // ── AI サジェスト (Gemini) ──
  const [aiInput, setAiInput] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AiSuggestion[]>([])
  const [aiError, setAiError] = useState<string | null>(null)
  const [aiSelectedIdx, setAiSelectedIdx] = useState<number | null>(null)
  const [aiPattern, setAiPattern] = useState<'yoneyama' | 'hashimoto'>('yoneyama')

  const fetchAiSuggestions = useCallback(async (text: string, pattern: string) => {
    if (!text.trim()) return
    setAiLoading(true)
    setAiError(null)
    setAiSuggestions([])
    setAiSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setAiSuggestions(data.suggestions ?? [])
    } catch (e) {
      setAiError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setAiLoading(false)
    }
  }, [])

  // ── 米山パターン用 AI input ──
  const [yoneyamaInput, setYoneyamaInput] = useState('')
  const [yoneyamaLoading, setYoneyamaLoading] = useState(false)
  const [yoneyamaSuggestions, setYoneyamaSuggestions] = useState<AiSuggestion[]>([])
  const [yoneyamaError, setYoneyamaError] = useState<string | null>(null)
  const [yoneyamaSelectedIdx, setYoneyamaSelectedIdx] = useState<number | null>(null)

  const fetchYoneyamaSuggestions = useCallback(async (text: string) => {
    if (!text.trim()) return
    setYoneyamaLoading(true)
    setYoneyamaError(null)
    setYoneyamaSuggestions([])
    setYoneyamaSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern: 'yoneyama' }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setYoneyamaSuggestions(data.suggestions ?? [])
    } catch (e) {
      setYoneyamaError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setYoneyamaLoading(false)
    }
  }, [])"""

content = content.replace(old_state, new_state)

# 6. AIサジェストセクション（キーワードマッチング）をGemini版に差し替え
old_ai_section_start = "          {/* ── AI切り返しサジェスト ── */}"
old_ai_section_end = "          {/* ── メモ欄 ── */}"

new_ai_section = """          {/* ── AI切り返しサジェスト (Gemini API) ── */}
          <div className="bg-slate-900 rounded-2xl border border-purple-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返しサジェスト</h2>
              <span className="text-xs bg-purple-900/60 border border-purple-700/50 text-purple-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">相手が言ったことをそのまま入力 → AIがデバイスエージェンシーの製品切り返しを表示</p>
            <div className="flex gap-2 mb-4">
              <button onClick={() => setAiPattern('yoneyama')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'yoneyama' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💰 米山パターン（IT補助金訴求）
              </button>
              <button onClick={() => setAiPattern('hashimoto')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'hashimoto' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💬 橋本パターン（ヒアリング型）
              </button>
            </div>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={aiInput} onChange={e => setAiInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchAiSuggestions(aiInput, aiPattern)}
                  placeholder="例：「もう他社のシステム入れてます」「今は忙しくて」「高そうだな」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30" />
                {aiInput && <button onClick={() => { setAiInput(''); setAiSuggestions([]); setAiSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${aiLoading ? 'bg-purple-900 text-purple-400 cursor-wait' : aiInput.trim() ? 'bg-purple-600 hover:bg-purple-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {aiLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {aiError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">⚠️ {aiError}</div>}
            {aiLoading && <div className="text-center py-8 text-purple-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-sm">Gemini AIが切り返しを生成中...</p></div>}
            {aiSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-purple-400 font-bold mb-3">💡 AI推奨切り返し ({aiSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {aiSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setAiSelectedIdx(aiSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${aiSelectedIdx === i ? 'bg-purple-600 text-white shadow-lg scale-105' : 'bg-purple-900/50 text-purple-200 hover:bg-purple-700 hover:text-white border border-purple-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {aiSelectedIdx !== null && aiSuggestions[aiSelectedIdx] && (
                  <div className="bg-purple-950/60 border-2 border-purple-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-purple-400 font-bold">💬 {aiSuggestions[aiSelectedIdx].label}</p>
                        <p className="text-xs text-purple-300/70 mt-0.5">📌 {aiSuggestions[aiSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(aiSuggestions[aiSelectedIdx!].talk, 'ai_suggest')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'ai_suggest' ? 'bg-purple-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'ai_suggest' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{aiSuggestions[aiSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ── メモ欄 ── */}"""

idx_start = content.find(old_ai_section_start)
idx_end = content.find(old_ai_section_end)

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + new_ai_section + content[idx_end + len(old_ai_section_end):]
    print("AI section replaced", flush=True)
else:
    print(f"WARNING: ai_section not found. start={idx_start}, end={idx_end}", flush=True)

# 7. 米山パターンタブを ステータス一覧タブの直前に挿入
yoneyama_tab = """
      {/* ─── TAB: 米山パターン ─── */}
      {activeTab === 'yoneyama' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-yellow-900/40 to-orange-900/40 border border-yellow-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金全面訴求型</h2>
                <p className="text-sm text-yellow-300/80 mt-0.5">IT補助金を前面に出し、2025年テレアポトレンドを反映したスクリプト</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl border border-yellow-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返し（米山パターン専用）</h2>
              <span className="text-xs bg-yellow-900/60 border border-yellow-700/50 text-yellow-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">相手の発言を入力 → IT補助金訴求を含む切り返しをAIが生成</p>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={yoneyamaInput} onChange={e => setYoneyamaInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchYoneyamaSuggestions(yoneyamaInput)}
                  placeholder="例：「予算がない」「他社で検討中」「今は時期が悪い」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 focus:ring-2 focus:ring-yellow-500/30" />
                {yoneyamaInput && <button onClick={() => { setYoneyamaInput(''); setYoneyamaSuggestions([]); setYoneyamaSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button onClick={() => fetchYoneyamaSuggestions(yoneyamaInput)} disabled={!yoneyamaInput.trim() || yoneyamaLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${yoneyamaLoading ? 'bg-yellow-900 text-yellow-400 cursor-wait' : yoneyamaInput.trim() ? 'bg-yellow-600 hover:bg-yellow-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {yoneyamaLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {yoneyamaError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">⚠️ {yoneyamaError}</div>}
            {yoneyamaLoading && <div className="text-center py-8 text-yellow-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-sm">Gemini AIが米山パターンで生成中...</p></div>}
            {yoneyamaSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-yellow-400 font-bold mb-3">💡 AI推奨切り返し ({yoneyamaSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {yoneyamaSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setYoneyamaSelectedIdx(yoneyamaSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${yoneyamaSelectedIdx === i ? 'bg-yellow-600 text-white shadow-lg scale-105' : 'bg-yellow-900/50 text-yellow-200 hover:bg-yellow-700 hover:text-white border border-yellow-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {yoneyamaSelectedIdx !== null && yoneyamaSuggestions[yoneyamaSelectedIdx] && (
                  <div className="bg-yellow-950/60 border-2 border-yellow-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-yellow-400 font-bold">💬 {yoneyamaSuggestions[yoneyamaSelectedIdx].label}</p>
                        <p className="text-xs text-yellow-300/70 mt-0.5">📌 {yoneyamaSuggestions[yoneyamaSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(yoneyamaSuggestions[yoneyamaSelectedIdx!].talk, 'yoneyama_ai')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'yoneyama_ai' ? 'bg-yellow-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'yoneyama_ai' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{yoneyamaSuggestions[yoneyamaSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📞 米山パターン — トークスクリプト</h2>
            <div className="space-y-3">
              {[
                { label: '① オープニング（受付突破）', color: 'blue', text: '「お忙しいところ恐れ入ります。デバイスエージェンシーの米山でございます。本日は、ホテル・旅館様向けのIT補助金活用でご導入できる自動チェックイン機のご案内でご連絡しました。ご担当者様かご支配人様はいらっしゃいますでしょうか？」' },
                { label: '② IT補助金を前面に出す', color: 'yellow', text: '「弊社では今、IT補助金の申請を全て弊社が代行する形で、自動チェックイン機をお手頃な価格でご導入いただけています。KIOSK型が実質48万円〜、タブレット型が13万円〜とご好評いただいておりまして。売り込みではなく、補助金活用の情報をお伝えしたくてご連絡しました。」' },
                { label: '③ ヒアリング', color: 'purple', text: '「最近、業界全体でインバウンド対応や人手不足のお声をよくお聞きするのですが、御社では現在、何か運用上の課題はお感じですか？」' },
                { label: '④ YES → 提案', color: 'green', text: '「そうですよね。その課題をIT補助金を活用して解決された事例が手元にあります。資料だけでもメールでお送りしてもよろしいでしょうか？」' },
                { label: '⑤ NO → 情報だけ提案', color: 'slate', text: '「承知しました。IT補助金は毎年申請枠がありますので、タイミングが来た時のためだけでも資料をお手元に置いていただければ。メールアドレスをお教えいただけますか？」' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' : item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' : item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' : item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' : 'bg-slate-700/50 border border-slate-600/40'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <p className={`text-xs font-bold ${item.color === 'blue' ? 'text-blue-400' : item.color === 'yellow' ? 'text-yellow-400' : item.color === 'purple' ? 'text-purple-400' : item.color === 'green' ? 'text-green-400' : 'text-slate-400'}`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `ym_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-sm text-slate-200 leading-relaxed">{item.text}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔄 断り文句別 切り返し（IT補助金訴求）</h2>
            <div className="space-y-3">
              {[
                { obj: '「予算がない」「お金がかかる」', res: '「そうですよね。実はIT補助金を活用していただくと、弊社が申請を全て代行しますので、KIOSK型が48万円〜、タブレット型が13万円〜でご導入できます。月額費用も使わない月は0円なので、繁忙期だけのご利用も可能です。資料だけでもご覧になりませんか？」' },
                { obj: '「他社製品を検討・使用中」', res: '「弊社はシリンダー錠対応・完全オーダーメイドカスタマイズという点で差別化できています。またIT補助金の申請代行は弊社の強みです。比較検討の資料としてお送りしてもよろしいでしょうか？」' },
                { obj: '「今は時期が悪い」「来年以降で」', res: '「IT補助金の申請枠は毎年更新されますので、今すぐでなくても情報だけ持っておいていただくと、タイミングが来た時にすぐ動けます。今日中に資料をメールでお送りするだけですので、メールアドレスをお教えいただけますか？」' },
                { obj: '「補助金って何ですか？」', res: '「IT導入補助金というもので、中小企業様がITシステムを導入する際に国が費用の最大2/3を補助してくれる制度です。弊社は申請手続きを全て代行しておりますので、御社は書類を揃えていただくだけでOKです。」' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-red-400 mb-2">❌ {item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">✅ {item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

"""

content = content.replace(
    "\n      {/* ─── TAB: ステータス一覧 ─── */}",
    yoneyama_tab + "      {/* ─── TAB: ステータス一覧 ─── */}"
)

print(f"Final lines: {content.count(chr(10))}", flush=True)

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done!", flush=True)
