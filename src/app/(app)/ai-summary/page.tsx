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
      elements.push(
        <h2 key={key++} className={`text-base font-bold mt-4 mb-2 ${inSpamSection ? 'text-yellow-400' : 'text-white'}`}>
          {line.replace('## ', '')}
        </h2>
      )
    } else if (line.startsWith('- ')) {
      const content = line.replace('- ', '')
      const isWarning = content.includes('⚠️') || content.includes('迷惑') || content.includes('詐欺')
      const isOk = content.includes('✅')
      elements.push(
        <li key={key++} className={`text-base ml-4 list-disc leading-relaxed ${isWarning ? 'text-yellow-300 font-medium' : isOk ? 'text-green-300' : 'text-slate-300'}`}>
          {content}
        </li>
      )
    } else if (line.trim() === '') {
      elements.push(<div key={key++} className="h-1" />)
    } else {
      const isWarning = line.includes('⚠️') || (inSpamSection && line.includes('可能性'))
      elements.push(
        <p key={key++} className={`text-base leading-relaxed ${isWarning ? 'text-yellow-300 font-medium' : 'text-slate-300'}`}>
          {line}
        </p>
      )
    }
  }
  return elements
}

export default function AiSummaryPage() {
  // 返信文
  const [replySource, setReplySource] = useState('')
  const [replyTone, setReplyTone] = useState('standard')
  const [replyText, setReplyText] = useState('')
  const [replyLoading, setReplyLoading] = useState(false)
  const [replyError, setReplyError] = useState('')
  const [replyCopied, setReplyCopied] = useState(false)

  // 要約
  const [emailText, setEmailText] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  // 電話判定
  const [phone, setPhone] = useState('')
  const [phoneResult, setPhoneResult] = useState<{ verdict: string; reason: string; recommend: string } | null>(null)
  const [phoneLoading, setPhoneLoading] = useState(false)
  const [phoneError, setPhoneError] = useState('')

  const handleReply = async () => {
    if (!replySource.trim()) return
    setReplyLoading(true)
    setReplyText('')
    setReplyError('')
    try {
      const res = await fetch('/api/ai/email-reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailContent: replySource, tone: replyTone }),
      })
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setReplyText(data.reply)
    } catch (e) {
      setReplyError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setReplyLoading(false)
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

  return (
    <div className="h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">🤖 AI ツール</h1>
          <p className="text-slate-400 text-base mt-1">返信文作成 / メール要約 / 迷惑電話判定</p>
        </div>
        <a
          href="https://gemini.google.com"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white text-base font-medium rounded-xl transition-all shadow-lg"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
          </svg>
          Gemini を開く ↗
        </a>
      </div>

      {/* 2カラムレイアウト */}
      <div className="grid grid-cols-2 gap-5 items-start">

        {/* 左：返信文作成（大） */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5 flex flex-col gap-3">
          <div>
            <p className="text-base font-semibold text-white">✉️ メール返信文作成</p>
            <p className="text-sm text-slate-500 mt-0.5">
              差出人：米山 文隆 &lt;humitaka_yoneyama@device-agency.co.jp&gt;　CC：support@and-iot.jp
            </p>
          </div>

          <textarea
            value={replySource}
            onChange={e => setReplySource(e.target.value)}
            placeholder="返信したいメール本文を貼り付け..."
            style={{ height: '238px' }}
            className="w-full bg-slate-900 border border-slate-600 rounded-xl p-3 text-slate-200 text-base placeholder-slate-500 focus:outline-none focus:border-emerald-500 resize-none leading-relaxed"
          />

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-400">トーン：</span>
              {[
                { value: 'formal', label: '🎩 丁寧' },
                { value: 'standard', label: '💼 標準' },
                { value: 'casual', label: '💬 簡潔' },
              ].map(t => (
                <button
                  key={t.value}
                  onClick={() => setReplyTone(t.value)}
                  className={`px-2.5 py-1 text-sm rounded-lg border transition-colors ${
                    replyTone === t.value
                      ? 'bg-emerald-700 border-emerald-500 text-white'
                      : 'bg-slate-700 border-slate-600 text-slate-400 hover:text-white'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
            <button
              onClick={handleReply}
              disabled={!replySource.trim() || replyLoading}
              className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-base font-medium rounded-xl transition-colors flex items-center gap-2"
            >
              {replyLoading
                ? <><span className="inline-block w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />生成中...</>
                : '✍️ 生成'}
            </button>
          </div>

          {replyError && <p className="text-red-400 text-sm">⚠️ {replyError}</p>}

          {replyText && (
            <div className="bg-slate-900 border border-slate-600 rounded-xl p-4 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">返信文</span>
                <button
                  onClick={() => { navigator.clipboard.writeText(replyText); setReplyCopied(true); setTimeout(() => setReplyCopied(false), 2000) }}
                  className="px-3 py-1 text-sm text-slate-400 hover:text-white border border-slate-600 rounded-lg transition-colors"
                >
                  {replyCopied ? '✅ コピー済み' : '📋 コピー'}
                </button>
              </div>
              <pre className="text-slate-200 text-base whitespace-pre-wrap leading-relaxed font-sans max-h-72 overflow-y-auto">{replyText}</pre>
            </div>
          )}
        </div>

        {/* 右：要約 + 電話判定 */}
        <div className="flex flex-col gap-4">

          {/* 要約 */}
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5 flex flex-col gap-3">
            <p className="text-base font-semibold text-white">✨ メール・Slack AI要約</p>
            <textarea
              value={emailText}
              onChange={e => setEmailText(e.target.value)}
              placeholder="メール・Slack本文を貼り付け..."
              className="w-full h-64 bg-slate-900 border border-slate-600 rounded-xl p-3 text-slate-200 text-base placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none leading-relaxed"
            />
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">{emailText.length} 文字</span>
              <div className="flex gap-2">
                {emailText && (
                  <button onClick={() => { setEmailText(''); setSummary(''); setError('') }}
                    className="px-3 py-1.5 text-sm text-slate-400 hover:text-white border border-slate-600 rounded-xl transition-colors">
                    クリア
                  </button>
                )}
                <button
                  onClick={handleSummarize}
                  disabled={!emailText.trim() || loading}
                  className="px-5 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-base font-medium rounded-xl transition-colors flex items-center gap-2"
                >
                  {loading
                    ? <><span className="inline-block w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />要約中...</>
                    : '✨ 要約'}
                </button>
              </div>
            </div>
            {error && <p className="text-red-400 text-sm">⚠️ {error}</p>}
            {summary && (
              <div className="bg-slate-900 border border-slate-600 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-400">要約結果</span>
                  <button onClick={() => { navigator.clipboard.writeText(summary); setCopied(true); setTimeout(() => setCopied(false), 2000) }}
                    className="px-3 py-1 text-sm text-slate-400 hover:text-white border border-slate-600 rounded-lg transition-colors">
                    {copied ? '✅ コピー済み' : '📋 コピー'}
                  </button>
                </div>
                <div className="max-h-48 overflow-y-auto">{renderMarkdown(summary)}</div>
              </div>
            )}
          </div>

          {/* 電話判定 */}
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5 flex flex-col gap-3">
            <p className="text-base font-semibold text-white">☎️ 迷惑電話AI判定</p>
            <div className="flex gap-2">
              <input
                value={phone}
                onChange={e => setPhone(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handlePhoneCheck()}
                placeholder="例: 0120-000-000"
                className="flex-1 px-3 py-2.5 bg-slate-900 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 text-base"
              />
              <button
                onClick={handlePhoneCheck}
                disabled={!phone.trim() || phoneLoading}
                className="px-4 py-2.5 bg-yellow-600 hover:bg-yellow-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-base font-medium rounded-xl transition-colors"
              >
                {phoneLoading ? '判定中...' : '🔍 判定'}
              </button>
            </div>
            {phoneError && <p className="text-red-400 text-sm">⚠️ {phoneError}</p>}
            {phoneResult && (
              <div className={`rounded-xl p-4 border ${
                phoneResult.verdict.includes('迷惑') || phoneResult.verdict.includes('注意') ? 'bg-yellow-900/20 border-yellow-700/50'
                : phoneResult.verdict.includes('詐欺') || phoneResult.verdict.includes('危険') ? 'bg-red-900/20 border-red-700/50'
                : 'bg-green-900/20 border-green-700/50'
              }`}>
                <p className={`text-base font-bold mb-1 ${
                  phoneResult.verdict.includes('迷惑') || phoneResult.verdict.includes('注意') ? 'text-yellow-400'
                  : phoneResult.verdict.includes('詐欺') || phoneResult.verdict.includes('危険') ? 'text-red-400'
                  : 'text-green-400'
                }`}>{phoneResult.verdict}</p>
                <p className="text-slate-300 text-sm mb-1"><span className="text-slate-500">根拠：</span>{phoneResult.reason}</p>
                <p className="text-slate-300 text-sm"><span className="text-slate-500">推奨：</span>{phoneResult.recommend}</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}
