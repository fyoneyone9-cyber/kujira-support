'use client'

import { useState } from 'react'

function renderMarkdown(text: string) {
  const lines = text.split('\n')
  const elements: React.ReactNode[] = []
  let key = 0
  let inSpamSection = false

  for (const line of lines) {
    if (line.startsWith('## ')) {
      inSpamSection = line.includes('迷惑') || line.includes('スパム')
      const isSpam = inSpamSection
      elements.push(
        <h2 key={key++} className={`text-base font-bold mt-5 mb-2 flex items-center gap-2 ${isSpam ? 'text-yellow-400' : 'text-white'}`}>
          {line.replace('## ', '')}
        </h2>
      )
    } else if (line.startsWith('- ')) {
      const content = line.replace('- ', '')
      const isWarning = content.includes('⚠️') || content.includes('迷惑') || content.includes('スパム') || content.includes('詐欺') || content.includes('フィッシング')
      const isOk = content.includes('✅')
      elements.push(
        <li key={key++} className={`text-sm ml-4 list-disc leading-relaxed ${isWarning ? 'text-yellow-300 font-medium' : isOk ? 'text-green-300' : 'text-slate-300'}`}>
          {content}
        </li>
      )
    } else if (line.trim() === '') {
      elements.push(<div key={key++} className="h-1" />)
    } else {
      const isWarning = line.includes('⚠️') || (inSpamSection && line.includes('可能性'))
      const isOk = line.includes('✅') && inSpamSection
      elements.push(
        <p key={key++} className={`text-sm leading-relaxed ${isWarning ? 'text-yellow-300 font-medium' : isOk ? 'text-green-300 font-medium' : 'text-slate-300'}`}>
          {line}
        </p>
      )
    }
  }
  return elements
}

export default function AiSummaryPage() {
  const [emailText, setEmailText] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  // 電話番号判定
  const [phone, setPhone] = useState('')
  const [phoneResult, setPhoneResult] = useState<{ verdict: string; reason: string; recommend: string } | null>(null)
  const [phoneLoading, setPhoneLoading] = useState(false)
  const [phoneError, setPhoneError] = useState('')

  const handlePhoneCheck = async () => {
    if (!phone.trim()) return
    setPhoneLoading(true)
    setPhoneResult(null)
    setPhoneError('')
    try {
      const res = await fetch('/api/ai/phone-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: phone.trim() }),
      })
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setPhoneResult(data)
    } catch (e) {
      setPhoneError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setPhoneLoading(false)
    }
  }

  const handleSummarize = async () => {
    if (!emailText.trim()) return
    setLoading(true)
    setSummary('')
    setError('')
    try {
      const res = await fetch('/api/ai/email-summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: emailText }),
      })
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setSummary(data.summary)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(summary)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleClear = () => {
    setEmailText('')
    setSummary('')
    setError('')
  }

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          🤖 メール・Slack AI要約 ＋ 迷惑電話AI判定
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          メール・Slackの内容をAIで要約／電話番号の迷惑判定
        </p>
      </div>

      {/* 電話番号判定 */}
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 mb-6">
        <label className="block text-sm font-medium text-slate-300 mb-3">☎️ 電話番号 迷惑判定</label>
        <div className="flex gap-2">
          <input
            value={phone}
            onChange={e => setPhone(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handlePhoneCheck()}
            placeholder="例: 0120-000-000 / 03-1234-5678"
            className="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 text-sm"
          />
          <button
            onClick={handlePhoneCheck}
            disabled={!phone.trim() || phoneLoading}
            className="px-5 py-2.5 bg-yellow-600 hover:bg-yellow-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-xl transition-colors whitespace-nowrap"
          >
            {phoneLoading ? '判定中...' : '🔍 判定'}
          </button>
        </div>

        {phoneError && (
          <p className="text-red-400 text-sm mt-3">⚠️ {phoneError}</p>
        )}

        {phoneResult && (
          <div className={`mt-4 rounded-xl p-4 border ${
            phoneResult.verdict.includes('迷惑') || phoneResult.verdict.includes('注意')
              ? 'bg-yellow-900/20 border-yellow-700/50'
              : phoneResult.verdict.includes('詐欺') || phoneResult.verdict.includes('危険')
              ? 'bg-red-900/20 border-red-700/50'
              : 'bg-green-900/20 border-green-700/50'
          }`}>
            <p className={`text-base font-bold mb-2 ${
              phoneResult.verdict.includes('迷惑') || phoneResult.verdict.includes('注意') ? 'text-yellow-400'
              : phoneResult.verdict.includes('詐欺') || phoneResult.verdict.includes('危険') ? 'text-red-400'
              : 'text-green-400'
            }`}>{phoneResult.verdict}</p>
            <p className="text-slate-300 text-sm mb-1"><span className="text-slate-500">根拠：</span>{phoneResult.reason}</p>
            <p className="text-slate-300 text-sm"><span className="text-slate-500">推奨：</span>{phoneResult.recommend}</p>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 mb-4">
        <label className="block text-sm font-medium text-slate-300 mb-3">
          📋 メール本文を貼り付け
        </label>
        <textarea
          value={emailText}
          onChange={(e) => setEmailText(e.target.value)}
          placeholder="ここにメール本文をコピー＆ペーストしてください..."
          className="w-full h-56 bg-slate-900 border border-slate-600 rounded-xl p-4 text-slate-200 text-sm placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none leading-relaxed"
        />
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-slate-500">{emailText.length} 文字</span>
          <div className="flex gap-2">
            {emailText && (
              <button
                onClick={handleClear}
                className="px-4 py-2 text-sm text-slate-400 hover:text-white border border-slate-600 hover:border-slate-500 rounded-xl transition-colors"
              >
                クリア
              </button>
            )}
            <button
              onClick={handleSummarize}
              disabled={!emailText.trim() || loading}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-xl transition-colors flex items-center gap-2"
            >
              {loading ? (
                <>
                  <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  要約中...
                </>
              ) : (
                <>✨ AI要約する</>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-900/30 border border-red-700 rounded-xl p-4 mb-4 text-red-300 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Result */}
      {summary && (
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold text-slate-300">📊 要約結果</h2>
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 text-xs text-slate-400 hover:text-white border border-slate-600 hover:border-slate-500 rounded-lg transition-colors"
            >
              {copied ? '✅ コピーした' : '📋 コピー'}
            </button>
          </div>
          <div className="border-t border-slate-700 pt-4">
            {renderMarkdown(summary)}
          </div>
        </div>
      )}
    </div>
  )
}
