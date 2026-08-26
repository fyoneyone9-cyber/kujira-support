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
          <h2 className="text-base font-semibold text-white">📋 車両システム利用料確定業務（定例）</h2>
          <p className="text-slate-400 text-xs mt-1">毎月実施 ・ 導入支援チーム定例業務</p>
        </div>
        <div className="p-5 space-y-4">
          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">1</div>
            <div>
              <p className="text-white font-medium text-sm mb-1">管理システムにログイン</p>
              <p className="text-slate-400 text-xs mb-2">管理者権限で以下のURLにアクセスします。</p>
              <a
                href="https://manage.sys.rentacar.and-iot.jp/system-admin?tab=usage-status"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 text-xs underline"
              >
                https://manage.sys.rentacar.and-iot.jp/system-admin?tab=usage-status ↗
              </a>
            </div>
          </div>

          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">2</div>
            <div>
              <p className="text-white font-medium text-sm mb-1">対象年月を指定して利用予約数を確認</p>
              <p className="text-slate-400 text-xs">「usage-status」タブで対象月を選択し、クライアントごとの利用予約数を確認します。</p>
            </div>
          </div>

          <div className="flex gap-4 p-4 bg-slate-700/50 border border-slate-600 rounded-xl">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">3</div>
            <div>
              <p className="text-white font-medium text-sm mb-1">スプレッドシートに入力</p>
              <p className="text-slate-400 text-xs mb-2">該当クライアントの利用予約数をスプレッドシートに記入します。</p>
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

          <div className="mt-2 p-3 bg-yellow-900/30 border border-yellow-700/50 rounded-xl">
            <p className="text-yellow-400 text-xs font-medium">⚠️ 詳細な手順は「運用メモ」を確認してください。</p>
          </div>
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
