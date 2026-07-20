'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

export default function EditManualPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [category, setCategory] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchManual = async () => {
      const supabase = createClient()
      const { data } = await supabase
        .from('manuals')
        .select('*')
        .eq('id', params.id)
        .single()
      if (data) {
        setTitle(data.title)
        setCategory(data.category ?? '')
        setContent(data.content ?? '')
      }
      setFetching(false)
    }
    fetchManual()
  }, [params.id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const supabase = createClient()
    const { error } = await supabase
      .from('manuals')
      .update({
        title: title.trim(),
        category: category.trim() || null,
        content: content.trim(),
        updated_at: new Date().toISOString(),
      })
      .eq('id', params.id)

    if (error) {
      setError('保存に失敗しました: ' + error.message)
      setLoading(false)
      return
    }

    router.push(`/manuals/${params.id}`)
  }

  const handleDelete = async () => {
    if (!confirm('このマニュアルを削除しますか？')) return
    const supabase = createClient()
    await supabase.from('manuals').delete().eq('id', params.id)
    router.push('/manuals')
  }

  if (fetching) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-slate-400">読み込み中...</p>
      </div>
    )
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">マニュアルを編集</h1>
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
              required
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">カテゴリ</label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">内容</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={16}
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-mono resize-y"
            />
          </div>
        </div>

        {error && (
          <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
        )}

        <div className="flex gap-3 justify-between">
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white font-medium rounded-xl transition-colors"
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
          <button
            type="button"
            onClick={handleDelete}
            className="px-6 py-3 bg-red-600/20 hover:bg-red-600/40 text-red-400 font-medium rounded-xl transition-colors"
          >
            削除
          </button>
        </div>
      </form>
    </div>
  )
}
