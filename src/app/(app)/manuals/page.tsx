import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'

export default async function ManualsPage({
  searchParams,
}: {
  searchParams: { q?: string; category?: string }
}) {
  const supabase = createClient()
  let query = supabase
    .from('manuals')
    .select('id, title, category, created_at, updated_at')
    .order('updated_at', { ascending: false })

  if (searchParams.q) {
    query = query.ilike('title', `%${searchParams.q}%`)
  }
  if (searchParams.category) {
    query = query.eq('category', searchParams.category)
  }

  const { data: manuals } = await query

  const { data: categories } = await supabase
    .from('manuals')
    .select('category')
    .not('category', 'is', null)

  const uniqueCategories = Array.from(new Set(categories?.map((m) => m.category).filter(Boolean) ?? []))

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">マニュアル</h1>
          <p className="text-slate-400 text-sm mt-1">作業手順書の管理</p>
        </div>
        <Link
          href="/manuals/new"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-xl transition-colors"
        >
          ＋ 新規作成
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-3 mb-6">
        <form method="GET" className="flex gap-3 flex-1">
          <input
            name="q"
            defaultValue={searchParams.q}
            placeholder="マニュアルを検索..."
            className="flex-1 px-4 py-2 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
          {uniqueCategories.length > 0 && (
            <select
              name="category"
              defaultValue={searchParams.category}
              className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            >
              <option value="">すべてのカテゴリ</option>
              {uniqueCategories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          )}
          <button
            type="submit"
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded-xl transition-colors"
          >
            検索
          </button>
        </form>
      </div>

      {/* List */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 divide-y divide-slate-700">
        {manuals && manuals.length > 0 ? (
          manuals.map((manual) => (
            <Link
              key={manual.id}
              href={`/manuals/${manual.id}`}
              className="flex items-center justify-between p-5 hover:bg-slate-700/50 transition-colors group"
            >
              <div>
                <p className="text-white font-medium group-hover:text-blue-300 transition-colors">
                  {manual.title}
                </p>
                {manual.category && (
                  <span className="text-xs text-blue-400 bg-blue-400/10 px-2 py-0.5 rounded mt-1 inline-block">
                    {manual.category}
                  </span>
                )}
              </div>
              <div className="text-right text-xs text-slate-500">
                <p>更新: {new Date(manual.updated_at).toLocaleDateString('ja-JP')}</p>
              </div>
            </Link>
          ))
        ) : (
          <div className="p-16 text-center">
            <p className="text-4xl mb-4">📋</p>
            <p className="text-slate-400 font-medium">マニュアルがありません</p>
            <Link
              href="/manuals/new"
              className="mt-4 inline-block text-sm text-blue-400 hover:text-blue-300"
            >
              最初のマニュアルを作成する →
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
