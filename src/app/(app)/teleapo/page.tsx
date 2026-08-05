export default function TeleapoPage() {
  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">テレアポ</h1>
        <p className="text-slate-400 text-sm mt-1">HubSpot 架電業務マニュアル（スマートチェックイン）</p>
      </div>

      {/* Step Flow */}
      <div className="mb-8">
        <h2 className="text-lg font-bold text-white mb-4">📋 架電業務フロー</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {[
            { step: '1', title: 'ビュー設定', desc: 'テーブルビューに切替・フィルター設定', color: 'blue' },
            { step: '2', title: '列の編集', desc: '前回の連絡・優先度を追加してソート', color: 'purple' },
            { step: '3', title: '対象選定', desc: '優先度「高」「中」はスキップ・上から順に', color: 'yellow' },
            { step: '4', title: '架電・更新', desc: '担当者変更→電話→ステージ更新', color: 'green' },
          ].map((item) => (
            <div key={item.step} className={`bg-slate-800 rounded-2xl border border-slate-700 p-5 relative`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mb-3 ${
                item.color === 'blue' ? 'bg-blue-600 text-white' :
                item.color === 'purple' ? 'bg-purple-600 text-white' :
                item.color === 'yellow' ? 'bg-yellow-600 text-white' :
                'bg-green-600 text-white'
              }`}>
                {item.step}
              </div>
              <p className="text-white font-bold text-sm mb-1">{item.title}</p>
              <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

        {/* STEP1: ビュー設定 */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white">1</span>
            <h2 className="text-base font-bold text-white">ビューの設定とフィルター</h2>
          </div>
          <div className="space-y-3">
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-blue-400 font-bold mb-2">① テーブルビューに切り替える</p>
              <p className="text-sm text-slate-300">HubSpot CRM の <span className="text-white font-medium">「取引」画面</span> を開き、表示形式を <span className="text-blue-300 font-medium">「テーブルビュー」</span> に変更する。</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-blue-400 font-bold mb-2">② 詳細フィルターを設定する</p>
              <p className="text-sm text-slate-300 mb-2">「詳細フィルター」を開き、取引ステージで以下を選択：</p>
              <div className="bg-slate-900 rounded-lg px-3 py-2">
                <p className="text-yellow-300 text-sm font-medium">楽天トラベル（不在）（スマートチェックイン）</p>
              </div>
            </div>
          </div>
        </div>

        {/* STEP2: 列の編集 */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="w-7 h-7 bg-purple-600 rounded-full flex items-center justify-center text-xs font-bold text-white">2</span>
            <h2 className="text-base font-bold text-white">表示列の編集と並び替え</h2>
          </div>
          <div className="space-y-3">
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-purple-400 font-bold mb-2">① 「前回の連絡」を追加</p>
              <p className="text-sm text-slate-300">「列を編集」から <span className="text-purple-300 font-medium">「前回の連絡」</span> を検索して追加。いつ最後に接触したか確認できる。</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-purple-400 font-bold mb-2">② 「優先度」を追加</p>
              <p className="text-sm text-slate-300">同様に <span className="text-purple-300 font-medium">「優先度」</span> を追加。架電をスキップする判断に使う。</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-purple-400 font-bold mb-2">③ 「前回の連絡」でソート</p>
              <p className="text-sm text-slate-300">「前回の連絡」列の矢印をクリックし、<span className="text-white font-medium">過去のものから順（昇順）</span>に並び替える。</p>
            </div>
          </div>
        </div>

        {/* STEP3: 対象選定 */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="w-7 h-7 bg-yellow-600 rounded-full flex items-center justify-center text-xs font-bold text-white">3</span>
            <h2 className="text-base font-bold text-white">架電対象の選定ルール</h2>
          </div>
          <div className="space-y-3">
            <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
              <p className="text-xs text-red-400 font-bold mb-2">⚠️ スキップするレコード</p>
              <p className="text-sm text-slate-300">優先度が <span className="text-red-300 font-bold">「高」または「中」</span> のレコードは架電不要。すでに進行中の可能性が高い。</p>
            </div>
            <div className="bg-green-950/50 border border-green-800/50 rounded-xl p-4">
              <p className="text-xs text-green-400 font-bold mb-2">✅ 架電する順番</p>
              <p className="text-sm text-slate-300">リストの <span className="text-green-300 font-bold">上から順番</span> に架電を進める。</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-slate-400 font-bold mb-2">💡 効率化テクニック</p>
              <p className="text-sm text-slate-300">ブラウザのタブを複製しておくと、リスト画面と詳細画面を素早く行き来できる。</p>
            </div>
          </div>
        </div>

        {/* STEP4: 架電・更新 */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="w-7 h-7 bg-green-600 rounded-full flex items-center justify-center text-xs font-bold text-white">4</span>
            <h2 className="text-base font-bold text-white">架電の実施フロー</h2>
          </div>
          <div className="space-y-3">
            <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
              <p className="text-xs text-red-400 font-bold mb-2">★ 必須：取引担当者の変更</p>
              <p className="text-sm text-slate-300">架電前に必ず担当者を <span className="text-red-300 font-bold">「米山」</span> に変更する。これを忘れずに！</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-green-400 font-bold mb-2">① 電話をかける</p>
              <p className="text-sm text-slate-300">画面左の <span className="text-white font-medium">通話（電話）ボタン</span> → 「電話をかける」をクリックして発信。</p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-green-400 font-bold mb-2">② 取引ステージを更新する</p>
              <p className="text-sm text-slate-300 mb-2">通話終了後、結果に合わせてステージを変更：</p>
              <div className="flex gap-2 flex-wrap">
                <span className="text-xs bg-red-900/60 text-red-300 border border-red-700 rounded-lg px-3 py-1">お断り</span>
                <span className="text-xs bg-blue-900/60 text-blue-300 border border-blue-700 rounded-lg px-3 py-1">資料送付</span>
                <span className="text-xs bg-slate-600/60 text-slate-300 border border-slate-500 rounded-lg px-3 py-1">その他</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* 重要ポイント早見表 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">📌</span>
          <h2 className="text-lg font-bold text-white">重要ポイント早見表</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left text-slate-400 font-medium py-2 pr-4 whitespace-nowrap">項目</th>
                <th className="text-left text-white font-medium py-2">内容</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {[
                { label: '対象取引ステージ', value: '楽天トラベル（不在）（スマートチェックイン）', highlight: true },
                { label: '追加する表示列', value: '「前回の連絡」「優先度」' },
                { label: 'ソート基準', value: '「前回の連絡」日時の昇順（過去から）' },
                { label: 'スキップ条件', value: '優先度が「高」または「中」のレコード', highlight: true },
                { label: '架電順序', value: 'リストの上から順番' },
                { label: '架電前の必須作業', value: '取引担当者を「米山」に変更（★絶対忘れずに）', highlight: true },
                { label: '架電後の作業', value: '取引ステージを結果に応じて更新（お断り／資料送付 など）' },
              ].map((row, i) => (
                <tr key={i}>
                  <td className="text-slate-400 py-3 pr-4 whitespace-nowrap font-medium">{row.label}</td>
                  <td className={`py-3 ${row.highlight ? 'text-yellow-300 font-medium' : 'text-slate-300'}`}>{row.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 参考資料 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">📁</span>
          <h2 className="text-lg font-bold text-white">参考資料</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a
            href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group"
          >
            <span className="text-xl">📊</span>
            <div>
              <p className="text-white text-sm font-medium group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル（スプレッドシート）</p>
              <p className="text-slate-500 text-xs mt-0.5">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a
            href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group"
          >
            <span className="text-xl">📋</span>
            <div>
              <p className="text-white text-sm font-medium group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-500 text-xs mt-0.5">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}
