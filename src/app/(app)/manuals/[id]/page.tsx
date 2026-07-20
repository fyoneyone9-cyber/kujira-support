import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'
import { notFound } from 'next/navigation'

export default async function ManualDetailPage({
  params,
}: {
  params: { id: string }
}) {
  const supabase = createClient()
  const { data: manual } = await supabase
    .from('manuals')
    .select('*')
    .eq('id', params.id)
    .single()

  if (!manual) notFound()

  return (
    <div className="max-w-3xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <Link href="/manuals" className="text-slate-400 hover:text-white text-sm transition-colors">
            ← マニュアル一覧
          </Link>
          <h1 className="text-2xl font-bold text-white mt-2">{manual.title}</h1>
          <div className="flex items-center gap-3 mt-2">
            {manual.category && (
              <span className="text-xs text-blue-400 bg-blue-400/10 px-3 py-1 rounded-full">
                {manual.category}
              </span>
            )}
            <span className="text-xs text-slate-500">
              更新: {new Date(manual.updated_at).toLocaleDateString('ja-JP')}
            </span>
          </div>
        </div>
        <Link
          href={`/manuals/${manual.id}/edit`}
          className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm font-medium rounded-xl transition-colors"
        >
          ✏️ 編集
        </Link>
      </div>

      {/* Content */}
      <div className="bg-slate-800 rounded-2xl p-8 border border-slate-700">
        {manual.content ? (
          <pre className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-sans">
            {manual.content}
          </pre>
        ) : (
          <p className="text-slate-500 text-sm">内容がありません。編集から追加してください。</p>
        )}
      </div>
    </div>
  )
}
