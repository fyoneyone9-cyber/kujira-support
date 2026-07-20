'use client'

import { useState } from 'react'

export default function AdminPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    const res = await fetch('/api/admin/create-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const data = await res.json()

    if (!res.ok) {
      setError(data.error ?? '登録に失敗しました')
    } else {
      setMessage(`${email} を登録しました`)
      setEmail('')
      setPassword('')
    }
    setLoading(false)
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">メンバー管理</h1>
        <p className="text-slate-400 text-sm mt-1">チームメンバーの追加</p>
      </div>

      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 max-w-lg mb-8">
        <h2 className="text-lg font-semibold text-white mb-4">メンバーを追加</h2>
        <form onSubmit={handleInvite} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">メールアドレス</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="member@example.com"
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">パスワード</label>
            <input
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="初期パスワードを設定"
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
            <p className="text-xs text-slate-500 mt-1">本人に直接伝えてください</p>
          </div>

          {message && <p className="text-green-400 text-sm bg-green-400/10 px-4 py-3 rounded-xl">✓ {message}</p>}
          {error && <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>}

          <button
            type="submit"
            disabled={loading || !email || !password}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors"
          >
            {loading ? '登録中...' : 'メンバーを追加する'}
          </button>
        </form>
      </div>

      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 max-w-lg">
        <h2 className="text-base font-semibold text-white mb-3">📌 使い方</h2>
        <ul className="space-y-2 text-sm text-slate-400">
          <li className="flex items-start gap-2"><span className="text-blue-400">1.</span> メールアドレスと初期パスワードを設定して追加</li>
          <li className="flex items-start gap-2"><span className="text-blue-400">2.</span> 本人にメールアドレスとパスワードを直接伝える</li>
          <li className="flex items-start gap-2"><span className="text-blue-400">3.</span> https://support.nextralab.jp/login からログイン</li>
        </ul>
      </div>
    </div>
  )
}
