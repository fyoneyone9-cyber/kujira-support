import { createClient } from '@supabase/supabase-js'
import Link from 'next/link'

export default async function TroubleshootingPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; category?: string }>
}) {
  const params = await searchParams
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const catFilter = params.category || 'トラブルシューティング'

  let query = supabase
    .from('manuals')
    .select('id, title, category, created_at, updated_at')
    .eq('category', catFilter)
    .order('updated_at', { ascending: false })

  if (params.q) {
    query = query.ilike('title', `%${params.q}%`)
  }

  const { data: items } = await query

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">🔧 トラブルシューティング</h1>
          <p className="text-slate-400 text-sm mt-1">機器・システムの障害対応手順</p>
        </div>
        <Link
          href="/manuals/new"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-xl transition-colors"
        >
          ✚ 新規作成
        </Link>
      </div>

      {/* Search */}
      <div className="flex gap-3 mb-6">
        <form method="GET" className="flex gap-3 flex-1">
          <input
            type="text"
            name="q"
            defaultValue={params.q}
            placeholder="キーワードで検索..."
            className="flex-1 px-4 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded-xl border border-slate-600 transition-colors"
          >
            検索
          </button>
        </form>
      </div>

      {/* タグ */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {['P400', 'KIOSK', 'PayCube', 'ネットワーク', 'その他'].map((tag) => (
          <Link
            key={tag}
            href={`/troubleshooting?category=${encodeURIComponent(tag)}`}
            className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs rounded-full border border-slate-600 transition-colors"
          >
            {tag}
          </Link>
        ))}
        <Link
          href="/troubleshooting"
          className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-400 text-xs rounded-full border border-slate-600 transition-colors"
        >
          すべて表示
        </Link>
      </div>

      {/* List */}
      {!items || items.length === 0 ? (
        <div className="text-center py-16 text-slate-500">
          <p className="text-4xl mb-4">🔧</p>
          <p>トラブルシューティング手順がまだありません</p>
          <Link href="/manuals/new" className="mt-4 inline-block text-blue-400 hover:text-blue-300 text-sm">
            最初の手順を作成する →
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <Link
              key={item.id}
              href={`/troubleshooting/${item.id}`}
              className="block bg-slate-800 border border-slate-700 hover:border-blue-500 rounded-xl p-5 transition-all"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h3 className="text-white font-medium text-sm mb-1">{item.title}</h3>
                  <div className="flex items-center gap-3 text-xs text-slate-500">
                    {item.category && (
                      <span className="px-2 py-0.5 bg-orange-900/40 text-orange-300 rounded-full border border-orange-800/40">
                        {item.category}
                      </span>
                    )}
                    <span>更新: {new Date(item.updated_at).toLocaleDateString('ja-JP')}</span>
                  </div>
                </div>
                <span className="text-slate-500 text-sm flex-shrink-0">→</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
