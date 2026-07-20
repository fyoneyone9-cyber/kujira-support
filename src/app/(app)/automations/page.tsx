export default function AutomationsPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">自動化</h1>
        <p className="text-slate-400 text-sm mt-1">業務フローの自動化管理</p>
      </div>

      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-16 text-center">
        <div className="text-6xl mb-4">⚡</div>
        <h2 className="text-xl font-semibold text-white mb-3">自動化機能 準備中</h2>
        <p className="text-slate-400 text-sm max-w-md mx-auto">
          Slackのやり取りをもとに、自動化フローを順次追加していきます。<br />
          どの業務を自動化するかが決まり次第、こちらに追加されます。
        </p>
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto text-left">
          {[
            { icon: '📨', title: '通知自動化', desc: '特定条件でSlack/メール通知' },
            { icon: '📝', title: 'レポート生成', desc: '定期的な報告書の自動作成' },
            { icon: '🔄', title: 'ワークフロー', desc: '承認フロー・タスク自動割り当て' },
          ].map((item) => (
            <div key={item.title} className="bg-slate-700/50 rounded-xl p-4 border border-slate-600 opacity-60">
              <div className="text-2xl mb-2">{item.icon}</div>
              <p className="text-white text-sm font-medium">{item.title}</p>
              <p className="text-slate-400 text-xs mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
