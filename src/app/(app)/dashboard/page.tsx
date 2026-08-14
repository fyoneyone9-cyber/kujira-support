import { createClient } from '@/lib/supabase/server'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

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
        <a href="https://app.slack.com/client/TB82LHSPM/CB82LJ1B5" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-purple-500 rounded-xl transition-colors group">
          <span className="text-lg">💬</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Slack（くじら）</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://app.slack.com/client/T07G6EHESKG/C07GD3LRMD0" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-purple-500 rounded-xl transition-colors group">
          <span className="text-lg">💬</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Slack（個人）</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://vercel.com/nextralabos" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-white rounded-xl transition-colors group">
          <span className="text-lg">▲</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Vercel</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://gemini.google.com/app" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-blue-400 rounded-xl transition-colors group">
          <span className="text-lg">✨</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Gemini</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://claude.ai/new" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-orange-400 rounded-xl transition-colors group">
          <span className="text-lg">🤖</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Claude</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://chatgpt.com/" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-green-400 rounded-xl transition-colors group">
          <span className="text-lg">💡</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">ChatGPT</span>
          <span className="text-slate-500 text-xs">↗</span>
        </a>
        <a href="https://www.genspark.ai/agents?type=ai_chat" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-pink-400 rounded-xl transition-colors group">
          <span className="text-lg">⚡</span>
          <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">Genspark</span>
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
    </div>
  )
}
