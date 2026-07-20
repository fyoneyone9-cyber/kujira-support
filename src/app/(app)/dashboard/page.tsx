import { createClient } from '@/lib/supabase/server'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()
  const { count: manualCount } = await supabase
    .from('manuals')
    .select('*', { count: 'exact', head: true })

  const { data: recentManuals } = await supabase
    .from('manuals')
    .select('id, title, category, created_at')
    .order('created_at', { ascending: false })
    .limit(5)

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">ダッシュボード</h1>
        <p className="text-slate-400 text-sm mt-1">
          ようこそ、{user?.email}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <p className="text-slate-400 text-sm">マニュアル数</p>
            <span className="text-2xl">📋</span>
          </div>
          <p className="text-3xl font-bold text-white">{manualCount ?? 0}</p>
        </div>
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <p className="text-slate-400 text-sm">自動化フロー</p>
            <span className="text-2xl">⚡</span>
          </div>
          <p className="text-3xl font-bold text-white">0</p>
          <p className="text-xs text-slate-500 mt-1">準備中</p>
        </div>
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <p className="text-slate-400 text-sm">チームメンバー</p>
            <span className="text-2xl">👥</span>
          </div>
          <p className="text-3xl font-bold text-white">-</p>
        </div>
      </div>

      {/* Recent Manuals */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700">
        <div className="p-6 border-b border-slate-700">
          <h2 className="text-lg font-semibold text-white">最近のマニュアル</h2>
        </div>
        <div className="divide-y divide-slate-700">
          {recentManuals && recentManuals.length > 0 ? (
            recentManuals.map((manual) => (
              <div key={manual.id} className="p-4 flex items-center justify-between hover:bg-slate-700/50 transition-colors">
                <div>
                  <p className="text-white text-sm font-medium">{manual.title}</p>
                  {manual.category && (
                    <span className="text-xs text-blue-400 bg-blue-400/10 px-2 py-0.5 rounded mt-1 inline-block">
                      {manual.category}
                    </span>
                  )}
                </div>
                <p className="text-slate-500 text-xs">
                  {new Date(manual.created_at).toLocaleDateString('ja-JP')}
                </p>
              </div>
            ))
          ) : (
            <div className="p-12 text-center">
              <p className="text-slate-500 text-sm">マニュアルがまだありません</p>
              <a
                href="/manuals/new"
                className="mt-3 inline-block text-sm text-blue-400 hover:text-blue-300"
              >
                最初のマニュアルを作成する →
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
