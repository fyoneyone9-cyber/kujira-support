export default function RentacarPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">🚗 レンタカー</h1>
        <p className="text-slate-400 text-sm mt-1">レンタカー関連システム・業務手順</p>
      </div>

      {/* クイックリンク */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <a
          href="https://manage.sys.rentacar.and-iot.jp/system-admin?tab=usage-status"
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col items-center gap-2 px-4 py-5 bg-blue-700 hover:bg-blue-600 border border-blue-500 rounded-2xl transition-colors"
        >
          <span className="text-3xl">🔐</span>
          <span className="text-sm font-bold text-white">管理システム（利用状況）</span>
        </a>
        <a
          href="https://docs.google.com/spreadsheets/d/150wKremcy74Qx8hAzQiUGVa8p3vp0JPp2iEVPDu-WF8/edit?gid=1550991846#gid=1550991846"
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col items-center gap-2 px-4 py-5 bg-green-700 hover:bg-green-600 border border-green-500 rounded-2xl transition-colors"
        >
          <span className="text-3xl">📊</span>
          <span className="text-sm font-bold text-white">車両システム利用料シート</span>
        </a>
        <a
          href="https://miyakojima.rentacarlite.and-iot.jp/login"
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col items-center gap-2 px-4 py-5 bg-cyan-700 hover:bg-cyan-600 border border-cyan-500 rounded-2xl transition-colors"
        >
          <span className="text-3xl">🏝️</span>
          <span className="text-sm font-bold text-white">宮古島 予約管理</span>
        </a>
      </div>

      {/* 車両システム利用料確定業務 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 mb-8">
        <div className="p-5 border-b border-slate-700">
          <h2 className="text-base font-semibold text-white">📋 車両システム利用料確定業務（毎月末〜翌月上旬）</h2>
          <p className="text-slate-400 text-xs mt-1">導入支援チーム定例業務 ・ 当月利用分 → 翌月に確定・請求発行</p>
        </div>
        <div className="p-5 space-y-4">

          {/* Step 1 */}
          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">1</div>
            <div className="flex-1">
              <p className="text-white font-medium text-sm mb-1">管理システムにログインして利用予約数を確認</p>
              <p className="text-slate-400 text-xs mb-2">管理者権限でアクセス。対象年月を指定しクライアントごとの利用台数を確認します。</p>
              <a
                href="https://manage.sys.rentacar.and-iot.jp/system-admin?tab=usage-status"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 text-xs underline"
              >
                管理システム（利用状況タブ）を開く ↗
              </a>
            </div>
          </div>

          {/* Step 2 */}
          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">2</div>
            <div className="flex-1">
              <p className="text-white font-medium text-sm mb-1">スプレッドシートを開き、該当クライアントシートへ</p>
              <p className="text-slate-400 text-xs mb-2">クライアントごとに個別シートがあります。月次明細テーブルの<span className="text-yellow-400 font-medium">最下行に新規1行を追加</span>します。</p>
              <a
                href="https://docs.google.com/spreadsheets/d/150wKremcy74Qx8hAzQiUGVa8p3vp0JPp2iEVPDu-WF8/edit?gid=1550991846#gid=1550991846"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-green-400 hover:text-green-300 text-xs underline"
              >
                車両システム利用料シートを開く ↗
              </a>
            </div>
          </div>

          {/* Step 3 */}
          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">3</div>
            <div>
              <p className="text-white font-medium text-sm mb-1">「対象月」と「数量（台数）」を入力</p>
              <p className="text-slate-400 text-xs">入力は<span className="text-yellow-400 font-medium">この2項目のみ</span>。請求金額はB4の料金体系設定に基づき<span className="text-green-400 font-medium">自動計算</span>されます。</p>
              <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                <div className="bg-slate-600/50 rounded-lg p-2">
                  <p className="text-slate-300 font-medium">従量制</p>
                  <p className="text-slate-400">単価（B5）× 台数</p>
                </div>
                <div className="bg-slate-600/50 rounded-lg p-2">
                  <p className="text-slate-300 font-medium">段階定額</p>
                  <p className="text-slate-400">台数範囲で自動判定</p>
                </div>
              </div>
            </div>
          </div>

          {/* Step 4 */}
          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">4</div>
            <div>
              <p className="text-white font-medium text-sm mb-1">計算結果を目視確認</p>
              <p className="text-slate-400 text-xs">自動計算された金額が、選択中の料金体系（従量制 or 段階定額）と合致しているか必ず確認します。</p>
            </div>
          </div>

          {/* 例外2社 警告 */}
          <div className="mt-2 p-4 bg-red-900/30 border border-red-700/60 rounded-xl">
            <p className="text-red-400 text-sm font-bold mb-2">⚠️ 例外対応が必要な2社（請求漏れ・誤請求注意）</p>
            <div className="space-y-2">
              <div className="flex gap-3 items-start">
                <span className="text-red-300 text-xs font-bold flex-shrink-0 mt-0.5">🚫 瀬戸内アイランドクルーズ</span>
                <p className="text-slate-400 text-xs">車両システム利用料を徴収していないため、<span className="text-red-300 font-medium">毎月の請求作業は不要</span>。</p>
              </div>
              <div className="flex gap-3 items-start">
                <span className="text-yellow-300 text-xs font-bold flex-shrink-0 mt-0.5">⏸️ メーカーズ</span>
                <p className="text-slate-400 text-xs">月額料金が未発生のため現在は請求しない。料金発生条件が確定次第、<span className="text-yellow-300 font-medium">速やかに九地良（クジラ）へ連絡</span>。</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 新規クライアント追加 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 mb-8">
        <div className="p-5 border-b border-slate-700">
          <h2 className="text-base font-semibold text-white">➕ 新規クライアント追加時のセットアップ</h2>
        </div>
        <div className="p-5 space-y-3">
          {[
            { step: '1', text: '既存シートを右クリック →「コピーを作成」で複製' },
            { step: '2', text: 'シート名とセルA1のタイトルを新規クライアント名に変更' },
            { step: '3', text: 'B4のドロップダウンで料金体系を選択し、単価または段階テーブルを設定' },
          ].map((item) => (
            <div key={item.step} className="flex gap-3 items-center">
              <span className="flex-shrink-0 w-6 h-6 bg-slate-600 rounded-full flex items-center justify-center text-white text-xs font-bold">{item.step}</span>
              <p className="text-slate-300 text-sm">{item.text}</p>
            </div>
          ))}
        </div>
      </div>

      {/* その他リンク */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700">
        <div className="p-5 border-b border-slate-700">
          <h2 className="text-base font-semibold text-white">🔗 関連リンク</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-5">
          {[
            { label: '管理スプレッドシート', url: 'https://docs.google.com/spreadsheets/d/1Tae6Ez5Vsg5DPZ97vFTSNsCqqg9U0jLhsE4b-nvuDHE/edit?gid=1555490795#gid=1555490795', icon: '📊' },
            { label: '管理システム（ログイン）', url: 'https://manage.sys.rentacar.and-iot.jp/auth/login', icon: '🔐' },
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
    </div>
  )
}
