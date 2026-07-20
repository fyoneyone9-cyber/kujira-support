'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

export default function NewLogPage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim()) return
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { data: { user } } = await supabase.auth.getUser()

    const { data, error } = await supabase.from('slack_logs').insert({
      title: title.trim() || null,
      content: content.trim(),
      created_by: user?.id,
    }).select().single()

    if (error) {
      setError('保存に失敗しました: ' + error.message)
      setLoading(false)
      return
    }

    router.push(`/logs/${data.id}`)
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Slackログを貼る</h1>
        <p className="text-slate-400 text-sm mt-1">タイトルは後でもOK。まず貼るだけ。</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              タイトル <span className="text-slate-500 text-xs font-normal">（省略可・後から編集できます）</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="例: IoT機器が繋がらない / 初期設定の流れ"
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Slackのやり取り <span className="text-red-400">*</span>
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="ここにSlackのやり取りをそのままコピペしてください..."
              rows={20}
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-mono resize-y"
            />
            <p className="text-xs text-slate-500 mt-1">
              {content.length > 0 ? `${content.length} 文字` : ''}
            </p>
          </div>
        </div>

        {error && (
          <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading || !content.trim()}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors"
          >
            {loading ? '保存中...' : '保存する'}
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-medium rounded-xl transition-colors"
          >
            キャンセル
          </button>
        </div>
      </form>
    </div>
  )
}
