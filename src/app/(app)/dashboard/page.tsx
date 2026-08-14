import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  const [
    { data: recentManuals },
    { data: recentLogs },
  ] = await Promise.all([
    supabase.from('manuals').select('id, title, category, created_at').order('created_at', { ascending: false }).limit(5),
    supabase.from('slack_logs').select('id, title, content, created_at').order('created_at', { ascending: false }).limit(5),
  ])

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">ダッシュボード</h1>
        <p className="text-slate-400 text-sm mt-1">ようこそ、{user?.email}</p>
      </div>


      {/* Quick links */}
      <div className="flex flex-wrap gap-3 mb-6">
        <a href="https://personal-support-mocha.vercel.app/dashboard" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-purple-500 rounded-xl transition-colors group">
          <span className="text-lg">🧑‍💼</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">パーソナル</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://attendance-app-prod-716327310989.asia-northeast1.run.app/login" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-green-500 rounded-xl transition-colors group">
          <span className="text-lg">🕐</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">勤怠管理</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://app.slack.com/client/T07G6EHESKG/C07GD3LRMD0" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-purple-500 rounded-xl transition-colors group">
          <span className="text-lg">💬</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Slack（くじら）</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://app.slack.com/client/TB82LHSPM/CB82LJ1B5" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-purple-500 rounded-xl transition-colors group">
          <span className="text-lg">💬</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Slack（個人）</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
      </div>

      {/* Quick Links */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 mb-8">
        <div className="p-5 border-b border-slate-700">
          <h2 className="text-base font-semibold text-white">🔗 リンク集</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-5">
          {[
            { label: '工程管理シート', url: 'https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486', icon: '📊' },
            { label: '勤怠管理システム', url: 'https://attendance-app-prod-716327310989.asia-northeast1.run.app/login', icon: '🕐' },
            { label: 'くじらCRM', url: 'https://d1zlma8f7wwwsg.cloudfront.net/login', icon: '🐋' },
            { label: 'NASサーバー', url: 'https://dxp2800-b53d.jp9.ug.link/desktop/?os=ugospro#/', icon: '🖥️' },
            { label: 'くじら社内Wiki', url: 'https://www.notion.so/kujira-device-agency/Wiki-dc27874409f24d549bb439103f852185', icon: '📖' },
            { label: 'Gmail（rukidouto）', url: 'https://mail.google.com', icon: '📧' },
          ].map((link) => (
            <a
              key={link.url}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 px-4 py-3 bg-slate-700/50 hover:bg-slate-700 border border-slate-600 hover:border-slate-500 rounded-xl transition-colors group"
            >
              <span className="text-xl">{link.icon}</span>
              <span className="text-base text-slate-200 group-hover:text-white transition-colors font-medium">{link.label}</span>
              <span className="ml-auto text-slate-500 group-hover:text-slate-300 transition-colors text-xs">↗</span>
            </a>
          ))}
        </div>
      </div>

      {/* 玄関集合機 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 mb-8">
        <div className="p-5 border-b border-slate-700">
          <h2 className="text-lg font-semibold text-white">🚪 玄関集合機</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-5">
          {[
            { label: 'Notion', url: 'https://app.notion.com/native/p/07554695c69f4f8c98f1b9a3db86c19a?deepLinkOpenNewTab=true', icon: '📝' },
            { label: 'スプレッドシート①', url: 'https://docs.google.com/spreadsheets/d/1MITcOZmpGeYc3MDTTby0bXVgFh8tlbQM1ev_mC1oVCo/edit?gid=0#gid=0', icon: '📊' },
            { label: 'スプレッドシート②', url: 'https://docs.google.com/spreadsheets/d/12xTmKKgeOKViRqf7SuLEBql0z30CczTNjVrghzkeL8I/edit?gid=1831569695#gid=1831569695', icon: '📊' },
            { label: '玄関集合機システム ログイン', url: 'https://sys.smart-interphone.kujira-realestatetech.co.jp/login', icon: '🔐' },
            { label: '施設一覧', url: 'https://sys.smart-interphone.kujira-realestatetech.co.jp/facilities', icon: '🏢' },
            { label: 'ランダム', url: 'https://www.luft.co.jp/cgi/randam.php', icon: '🎲' },
          ].map((link) => (
            <a
              key={link.url}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-4 px-5 py-4 bg-slate-700/50 hover:bg-slate-700 border border-slate-600 hover:border-slate-500 rounded-xl transition-colors group"
            >
              <span className="text-3xl">{link.icon}</span>
              <span className="text-base text-slate-200 group-hover:text-white transition-colors font-semibold">{link.label}</span>
              <span className="ml-auto text-slate-500 group-hover:text-slate-300 transition-colors text-sm">↗</span>
            </a>
          ))}
        </div>
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
