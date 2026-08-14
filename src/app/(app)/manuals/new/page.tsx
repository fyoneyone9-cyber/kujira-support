'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

type AudienceType = 'internal' | 'customer'

export default function NewManualPage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [category, setCategory] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiAudience, setAiAudience] = useState<AudienceType>('internal')

  const generateWithAI = async (audience: AudienceType) => {
    if (!title.trim()) { setError('タイトルを入力してからAI生成してください'); return }
    setAiLoading(true)
    setAiAudience(audience)
    setError('')
    try {
      const res = await fetch('/api/ai/manual-generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, category, audience }),
      })
      const data = await res.json()
      if (data.error) setError(data.error)
      else setContent(data.content)
    } catch {
      setError('AI生成に失敗しました')
    } finally {
      setAiLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { data: { user } } = await supabase.auth.getUser()

    const { data, error } = await supabase.from('manuals').insert({
      title: title.trim(),
      category: category.trim() || null,
      content: content.trim(),
      created_by: user?.id,
    }).select().single()

    if (error) {
      setError('保存に失敗しました: ' + error.message)
      setLoading(false)
      return
    }

    router.push(`/manuals/${data.id}`)
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">新規マニュアル作成</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              タイトル <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="例: IoT機器の初期設定手順"
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              カテゴリ
            </label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="例: 機器設定 / トラブルシューティング"
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          {/* AI生成ボタン */}
          <div className="border border-slate-600 rounded-xl p-4 bg-slate-700/30">
            <p className="text-sm font-medium text-slate-300 mb-3">🤖 Gemini AIで内容を自動生成</p>
            <div className="flex gap-3">
              <button type="button" onClick={() => generateWithAI('internal')}
                disabled={aiLoading || !title.trim()}
                className={`flex-1 py-3 rounded-xl text-sm font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${aiLoading && aiAudience === 'internal' ? 'bg-blue-700 text-white' : 'bg-blue-600 hover:bg-blue-500 text-white'}`}>
                {aiLoading && aiAudience === 'internal' ? <><span className="animate-spin">⏳</span> 生成中...</> : <>🏢 社内向けで生成</>}
              </button>
              <button type="button" onClick={() => generateWithAI('customer')}
                disabled={aiLoading || !title.trim()}
                className={`flex-1 py-3 rounded-xl text-sm font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${aiLoading && aiAudience === 'customer' ? 'bg-green-700 text-white' : 'bg-green-600 hover:bg-green-500 text-white'}`}>
                {aiLoading && aiAudience === 'customer' ? <><span className="animate-spin">⏳</span> 生成中...</> : <>👤 顧客向けで生成</>}
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-2">タイトルを入力してからボタンを押してください。生成後に内容を編集できます。</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              内容
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="手順や注意事項を記載してください..."
              rows={16}
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-mono resize-y"
            />
            <p className="text-xs text-slate-500 mt-1">マークダウン形式で記述できます</p>
          </div>
        </div>

        {error && (
          <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading || !title.trim()}
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
