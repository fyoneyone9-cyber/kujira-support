export default function TeleapoPage() {
  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">テレアポ</h1>
        <p className="text-slate-400 text-sm mt-1">架電サポート・トーク台本・よくある質問</p>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* トーク台本 */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">📞</span>
            <h2 className="text-lg font-bold text-white">トーク台本</h2>
          </div>
          <div className="space-y-3">
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-blue-400 font-medium mb-1">オープニング</p>
              <p className="text-sm text-slate-300 leading-relaxed">
                「お電話ありがとうございます。私、○○と申します。
                結婚相談所マレッジロードジャパンよりご連絡差し上げました。
                少々お時間よろしいでしょうか？」
              </p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-green-400 font-medium mb-1">ご案内</p>
              <p className="text-sm text-slate-300 leading-relaxed">
                「現在、無料カウンセリングを実施しております。
                結婚についてお悩みの方に、専任のカウンセラーが丁寧にご対応いたします。
                ご興味はございますか？」
              </p>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-4">
              <p className="text-xs text-yellow-400 font-medium mb-1">クロージング</p>
              <p className="text-sm text-slate-300 leading-relaxed">
                「それでは、ご都合のよい日時を教えていただけますか？
                ZOOMまたは対面、どちらでもご対応可能です。」
              </p>
            </div>
          </div>
        </div>

        {/* よくある断り文句と切り返し */}
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">💬</span>
            <h2 className="text-lg font-bold text-white">断り文句と切り返し</h2>
          </div>
          <div className="space-y-3">
            {[
              {
                objection: '「今は忙しい」',
                response: '「承知いたしました。では、またお時間のよいときにご連絡させていただいてもよろしいでしょうか？」',
              },
              {
                objection: '「興味がない」',
                response: '「そうでしたか。もしご友人・知人でご相談されている方がいらっしゃれば、ご紹介いただけると幸いです。」',
              },
              {
                objection: '「もう相手がいる」',
                response: '「それはおめでとうございます！もしお役に立てることがあれば、いつでもご連絡ください。」',
              },
              {
                objection: '「お金がかかりそう」',
                response: '「まずは無料カウンセリングですので、料金のご説明もその際にさせていただきます。お気軽にご参加ください。」',
              },
            ].map((item, i) => (
              <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-red-400 font-medium mb-1">{item.objection}</p>
                <p className="text-sm text-slate-300 leading-relaxed">{item.response}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 架電チェックリスト */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">✅</span>
          <h2 className="text-lg font-bold text-white">架電前チェックリスト</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            '電話番号・相手の名前を確認した',
            'トーク台本を手元に用意した',
            '静かな環境で話せる状態にある',
            '架電記録シートを開いている',
            'ZOOMリンクをすぐ送れる準備ができている',
            '無料カウンセリングの空き日程を確認した',
          ].map((item, i) => (
            <label key={i} className="flex items-center gap-3 p-3 bg-slate-700/50 rounded-xl cursor-pointer hover:bg-slate-700 transition-colors">
              <input type="checkbox" className="w-4 h-4 accent-blue-500" />
              <span className="text-sm text-slate-300">{item}</span>
            </label>
          ))}
        </div>
      </div>

      {/* 会社情報 */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">🏢</span>
          <h2 className="text-lg font-bold text-white">会社・連絡先情報</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">会社名</p>
            <p className="text-sm text-white font-medium">マレッジロードジャパン</p>
          </div>
          <div className="bg-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">電話番号</p>
            <p className="text-sm text-white font-medium">080-3207-8422</p>
          </div>
          <div className="bg-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">対応エリア</p>
            <p className="text-sm text-white font-medium">全国（ZOOM対応）</p>
          </div>
          <div className="bg-slate-700/50 rounded-xl p-4 md:col-span-3">
            <p className="text-xs text-slate-400 mb-1">所在地</p>
            <p className="text-sm text-white font-medium">〒243-0424 神奈川県海老名市社家6-5-2-301</p>
          </div>
        </div>
      </div>
    </div>
  )
}
