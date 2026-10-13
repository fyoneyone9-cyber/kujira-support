import { createClient } from '@supabase/supabase-js'
import Link from 'next/link'
import { notFound } from 'next/navigation'

export default async function TroubleshootingDetailPage({
  params,
}: {
  params: { id: string }
}) {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )
  const { data: item } = await supabase
    .from('manuals')
    .select('*')
    .eq('id', params.id)
    .single()

  if (!item) notFound()

  return (
    <div className="max-w-3xl">
      {/* Back */}
      <Link
        href="/troubleshooting"
        className="inline-flex items-center gap-2 text-slate-400 hover:text-white text-sm mb-6 transition-colors"
      >
        ← トラブルシューティング一覧
      </Link>

      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          {item.category && (
            <span className="px-2 py-0.5 bg-orange-900/40 text-orange-300 rounded-full border border-orange-800/40 text-xs">
              {item.category}
            </span>
          )}
          <span className="text-slate-500 text-xs">
            更新: {new Date(item.updated_at).toLocaleDateString('ja-JP')}
          </span>
        </div>
        <h1 className="text-2xl font-bold text-white">{item.title}</h1>
      </div>

      {/* Content */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <div
          className="prose prose-invert prose-sm max-w-none text-slate-300 leading-relaxed whitespace-pre-wrap"
        >
          {item.content}
        </div>
      </div>

      {/* Edit */}
      <div className="mt-4 flex gap-3">
        <Link
          href={`/manuals/${item.id}/edit`}
          className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded-xl border border-slate-600 transition-colors"
        >
          ✏️ 編集
        </Link>
      </div>
    </div>
  )
}
