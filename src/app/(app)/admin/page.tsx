'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export default function AdminPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    const supabase = createClient()
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      setError('招待の送信に失敗しました: ' + error.message)
    } else {
      setMessage(`${email} に招待リンクを送信しました`)
      setEmail('')
    }
    setLoading(false)
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">メンバー管理</h1>
        <p className="text-slate-400 text-sm mt-1">チームメンバーの招待</p>
      </div>

      {/* Invite Form */}
      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 max-w-lg mb-8">
        <h2 className="text-lg font-semibold text-white mb-4">メンバーを招待</h2>
        <form onSubmit={handleInvite} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              メールアドレス
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="招待するメールアドレス"
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          {message && (
            <p className="text-green-400 text-sm bg-green-400/10 px-4 py-3 rounded-xl">✓ {message}</p>
          )}
          {error && (
            <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading || !email}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors"
          >
            {loading ? '送信中...' : '招待メールを送る'}
          </button>
        </form>
      </div>

      {/* Info */}
      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 max-w-lg">
        <h2 className="text-base font-semibold text-white mb-3">📌 招待の仕組み</h2>
        <ul className="space-y-2 text-sm text-slate-400">
          <li className="flex items-start gap-2">
            <span className="text-blue-400 mt-0.5">1.</span>
            招待するメールアドレスを入力して送信
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-400 mt-0.5">2.</span>
            相手のメールにログインリンクが届く
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-400 mt-0.5">3.</span>
            リンクをクリックするとシステムにアクセスできる
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-400 mt-0.5">⚠️</span>
            招待リンクの有効期限は24時間です
          </li>
        </ul>
      </div>
    </div>
  )
}
