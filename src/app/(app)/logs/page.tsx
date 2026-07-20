import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'

export default async function LogsPage({
  searchParams,
}: {
  searchParams: { q?: string }
}) {
  const supabase = createClient()
  let query = supabase
    .from('slack_logs')
    .select('id, title, content, created_at')
    .order('created_at', { ascending: false })

  if (searchParams.q) {
    query = query.or(`title.ilike.%${searchParams.q}%,content.ilike.%${searchParams.q}%`)
  }

  const { data: logs } = await query

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Slackログ</h1>
          <p className="text-slate-400 text-sm mt-1">やり取りをそのまま貼る場所</p>
        </div>
        <Link
          href="/logs/new"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-xl transition-colors"
        >
          ＋ 貼り付ける
        </Link>
      </div>

      {/* Search */}
      <form method="GET" className="mb-6">
        <input
          name="q"
          defaultValue={searchParams.q}
          placeholder="キーワードで検索..."
          className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </form>

      {/* List */}
      <div className="space-y-3">
        {logs && logs.length > 0 ? (
          logs.map((log) => (
            <Link
              key={log.id}
              href={`/logs/${log.id}`}
              className="block bg-slate-800 rounded-2xl p-5 border border-slate-700 hover:border-slate-500 transition-colors group"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium group-hover:text-blue-300 transition-colors truncate">
                    {log.title || '(タイトルなし)'}
                  </p>
                  <p className="text-slate-500 text-sm mt-1 line-clamp-2 font-mono">
                    {log.content?.slice(0, 120)}...
                  </p>
                </div>
                <p className="text-slate-500 text-xs whitespace-nowrap">
                  {new Date(log.created_at).toLocaleDateString('ja-JP')}
                </p>
              </div>
            </Link>
          ))
        ) : (
          <div className="bg-slate-800 rounded-2xl p-16 text-center border border-slate-700">
            <p className="text-4xl mb-4">💬</p>
            <p className="text-slate-400 font-medium">まだ何もありません</p>
            <Link
              href="/logs/new"
              className="mt-4 inline-block text-sm text-blue-400 hover:text-blue-300"
            >
              最初のやり取りを貼る →
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
