'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { error } = await supabase.auth.signInWithPassword({ email, password })

    if (error) {
      setError('メールアドレスまたはパスワードが違います')
      setLoading(false)
    } else {
      router.push('/dashboard')
      router.refresh()
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-600 mb-4">
            <span className="text-2xl">🐋</span>
          </div>
          <h1 className="text-2xl font-bold text-white">KUJIRA</h1>
          <p className="text-slate-400 text-sm mt-1">導入支援サポートシステム</p>
        </div>

        <div className="bg-slate-800 rounded-2xl p-8 shadow-xl border border-slate-700">
          <h2 className="text-xl font-semibold text-white mb-6">ログイン</h2>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">メールアドレス</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">パスワード</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>

            {error && (
              <p className="text-red-400 text-sm bg-red-400/10 px-3 py-2 rounded-xl">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading || !email || !password}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors"
            >
              {loading ? 'ログイン中...' : 'ログイン'}
            </button>
          </form>
          <p className="mt-6 text-xs text-slate-500 text-center">
            招待されたアカウントのみログインできます
          </p>
        </div>
      </div>
    </div>
  )
}
