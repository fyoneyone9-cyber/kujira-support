import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  const [
    { count: manualCount },
    { count: logCount },
    { data: recentManuals },
    { data: recentLogs },
  ] = await Promise.all([
    supabase.from('manuals').select('*', { count: 'exact', head: true }),
    supabase.from('slack_logs').select('*', { count: 'exact', head: true }),
    supabase.from('manuals').select('id, title, category, created_at').order('created_at', { ascending: false }).limit(5),
    supabase.from('slack_logs').select('id, title, content, created_at').order('created_at', { ascending: false }).limit(5),
  ])

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">ダッシュボード</h1>
        <p className="text-slate-400 text-sm mt-1">ようこそ、{user?.email}</p>
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
            <p className="text-slate-400 text-sm">Slackログ数</p>
            <span className="text-2xl">💬</span>
          </div>
          <p className="text-3xl font-bold text-white">{logCount ?? 0}</p>
        </div>
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <p className="text-slate-400 text-sm">自動化フロー</p>
            <span className="text-2xl">⚡</span>
          </div>
          <p className="text-3xl font-bold text-white">0</p>
          <p className="text-xs text-slate-500 mt-1">準備中</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        <Link
          href="/logs/new"
          className="bg-blue-600/20 hover:bg-blue-600/30 border border-blue-600/40 rounded-2xl p-5 flex items-center gap-4 transition-colors group"
        >
          <span className="text-3xl">💬</span>
          <div>
            <p className="text-white font-semibold group-hover:text-blue-300 transition-colors">Slackログを貼る</p>
            <p className="text-slate-400 text-sm">やり取りをそのままコピペ</p>
          </div>
        </Link>
        <Link
          href="/manuals/new"
          className="bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-2xl p-5 flex items-center gap-4 transition-colors group"
        >
          <span className="text-3xl">📋</span>
          <div>
            <p className="text-white font-semibold">マニュアルを作成</p>
            <p className="text-slate-400 text-sm">手順書を新規作成</p>
          </div>
        </Link>
      </div>

      {/* Two columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Logs */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700">
          <div className="p-5 border-b border-slate-700 flex items-center justify-between">
            <h2 className="text-base font-semibold text-white">最近のSlackログ</h2>
            <Link href="/logs" className="text-xs text-slate-400 hover:text-white transition-colors">すべて見る →</Link>
          </div>
          <div className="divide-y divide-slate-700">
            {recentLogs && recentLogs.length > 0 ? (
              recentLogs.map((log) => (
                <Link key={log.id} href={`/logs/${log.id}`} className="block p-4 hover:bg-slate-700/50 transition-colors">
                  <p className="text-white text-sm font-medium truncate">{log.title || '(タイトルなし)'}</p>
                  <p className="text-slate-500 text-xs mt-0.5 truncate font-mono">{log.content?.slice(0, 60)}...</p>
                  <p className="text-slate-600 text-xs mt-1">{new Date(log.created_at).toLocaleDateString('ja-JP')}</p>
                </Link>
              ))
            ) : (
              <div className="p-10 text-center">
                <p className="text-slate-500 text-sm">まだログがありません</p>
                <Link href="/logs/new" className="mt-2 inline-block text-sm text-blue-400 hover:text-blue-300">貼り付ける →</Link>
              </div>
            )}
          </div>
        </div>

        {/* Recent Manuals */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700">
          <div className="p-5 border-b border-slate-700 flex items-center justify-between">
            <h2 className="text-base font-semibold text-white">最近のマニュアル</h2>
            <Link href="/manuals" className="text-xs text-slate-400 hover:text-white transition-colors">すべて見る →</Link>
          </div>
          <div className="divide-y divide-slate-700">
            {recentManuals && recentManuals.length > 0 ? (
              recentManuals.map((manual) => (
                <div key={manual.id} className="p-4 flex items-center justify-between hover:bg-slate-700/50 transition-colors">
                  <div>
                    <p className="text-white text-sm font-medium">{manual.title}</p>
                    {manual.category && (
                      <span className="text-xs text-blue-400 bg-blue-400/10 px-2 py-0.5 rounded mt-1 inline-block">{manual.category}</span>
                    )}
                  </div>
                  <p className="text-slate-500 text-xs">{new Date(manual.created_at).toLocaleDateString('ja-JP')}</p>
                </div>
              ))
            ) : (
              <div className="p-10 text-center">
                <p className="text-slate-500 text-sm">マニュアルがまだありません</p>
                <Link href="/manuals/new" className="mt-2 inline-block text-sm text-blue-400 hover:text-blue-300">作成する →</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
