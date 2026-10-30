# -*- coding: utf-8 -*-
"""[ALERT_ACTION_LOG_V1 2026-10-29]
カード上部の「⚠️ 要対応」バー全体に対する対応履歴欄を追加する。

要望: 要対応が出たとき「いつ・どんなアクションを取ったか」を近くに記録したい。
      PMS/スマートロックには [INTEG_ACTION_LOG_V1] で追加済み。今回はそれ以外の
      全アラート（納期超過 / JITボックス未発注 / 作業員情報未入力 / 入金未確認 /
      PayCube未発注 / ヒアリング・工程表・Slack未登録 など）が対象。

設計: アラートは種類が多く変動するため、項目ごとに欄を散らすと画面が破綻する。
      cardAlerts バーの直下に1つだけ置き、そこに時系列で積む方式にする。
      保存先は dashboard_todos.alert_action_log（import-csvが触らない安全地帯）。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_alertlog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                {/* [CARD_ALERTS_V1] 総合アラートバー（コマ上部・クリックで該当箇所へジャンプ） */}
                {cardAlerts.length > 0 && (
                  <div className="bg-red-900/40 border border-red-600 rounded-lg px-3 py-2 flex items-center gap-2 flex-wrap">
                    <span className="text-xs font-bold text-red-300">⚠️ 要対応:</span>
                    {cardAlerts.map((a, i) => (
                      a.target
                        ? <button key={i} onClick={() => jumpToSection(a.target)}
                            className="text-xs px-2 py-0.5 rounded-full bg-red-800/80 hover:bg-red-600 text-red-100 font-bold cursor-pointer transition-colors">{a.label} ↗</button>
                        : <span key={i} className="text-xs px-2 py-0.5 rounded-full bg-red-800/80 text-red-100 font-bold">{a.label}</span>
                    ))}
                  </div>
                )}"""
assert s.count(OLD) == 1, "anchor"

NEW = """                {/* [CARD_ALERTS_V1] 総合アラートバー（コマ上部・クリックで該当箇所へジャンプ） */}
                {cardAlerts.length > 0 && (
                  <div className="bg-red-900/40 border border-red-600 rounded-lg px-3 py-2 space-y-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-bold text-red-300">⚠️ 要対応:</span>
                      {cardAlerts.map((a, i) => (
                        a.target
                          ? <button key={i} onClick={() => jumpToSection(a.target)}
                              className="text-xs px-2 py-0.5 rounded-full bg-red-800/80 hover:bg-red-600 text-red-100 font-bold cursor-pointer transition-colors">{a.label} ↗</button>
                          : <span key={i} className="text-xs px-2 py-0.5 rounded-full bg-red-800/80 text-red-100 font-bold">{a.label}</span>
                      ))}
                    </div>
                    {/* [ALERT_ACTION_LOG_V1 2026-10-29] 要対応に対する「いつ・何をしたか」の記録。
                        アラートは種類が多く変動するため、項目ごとではなくここに集約して時系列で積む。
                        保存先は dashboard_todos なので CSV再取込でも消えない。 */}
                    {(() => {
                      const log = (it.dashboard_todos?.['alert_action_log'] as string) || ''
                      const today = new Date().toISOString().slice(0, 10)
                      const append = (text: string) => {
                        const line = `${today} ${text}`
                        saveTodoKey(it.id, it.dashboard_todos, 'alert_action_log', log ? `${log}\\n${line}` : line)
                      }
                      return (
                        <div className="pt-1.5 border-t border-red-700/50 space-y-1">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            <span className="text-[11px] text-red-200 font-bold">📝 対応履歴:</span>
                            {['電話した', 'メール送った', 'Slackで連絡', '先方確認待ち', '社内確認中', '発注した', '対応完了'].map(q => (
                              <button key={q} onClick={() => append(q)}
                                className="text-[11px] px-1.5 py-0.5 rounded bg-red-950/60 hover:bg-blue-700 text-red-200 hover:text-white border border-red-800/60 transition-colors"
                                title={`「${today} ${q}」を追記`}>+{q}</button>
                            ))}
                          </div>
                          <textarea
                            defaultValue={log}
                            onBlur={(e) => { if (e.target.value !== log) saveTodoKey(it.id, it.dashboard_todos, 'alert_action_log', e.target.value) }}
                            rows={log ? Math.min(8, log.split('\\n').length + 1) : 2}
                            placeholder={`例: ${today} 担当者に架電、来週までに回答もらう`}
                            className="w-full text-xs bg-slate-900/80 border border-red-900/60 rounded px-2 py-1 text-slate-100 placeholder-slate-600 focus:border-blue-500 focus:outline-none resize-y"
                          />
                          {log && (
                            <p className="text-[11px] text-red-200/70">
                              最終対応: {log.split('\\n').filter(Boolean).slice(-1)[0] || '-'}
                            </p>
                          )}
                        </div>
                      )
                    })()}
                  </div>
                )}"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
