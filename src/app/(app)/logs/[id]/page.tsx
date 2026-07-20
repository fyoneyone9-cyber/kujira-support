import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'
import { notFound } from 'next/navigation'

export default async function LogDetailPage({ params }: { params: { id: string } }) {
  const supabase = createClient()
  const { data: log } = await supabase
    .from('slack_logs')
    .select('*')
    .eq('id', params.id)
    .single()

  if (!log) notFound()

  return (
    <div className="max-w-3xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <Link href="/logs" className="text-slate-400 hover:text-white text-sm transition-colors">
            ← Slackログ一覧
          </Link>
          <h1 className="text-2xl font-bold text-white mt-2">
            {log.title || '(タイトルなし)'}
          </h1>
          <p className="text-slate-500 text-xs mt-1">
            {new Date(log.created_at).toLocaleString('ja-JP')}
          </p>
        </div>
        <div className="flex gap-2">
          <Link
            href={`/logs/${log.id}/edit`}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm font-medium rounded-xl transition-colors"
          >
            ✏️ 編集
          </Link>
          <Link
            href={`/manuals/new?from_log=${log.id}`}
            className="px-4 py-2 bg-green-600/30 hover:bg-green-600/50 text-green-400 text-sm font-medium rounded-xl transition-colors"
          >
            📋 マニュアル化
          </Link>
        </div>
      </div>

      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <pre className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-mono">
          {log.content}
        </pre>
      </div>
    </div>
  )
}
