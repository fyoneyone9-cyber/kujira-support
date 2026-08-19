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
          📧 AI要約
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          顧客メールをペーストしてAIが内容を整理します（第一弾：メール要約）
        </p>
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
